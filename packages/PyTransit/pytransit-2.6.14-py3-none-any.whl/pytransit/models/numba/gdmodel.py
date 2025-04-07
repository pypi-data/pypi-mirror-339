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

from numba import njit, prange
from scipy.constants import G, k, h, c
from numpy import exp, pi, sqrt, zeros, sin, cos, nan, inf, linspace, meshgrid, floor, isfinite, fmax, isnan, nanmean, \
    arange, zeros_like, atleast_2d, array, cross, sign

from ..roadrunner.common import circle_circle_intersection_area
from ...orbits.taylor_z import vajs_from_paiew, find_contact_point, t14

d2sec = 24.*60.*60.

@njit
def lerpflux_multiband(t, fluxes, t0, dt):
    npb = fluxes.shape[0]
    x = (t-t0) / dt
    i = int(floor(x))
    fs = zeros(npb)
    if i < 0 or i > fluxes.shape[1]:
        fs[:] = inf
    else:
        a = x - i
        for ipb in range(npb):
            fs[ipb] = (1.-a)*fluxes[ipb, i] + a*fluxes[ipb, i+1]
    return fs


@njit
def lerpflux_singleband(t, ipb, fluxes, t0, dt):
    x = (t-t0) / dt
    i = int(floor(x))
    if i < 0 or i > fluxes.shape[1]:
        return inf
    else:
        a = x - i
        return (1.-a)*fluxes[ipb, i] + a*fluxes[ipb, i+1]


@njit
def planck(l, t):
    return 2.*h*c**2/l**5/(exp(h*c/(l*k*t)) - 1.)


@njit
def stellar_oblateness(w, rho):
    return 3.*w*w/(8.*G*pi*rho)


@njit
def z_s(x, y, r, f, sphi, cphi):
    x2, y2, r2 = x*x, y*y, r*r
    if x2 + y2 > r2:
        return nan
    else:
        sphi2, cphi2, f2 = sphi**2, cphi**2, f**2

        a = 1./(1. - f)**2
        d = (4.*y2*sphi2*cphi2*(a - 1.)**2- 4.*(cphi2 + a*sphi2)*(x2 + y2*(a*cphi2 + sphi2) - r2))
        if d >= 0.0:
            return (-2.*y*cphi*sphi*(a - 1.) + sqrt(d))/(2.*(cphi2 + a*sphi2))
        else:
            return nan


@njit
def mu_s(x, y, f, ci, si):
    """Calculates mu analytically.

    Calculates mu = sqrt(1 - z^2) = cos(theta), where z is the normalized distance from the centre
    of the stellar disk and theta is the foreshortening angle. Contributed by V. Bourrier.

    Parameters
    ----------
    x
      x position in the sky plane
    y
      y position in the sky plane
    f
      Stellar oblateness
    ci
      cos(i_star)
    si
      sin(i_star)

    Returns
    -------
    mu
    """
    g = 1.0-f
    g2  = g**2
    h = (1. - g2)
    qa = 1. - si**2 * h
    qb = 2.*y*ci*si*h
    qc = y**2 * si**2 * h + g2 * (x**2 + y**2 - 1.)
    det = qb**2 - 4*qa*qc
    if det != 0.0:
        nx2 = (g2*2*x)**2 / abs(det)
        ny2 = ((1./qa)*(-(ci*si*h) + 2*y*g2/sqrt(det)))**2
        nz2 = 1.
        mu = 1.0 / sqrt(nx2 + ny2 + nz2)
    else:
        mu = nan
    return mu


@njit
def z_and_mu_numerical_s(x, y, r, f, sphi, cphi):
    """Calculates z and mu accurately."""

    z = z_s(x, y, r, f, sphi, cphi)
    if isfinite(z):
        d1x = -sign(x) * 1e-5 * r
        d1z = z_s(x + d1x, y, r, f, sphi, cphi) - z
        d2y = -sign(y) * 1e-5 * r
        d2z = z_s(x, y + d2y, r, f, sphi, cphi) - z
        nx = - d1z * d2y
        ny = - d1x * d2z
        nz = d1x * d2y
        return z, abs(nz) / sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    else:
        return z, nan


@njit
def z_and_mu_s(x, y, r, f, sphi, cphi):
    """Calculates z and mu accurately."""

    z = z_s(x, y, r, f, sphi, cphi)
    if isfinite(z):
        return z, mu_s(x/r, y/r, f, -sphi, cphi)
    else:
        return z, nan


