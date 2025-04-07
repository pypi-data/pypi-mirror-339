#  PyTransit: fast and easy exoplanet transit modelling in Python.
#  Copyright (C) 2010-2019  Hannu Parviainen
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Tuple, Callable, Union, List, Optional
from warnings import warn

from numba import get_num_threads
from numpy import ndarray, linspace, isscalar, unique, atleast_1d
from scipy.integrate import trapezoid

from ..ldmodel import LDModel
from ..numba.ldmodels import *
from ..transitmodel import TransitModel

from .common import create_z_grid, calculate_weights_3d
from .model import rrmodel

__all__ = ['RoadRunnerModel']


class RoadRunnerModel(TransitModel):
    ldmodels = {'uniform': (ld_uniform, ldi_uniform),
                'linear': (ld_linear, ldi_linear),
                'quadratic': (ld_quadratic, ldi_quadratic),
                'quadratic-tri': (ld_quadratic_tri, ldi_quadratic_tri),
                'nonlinear': ld_nonlinear,
                'general': ld_general,
                'square_root': ld_square_root,
                'logarithmic': ld_logarithmic,
                'exponential': ld_exponential,
                'power-2': (ld_power_2, ldi_power_2),
                'power-2-pm': ld_power_2_pm}

    def __init__(self, ldmodel: Union[str, Callable, Tuple[Callable, Callable]] = 'quadratic',
                 precompute_weights: bool = False, klims: tuple = (0.005, 0.5), nk: int = 256,
                 nzin: int = 20, nzlimb: int = 20, zcut: float = 0.7, ng: int = 100,
                 nthreads: int = 1, small_planet_limit: float = 0.05, **kwargs):
        """The RoadRunner transit model by Parviainen (2020).

        Parameters
        ----------
        precompute_weights : bool, optional
            Precompute a 3D weight table for radius ratio values set by `klims`.
        klims : tuple, optional
            Radius ratio limits (kmin, kmax) for the precomputed weight table.
        nk : int, optional
            Radius ratio grid size for the precomputed weight table.
        nzin : int, optional
            Normalized distance grid size for the inner disk.
        nzlimb : int, optional
            Normalized distance grid size for the limb.
        zcut: float, optional
            Normalized distance that separates the stellar disk into an inner disk and limb.
        ng : int, optional
            Size of the grazing value table.
        nthreads: int, optional
            Number of threads to use for the model computation.
        small_planet_limit: float, optional
            The radius ratio limit below which to use a small planet approximation.
        """
        super().__init__()

        if 'interpolate' in kwargs:
            warn("The 'interpolate' argument has been replaced by 'precompute_weights' and will be removed in the future.", FutureWarning)
            self.interpolate: bool = kwargs.get('interpolate', False)
        else:
            self.interpolate: bool = precompute_weights

        if 'parallel' in kwargs:
            warn("The 'parallel' argument has been replaced by 'nthreads' and will be removed in the future.", FutureWarning)
            self.nthreads: int = get_num_threads()
            self.parallel: bool = True
        else:
            self.nthreads: int = nthreads
            self.parallel = self.nthreads > 1

        self.splimit: float = small_planet_limit

        # Set up the limb darkening model
        # --------------------------------
        if isinstance(ldmodel, str):
            try:
                if isinstance(self.ldmodels[ldmodel], tuple):
                    self.ldmodel = self.ldmodels[ldmodel][0]
                    self.ldmmean = self.ldmodels[ldmodel][1]
                else:
                    self.ldmodel = self.ldmodels[ldmodel]
                    self.ldmmean = None
            except KeyError:
                print(
                    f"Unknown limb darkening model: {ldmodel}. Choose from [{', '.join(self.ldmodels.keys())}] or supply a callable function.")
                raise
        elif isinstance(ldmodel, LDModel):
            self.ldmodel = ldmodel
            self.ldmmean = ldmodel._integrate
        elif callable(ldmodel):
            self.ldmodel = ldmodel
            self.ldmmean = None
        elif isinstance(ldmodel, tuple) and callable(ldmodel[0]) and callable(ldmodel[1]):
            self.ldmodel = ldmodel[0]
            self.ldmmean = ldmodel[1]
        else:
            raise NotImplementedError

        # Set the basic variable
        # ----------------------
        self.klims = klims
        self.nk = nk
        self.ng = ng
        self.nzin = nzin
        self.nzlimb = nzlimb
        self.zcut = zcut

        # Declare the basic arrays
        # ------------------------
        self.ze = None
        self.zm = None
        self.mu = None
        self.dk = None
        self.dg = None
        self.weights = None

        self._ldmu = linspace(1, 0, 200)
        self._ldz = sqrt(1 - self._ldmu ** 2)

        self.init_integration(nzin, nzlimb, zcut, ng, nk)

    def set_data(self, time: Union[ndarray, List],
                 lcids: Optional[Union[ndarray, List]] = None,
                 pbids: Optional[Union[ndarray, List]] = None,
                 nsamples: Optional[Union[ndarray, List]] = None,
                 exptimes: Optional[Union[ndarray, List]] = None,
                 epids: Optional[Union[ndarray, List]] = None) -> None:
        super().set_data(time, lcids, pbids, nsamples, exptimes, epids)
        self.nep = unique(self.epids).size

    def init_integration(self, nzin, nzlimb, zcut, ng, nk):
        self.nk = nk
        self.ng = ng
        self.nzin = nzin
        self.nzlimb = nzlimb
        self.zcut = zcut
        self.ze, self.zm = create_z_grid(zcut, nzin, nzlimb)
        self.mu = sqrt(1 - self.zm ** 2)
        self.dk, self.dg, self.weights = calculate_weights_3d(nk, self.klims[0], self.klims[1], self.ze, ng)

    def evaluate(self, k: Union[float, ndarray], ldc: Union[ndarray, List],
                 t0: Union[float, ndarray], p: Union[float, ndarray], a: Union[float, ndarray],
                 i: Union[float, ndarray], e: Union[float, ndarray] = 0.0, w: Union[float, ndarray] = 0.0,
                 copy: bool = True) -> ndarray:
        """Evaluate the transit model for a set of scalar or vector parameters.

        Parameters
        ----------
        k
            Radius ratio(s) either as a single float, 1D vector, or 2D array.
        ldc
            Limb darkening coefficients as a 1D or 2D array.
        t0
            Transit center(s) as a float or a 1D vector.
        p
            Orbital period(s) as a float or a 1D vector.
        a
            Orbital semi-major axis (axes) divided by the stellar radius as a float or a 1D vector.
        i
            Orbital inclination(s) as a float or a 1D vector.
        e : optional
            Orbital eccentricity as a float or a 1D vector.
        w : optional
            Argument of periastron as a float or a 1D vector.

        Notes
        -----
        The model can be evaluated either for one set of parameters or for many sets of parameters simultaneously. In
        the first case, the orbital parameters should all be given as floats. In the second case, the orbital parameters
        should be given as a 1D array-like.

        Returns
        -------
        ndarray
            Modelled flux either as a 1D or 2D ndarray.
        """

        npv = 1 if isscalar(p) else p.size
        ldc = atleast_1d(ldc)

        if isinstance(self.ldmodel, LDModel):
            ldp, istar = self.ldmodel(self.mu, ldc)
        else:
            ldp = evaluate_ld(self.ldmodel, self.mu, ldc)

            if self.ldmmean is not None:
                istar = evaluate_ldi(self.ldmmean, ldc)
            else:
                istar = zeros((npv, self.npb))
                ldpi = evaluate_ld(self.ldmodel, self._ldmu, ldc)
                for ipv in range(npv):
                    for ipb in range(self.npb):
                        istar[ipv, ipb] = 2 * pi * trapezoid(self._ldz * ldpi[ipv, ipb], self._ldz)

        flux = rrmodel(self.time, k, t0, p, a, i, e, w, self.parallel,
                       self.nlc, self.npb, self.nep, self.lcids, self.pbids, self.epids, self.nsamples, self.exptimes,
                       ldp, istar, self.weights, self.dk, self.klims[0], self.klims[1], self.dg, self.ze)

        return flux