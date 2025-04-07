#  PyTransit: fast and easy exoplanet transit modelling in Python.
#  Copyright (C) 2010-2020  Hannu Parviainen
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

from typing import Tuple, Optional, Union
from pathlib import Path

from numpy import ndarray, linspace, meshgrid, transpose, asarray, newaxis, errstate
from numba import njit

from .ldmodel import LDModel
from .numba.ldtkldm import trilinear_interpolation_set, integrate_profiles_set

try:
    from ldtk import LDPSetCreator
except ImportError:
    class LDPSetCreator:
        def __init__(self, *nargs, **kwargs):
            raise ModuleNotFoundError('LDTkLDModel requires LDTk.')

@njit
def ntrapz(x, y):
    npt = x.size
    ii = 0.0
    for i in range(1, npt):
        ii += (x[i] - x[i - 1]) * 0.5 * (y[i] + y[i - 1])
    return ii


class LDTkLDModel(LDModel):
    def __init__(self, pbs: Tuple, teff: Tuple[float, float], logg: Tuple[float, float], metal: Tuple[float, float],
                 cache: Optional[Union[str, Path]] = None, dataset: str = 'vis-lowres'):

        super().__init__()
        self.sc = LDPSetCreator(teff, logg, metal, pbs, cache=cache, dataset=dataset)
        self.pbs = pbs
        self.npb = len(pbs)
        self.mu = None
        self.nmu = 0
        self.ps = None
        self.profiles = None
        self.rgi = None

    def _init_interpolation(self, mu):
        self.mu = mu
        self.nmu = mu.size
        c = self.sc.client

        teffs = linspace(*c.teffl, self.sc.client.nteff)
        loggs = linspace(*c.loggl, self.sc.client.nlogg)
        zs = linspace(*c.zl, self.sc.client.nz)
        teffg, loggg, zg = meshgrid(teffs, loggs, zs)
        self.teff0, self.dteff, self.nteff = teffs[0], teffs[1]-teffs[0], self.sc.client.nteff
        self.logg0, self.dlogg, self.nlogg = loggs[0], loggs[1]-loggs[0], self.sc.client.nlogg
        self.metal0, self.dmetal, self.nmetal = zs[0], zs[1]-zs[0], self.sc.client.nz

        with errstate(divide='ignore'):
            self.ps = self.sc.create_profiles(teff=teffg.ravel(), logg=loggg.ravel(), metal=zg.ravel())
            self.ps.resample(mu=self.mu)
            self.profiles = transpose(self.ps._ldps.copy(), axes=(1, 0, 2)).reshape((self.nteff, self.nlogg, self.nmetal, self.npb, self.nmu))

    def __call__(self, mu: ndarray, x: ndarray) -> Tuple[ndarray, ndarray]:
        if self.mu is None or id(mu) != id(self.mu):
            self._init_interpolation(mu)

        x = asarray(x)
        if x.ndim == 1:
            x = x[newaxis, newaxis, :]
        elif x.ndim == 2:
            x = x[:, newaxis, :]

        ldp = trilinear_interpolation_set(self.profiles, x[:, 0, 0], x[:, 0, 1], x[:, 0, 2],
                                          self.teff0, self.dteff, self.nteff,
                                          self.logg0, self.dlogg, self.nlogg,
                                          self.metal0, self.dmetal, self.nmetal)
        ldi = integrate_profiles_set(self.mu, ldp)
        return ldp, ldi

    def _evaluate(self, mu: ndarray, x: ndarray) -> ndarray:
        raise NotImplementedError

    def _integrate(self, x: ndarray) -> float:
        raise NotImplementedError

class LDTkLD(LDTkLDModel):
    ...