@njit
def z_v(xs, ys, r, f, sphi, cphi):
    npt = xs.size
    z = zeros(npt)

    sphi2, cphi2, f2, r2 = sphi**2, cphi**2, f**2, r**2
    a = 1./(1. - f)**2

    for i in range(npt):
        x2, y2 = xs[i]**2, ys[i]**2
        if x2 + y2 > r2:
            z[i] = nan
        else:
            d = (4.*y2*sphi2*cphi2*(a - 1.)**2 - 4.*(cphi2 + a*sphi2)*(x2 + y2*(a*cphi2 + sphi2) - r2))
            if d >= 0.0:
                z[i] = (-2.*ys[i]*cphi*sphi*(a - 1.) + sqrt(d))/(2.*(cphi2 + a*sphi2))
            else:
                z[i] = nan
    return z


@njit
def z_and_mu_v(xs, ys, r, f, sphi, cphi):
    npt = xs.size
    zs = zeros(npt)
    mus = zeros(npt)

    for i in range(npt):
        z, mu = z_and_mu_s(xs[i], ys[i], r, f, sphi, cphi)
        zs[i] = z
        mus[i] = mu
    return zs, mus


@njit
def luminosity_s(x, y, mstar, rstar, ostar, tpole, gpole, f, sphi, cphi, beta, ldc, ipb, ftable, t0, dt):
    dg = zeros(3)
    dc = zeros(3)

    z, mu = z_and_mu_s(x, y, rstar, f, sphi, cphi)
    if isnan(z):
        return nan
    else:
        dg[0] = x
        dg[1] = y*cphi + z*sphi
        dg[2] = -y*sphi + z*cphi

        dc[0] = dg[0]
        dc[2] = dg[2]

        # Direction vector lengths
        # ------------------------
        lg2 = dg[0]**2 + dg[1]**2 + dg[2]**2
        lg = sqrt(lg2)
        lc = sqrt(dc[0]**2 + dc[2]**2)

        # Normalize the direction vectors
        # -------------------------------
        dg /= lg
        dc /= lc

        gg = - G*mstar/lg2
        gc = ostar*ostar*lc

        dgg = gg*dg + gc*dc
        g = sqrt((dgg**2).sum())
        t = tpole*g**beta/gpole**beta

        return lerpflux_singleband(t, ipb, ftable, t0, dt) * (1. - ldc[ipb, 0] * (1. - mu) - ldc[ipb, 1] * (1. - mu) ** 2)


@njit
def luminosity_v(xs, ys, mstar, rstar, ostar, tpole, gpole, f, sphi, cphi, beta, ldc, ipb, ftable, t0, dt, accurate_mu):
    npt = xs.size
    l = zeros(npt)
    dg = zeros(3)
    dc = zeros(3)

    for i in range(npt):
        x, y = xs[i], ys[i]
        if accurate_mu:
            z, mu = z_and_mu_s(x, y, rstar, f, sphi, cphi)
        else:
            z = z_s(x, y, rstar, f, sphi, cphi)
            mu = z/sqrt((x**2 + y**2 + z**2))

        if isnan(z):
            l[i] = nan
        else:
            dg[0] = x
            dg[1] = y*cphi + z*sphi
            dg[2] = -y*sphi + z*cphi

            dc[0] = dg[0]
            dc[2] = dg[2]

            # Direction vector lengths
            # ------------------------
            lg2 = dg[0]**2 + dg[1]**2 + dg[2]**2
            lg = sqrt(lg2)
            lc = sqrt(dc[0]**2 + dc[2]**2)

            # Normalize the direction vectors
            # -------------------------------
            dg /= lg
            dc /= lc

            gg = - G*mstar/lg2
            gc = ostar*ostar*lc

            dgg = gg*dg + gc*dc
            g = sqrt((dgg**2).sum())
            t = tpole*g**beta / gpole**beta

            l[i] = lerpflux_singleband(t, ipb, ftable, t0, dt) * (1. - ldc[ipb, 0]*(1. - mu) - ldc[ipb, 1]*(1. - mu)**2)
    return l


