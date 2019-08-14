"""Module with functions for aerodynamic forces."""

import pathlib
import numpy


def read_forces(*filepaths):
    """Read PetIBM forces from given file(s).

    If multiple files are provided, the histories are concatenated.
    Parameters
    ----------
    filepaths : tuple of pathlib.Path objects or strings
        Path of the files to load the history from.

    Returns
    -------
    data : numpy.ndarray
        Time followed by the forces in the x, y, and z directions.

    """
    if type(filepaths) in [str, pathlib.Path]:
        filepaths = [filepaths]
    for i, filepath in enumerate(filepaths):
        with open(filepath, 'r') as infile:
            subdata = numpy.loadtxt(infile, unpack=True)
        if i == 0:
            data = subdata
        else:
            data = numpy.concatenate((data, subdata), axis=1)
        _, mask = numpy.unique(data[0], return_index=True)
    return numpy.array([subdata[mask] for subdata in data])


def get_force_coefficients(*forces, coeff=1.0):
    """Convert forces to force coefficients.

    Parameters
    ----------
    forces : tuple of numpy.ndarray objects
        The forces.
    coeff : float (optional)
        The scaling coefficient; default: 1.0.

    Returns
    -------
    force_coeffs : tuple of numpy.ndarray objects
        The force coefficients.

    """
    force_coeffs = (coeff * f for f in forces)
    return force_coeffs


def get_time_averaged_values(t, *forces, limits=(-numpy.infty, numpy.infty)):
    """Compute the time-averaged values.

    Parameters
    ----------
    t : numpy.ndarray object
        The time values.
    forces : tuple of numpy.ndarray objects
        The forces (or force coefficients).
    limits : tuple of 2 floats (optional)
        Time limits used to compute the mean; default: (-inf, +inf).

    Returns
    -------
    means : tuple of floats
        The time-averaged values.

    """
    mask = (t >= limits[0]) & (t <= limits[1])
    means = (numpy.mean(f[mask]) for f in forces)
    return means
