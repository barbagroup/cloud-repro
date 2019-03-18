"""Generate a figure of the drag and lift force coefficients over time.

Save the figure in the sub-folder `figures` of the simulation directory.
"""

import sys
import pathlib
from matplotlib import pyplot

import petibmpy


simudir = pathlib.Path(__file__).absolute().parents[1]

filepath = simudir / 'output' / 'forces-0.txt'
t, fx, fy = petibmpy.read_forces(filepath)
cd, cl = petibmpy.get_force_coefficients(fx, fy, coeff=2.0)

pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.grid()
ax.plot(t, cd, label='$C_D$')
ax.plot(t, cl, label='$C_L$')
ax.legend(ncol=2)
ax.set_xlim(t[0], t[-1])
ax.set_ylim(0.0, 3.0)
fig.tight_layout()

figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'forceCoefficients.png'
fig.savefig(str(filepath), dpi=300)