@njit
def luminosity_v2(ps, normals, istar, mstar, rstar, ostar, tpole, gpole, beta, ldc, ipb, ftable, t0, dt):
    npt = ps.shape[0]
    l = zeros(npt)
    dc = zeros(3)

    vx = 0.0
    vy = -cos(istar)
    vz = -sin(istar)

    for i in range(npt):
        px, py, pz = ps[i] * rstar         # Position vector components
        nx, ny, nz = normals[i]            # Normal vector components

        mu =  vy*ny + vz*nz

        lp2 = (px**2 + py**2 + pz**2)      # Squared distance from center
        lc = sqrt(px**2 + pz**2)           # Centrifugal vector length
        cx, cz = px/lc, pz/lc              # Normalized centrifugal vector

        gg = -G * mstar / lp2              # Newtonian surface gravity component
        gc = ostar * ostar * lc            # Centrifugal surface gravity component

        gx = gg*nx + gc*cx                 # Surface gravity x component
        gy = gg*ny                         # Surface gravity y component
        gz = gg*nz + gc*cz                 # Surface gravity z component

        g = sqrt((gx**2 + gy**2 + gz**2))  # Surface gravity
        t = tpole*g**beta / gpole**beta    # Temperature [K]
        l[i] = lerpflux_singleband(t, ipb, ftable, t0, dt) # Thermal radiation
        l[i] *= (1.-ldc[ipb, 0]*(1.-mu) - ldc[ipb, 1]*(1.-mu)**2) # Quadratic limb darkening
    return l


@njit
def luminosity_s2(p, normal, istar, mstar, rstar, ostar, tpole, gpole, beta, ldc, ipb, ftable, t0, dt):

    vx = 0.0
    vy = -cos(istar)
    vz = -sin(istar)

    px, py, pz = p * rstar             # Position vector components
    nx, ny, nz = normal                # Normal vector components

    mu =  vy*ny + vz*nz

    lp2 = (px**2 + py**2 + pz**2)      # Squared distance from center
    lc = sqrt(px**2 + pz**2)           # Centrifugal vector length
    cx, cz = px/lc, pz/lc              # Normalized centrifugal vector

    gg = -G * mstar / lp2              # Newtionian surface gravity component
    gc = ostar * ostar * lc            # Centrifugal surface gravity component

    gx = gg*nx + gc*cx                 # Surface gravity x component
    gy = gg*ny                         # Surface gravity y component
    gz = gg*nz + gc*cz                 # Surface gravity z component

    g = sqrt((gx**2 + gy**2 + gz**2))  # Surface gravity
    t = tpole*g**beta / gpole**beta    # Temperature [K]
    l = lerpflux_singleband(t, ipb, ftable, t0, dt)  # Thermal radiation
    l *= (1.-ldc[ipb, 0]*(1.-mu) - ldc[ipb, 1]*(1.-mu)**2) # Quadratic limb darkening
    return l


def create_star_xy(res: int = 64):
    st = linspace(-1., 1., res)
    x, y = meshgrid(st, st)
    return st, x.ravel(), y.ravel()


def create_planet_xy(res: int = 6):
    dd = 2/(res + 1)
    dt = dd*arange(1, res + 1) - 1
    xs, ys = meshgrid(dt, dt)
    m = sqrt(xs**2 + ys**2) <= 1.
    return xs[m], ys[m]


@njit
def create_star_luminosity(res, x, y, mstar, rstar, ostar, tpole, gpole, f, sphi, cphi, beta, ldc, ftable, t0, dt, accurate_mu):
    l = zeros((ftable.shape[0], res, res))
    for ipb in range(ftable.shape[0]):
        l[ipb] = luminosity_v(x*rstar, y*rstar, mstar, rstar, ostar, tpole, gpole, f, sphi, cphi, beta, ldc, ipb, ftable, t0, dt, accurate_mu).reshape((res,res))
    return l


@njit(cache=False, fastmath=False)
def mean_luminosity(xc, yc, k, xs, ys, feff, lt, xt, yt):
    ns = xs.size
    rf = 1.0/(1.0 - feff)

    lsum = 0.0
    weight = 0.0
    for i in range(ns):
        x = xc + xs[i]*k
        y = (yc + ys[i]*k)*rf

        if x**2 + y**2 > 1.0:
            continue

        dx = xt[1] - xt[0]
        dy = yt[1] - yt[0]

        ix = int(floor((x - xt[0])/dx))
        ax1 = (x - xt[ix])/dx
        ax2 = 1.0 - ax1

        iy = int(floor((y - yt[0])/dy))
        ay1 = (y - yt[iy])/dy
        ay2 = 1.0 - ay1

        l = (  lt[iy,     ix    ]*ay2*ax2
             + lt[iy + 1, ix    ]*ay1*ax2
             + lt[iy,     ix + 1]*ay2*ax1
             + lt[iy + 1, ix + 1]*ay1*ax1)

        if isfinite(l):
            lsum += l
            weight += 1.

    if weight > 0.:
        return lsum/weight
    else:
        return nan


