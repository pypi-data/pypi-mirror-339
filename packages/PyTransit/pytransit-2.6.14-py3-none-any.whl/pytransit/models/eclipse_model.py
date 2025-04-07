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

from typing import Union, Optional

from numba import njit
from numpy import ndarray, squeeze, zeros, asarray, ones
from .numba.ma_uniform_nb import uniform_model_v, uniform_model_s, uniform_model_pv
from .transitmodel import TransitModel

__all__ = ['EclipseModel']

npfloat = Union[float, ndarray]


class EclipseModel(TransitModel):

    def __init__(self) -> None:
        super().__init__()

    def evaluate(self, k: npfloat, t0: npfloat, p: npfloat, a: npfloat, i: npfloat, e: npfloat = None, w: npfloat = None,
                 fr: npfloat = None, multiplicative: bool = False, copy: bool = True) -> ndarray:
        """Evaluates a secondary eclipse model for a set of scalar or vector parameters.

        Parameters
        ----------
        k
            Radius ratio(s) either as a single float or a 1D vector.
        t0
            Transit center(s) as a float or a 1D vector.
        p
            Orbital period(s) as a float or a 1D vector.
        a
            Orbital semi-major axis (axes) divided by the stellar radius as a float or a 1D vector.
        i
            Orbital inclination(s) as a float or a 1D vector.
        e
            Orbital eccentricity as a float or a 1D vector.
        w
            Argument of periastron as a float or a 1D vector.
        fr
            Planet-star flux ratio as a float or a 1D vector.
        multiplicative
            If True, will return the fraction of the visible planet disk area to the total planet disk area
        copy

        Notes
        -----
        The model can be evaluated either for one set of parameters or for many sets of parameters simultaneously.
        The orbital parameters can be given either as a float or a 1D array-like (preferably ndarray for optimal speed.)

        Returns
        -------
        Transit model
        """

        k = asarray(k)

        # Scalar parameters branch
        # ------------------------
        if isinstance(t0, float):
            e = 0. if e is None else e
            w = 0. if w is None else w

            flux = uniform_model_s(self.time, k, t0, p, a, i, e, w, self.lcids, self.pbids, self.nsamples,
                                   self.exptimes, zsign=-1.0)

        # Parameter population branch
        # ---------------------------
        else:
            npv = t0.size
            e = zeros(npv) if e is None else e
            w = zeros(npv) if w is None else w

            if k.ndim == 1:
                k = k.reshape((k.size,1))

            flux = uniform_model_v(self.time, k, t0, p, a, i, e, w, self.lcids, self.pbids, self.nsamples, self.exptimes,
                                   zsign=-1.0)

        if fr is not None:
            flux = 1.0 + (flux - 1.0) * fr
        elif multiplicative:
            flux = 1.0 + (flux - 1.0) / k**2

        return squeeze(flux)