@njit
def mean_luminosity_under_planet(x, y, mstar, rstar, ostar, tpole, gpole, f, sphi, cphi, beta, ldc, ipb, ftable, t0, dt, accurate_mu):
    l = luminosity_v(x*rstar, y*rstar, mstar, rstar, ostar, tpole, gpole, f, sphi, cphi, beta, ldc, ipb, ftable, t0, dt, accurate_mu)
    return nanmean(l)


@njit
def calculate_luminosity_interpolation_table(res, k, xp, yp, sa, ca, y0, vx, vy, ax, ay, jx, jy, sx, sy,
                                             mstar, rstar, ostar, tpole, gpole, f, sphi, cphi, beta, ldc,
                                             ftable, t0, dt, accurate_mu):
    t1 = find_contact_point(k, 1, y0, vx, vy, ax, ay, jx, jy, sx, sy)
    t4 = find_contact_point(k, 4, y0, vx, vy, ax, ay, jx, jy, sx, sy)
    times = linspace(t1, t4, res)

    npb = ftable.shape[0]
    lt = zeros((npb, res))
    for ipb in range(npb):
        for i in range(lt.shape[1]):
            x, y = xy_taylor_st(times[i], sa, ca, y0, vx, vy, ax, ay, jx, jy, sx, sy)
            xs = x + k * xp
            ys = y + k * yp
            lt[ipb, i] = mean_luminosity_under_planet(xs, ys, mstar, rstar, ostar, tpole, gpole, f, sphi, cphi, beta, ldc,
                                                 ipb, ftable, t0, dt, accurate_mu)

        i = 0
        while isnan(lt[ipb, i]):
            i += 1

        ifill = lt[ipb, i]
        while i >= 0:
            lt[ipb, i] = ifill
            i -= 1

        i = lt.shape[1] - 1
        while isnan(lt[ipb, i]):
            i -= 1

        ifill = lt[ipb, i]
        while i < lt.shape[1]:
            lt[ipb, i] = ifill
            i += 1

    return times, lt


@njit(fastmath=True)
def xy_taylor_st(t, sa, ca, y0, vx, vy, ax, ay, jx, jy, sx, sy):
    t2 = t*t
    t3 = t2*t
    t4 = t3*t
    px =      vx*t + 0.5*ax*t2 + jx*t3/6.0 + sx*t4/24.
    py = y0 + vy*t + 0.5*ay*t2 + jy*t3/6.0 + sy*t4/24.

    x = ca*px - sa*py
    y = ca*py + sa*px

    return x, y


@njit(fastmath=True)
def xy_taylor_vt(ts, a, y0, vx, vy, ax, ay, jx, jy, sx, sy):
    npt = ts.size
    x, y = zeros(npt), zeros(npt)
    ca, sa = cos(a), sin(a)

    for i in range(npt):
        t = ts[i]
        t2 = t*t
        t3 = t2*t
        t4 = t3*t
        px =      vx*t + 0.5*ax*t2 + jx*t3/6.0 + sx*t4/24.
        py = y0 + vy*t + 0.5*ay*t2 + jy*t3/6.0 + sy*t4/24.

        x[i] = ca*px - sa*py
        y[i] = ca*py + sa*px

    return x, y


@njit
def find_contact_point_2d(k: float, point: int, az, feff, y0, vx, vy, ax, ay, jx, jy, sx, sy):
    if point == 1 or point == 2 or point == 12:
        s = -1.0
    else:
        s = 1.0

    if point == 1 or point == 4:
        zt = 1.0 + k
    elif point == 2 or point == 3:
        zt = 1.0 - k
    else:
        zt = 1.0

    t0 = 0.0
    t2 = s * 2.0 / vx
    t1 = 0.5 * t2

    sa, ca = sin(az), cos(az)

    x0, y0 = xy_taylor_st(t0, sa, ca, y0, vx, vy, ax, ay, jx, jy, sx, sy)
    x1, y1 = xy_taylor_st(t1, sa, ca, y0, vx, vy, ax, ay, jx, jy, sx, sy)
    z0 = sqrt(x0 ** 2 + (y0 / (1 - feff)) ** 2) - zt
    z1 = sqrt(x1 ** 2 + (y1 / (1 - feff)) ** 2) - zt

    i = 0
    while abs(t2 - t0) > 1e-6 and i < 100:
        if z0 * z1 < 0.0:
            t1, t2 = 0.5 * (t0 + t1), t1
            z2 = z1
            x1, y1 = xy_taylor_st(t1, sa, ca, y0, vx, vy, ax, ay, jx, jy, sx, sy)
            z1 = sqrt(x1 ** 2 + (y1 / (1 - feff)) ** 2) - zt
        else:
            t0, t1 = t1, 0.5 * (t1 + t2)
            z0 = z1
            x1, y1 = xy_taylor_st(t1, sa, ca, y0, vx, vy, ax, ay, jx, jy, sx, sy)
            z1 = sqrt(x1 ** 2 + (y1 / (1 - feff)) ** 2) - zt
        i += 1
    return t1


@njit
def oblate_model_s(t, k, t0, p, a, aa, i, e, w, ldc,
                   mstar, rstar, ostar, tpole, gpole,
                   f, feff, sphi, cphi, beta, ftable, teff0, dteff,
                   tres, ts, xs, ys, xp, yp,
                   lcids, pbids, nsamples, exptimes, npb, accurate_mu):
    y0, vx, vy, ax, ay, jx, jy, sx, sy = vajs_from_paiew(p, a, i, e, w)
    ldc = atleast_2d(ldc)

    sa, ca = sin(aa), cos(aa)
    half_window_width = 0.025 + 0.5 * t14(k[0], y0, vx, vy, ax, ay, jx, jy, sx, sy)

    npt = t.size
    flux = zeros(npt)
    tp, lp = calculate_luminosity_interpolation_table(tres, k[0], xp, yp, sa, ca,
                                                      y0, vx, vy, ax, ay, jx, jy, sx, sy,
                                                      mstar, rstar, ostar, tpole, gpole, f,
                                                      sphi, cphi, beta, ldc, ftable, teff0, dteff, accurate_mu)
    dtp = tp[1] - tp[0]

    ls = create_star_luminosity(ts.size, xs, ys, mstar, rstar, ostar, tpole, gpole,
                                f, sphi, cphi, beta, ldc, ftable, teff0, dteff, accurate_mu)

    astar = pi * (1. - feff)      # Area of an ellipse = pi * a * b, where a = 1 and b = (1 - feff)
    istar = zeros(npb)
    for ipb in range(npb):
        istar[ipb] = astar * nanmean(ls[ipb])

    for j in range(npt):
        epoch = floor((t[j] - t0 + 0.5*p)/p)
        tc = t[j] - (t0 + epoch*p)
        if abs(tc) > half_window_width:
            flux[j] = 1.0
        else:
            ilc = lcids[j]
            ipb = pbids[ilc]

            if k.size == 1:
                _k = k[0]
            else:
                _k = k[ipb]

            if isnan(_k) or isnan(a):
                flux[j] = inf
            else:
                for isample in range(1, nsamples[ilc] + 1):
                    time_offset = exptimes[ilc] * ((isample - 0.5) / nsamples[ilc] - 0.5)

                    to = tc + time_offset
                    it = int(floor((to - tp[0]) / dtp))
                    if it < 0:
                        it = 0
                        at = 0.0
                    elif it > lp.shape[1] - 2:
                        it = lp.shape[1] - 2
                        at = 1.0
                    else:
                        at = (to - tp[it]) / dtp
                    ml = (1.0 - at) * lp[ipb, it] + at * lp[ipb, it + 1]

                    x, y = xy_taylor_st(to, sa, ca, y0, vx, vy, ax, ay, jx, jy, sx, sy)

                    b = sqrt(x**2 + (y / (1. - feff))**2)
                    ia = circle_circle_intersection_area(1., _k, b)
                    flux[j] += (istar[ipb] - ml * ia) / istar[ipb]

                flux[j] /= nsamples[ilc]
    return flux


def map_osm(rstar, dstar, rperiod, phi):
    """
    Parameters
    ----------
    rstar : float
        Stellar radius [R_Sun]

    dstar : float
        Stellar density [g/cm^3]

    rperiod : float
        Stellar rotation period [days]

    phi : float
        Latitude of the point on the stellar surface [radians]

    Returns
    -------
    mstar : float
        Stellar mass [kg]

    omega : float
        Stellar rotation rate [rad/s]

    gpole : float
        Surface gravity at the pole [m/s^2]

    f : float
        Stellar oblateness

    feff : float
        Projected stellar oblateness

    """
    omega = 2*pi/(rperiod*d2sec)    # Stellar rotation rate [rad/s]
    dstar = 1e3*dstar                   # Stellar density       [kg/m^3]

    f = stellar_oblateness(omega, dstar)  # Stellar oblateness
    feff = 1 - sqrt((1 - f)**2*cos(phi)**2 + sin(phi)**2)  # Projected stellar oblateness
    mstar = dstar*4*pi/3*rstar**2*rstar*(1 - f)  # Stellar mass [kg]
    gpole = G*mstar/(rstar*(1 - f))**2  # Surface gravity at the pole  [m/s^2]
    return mstar, omega, gpole, f, feff