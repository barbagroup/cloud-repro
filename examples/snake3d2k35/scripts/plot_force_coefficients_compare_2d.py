"""Generate a figure of the force coefficients over time.

Compare the 3D force coefficients with the 2D ones.
Save the figure in the sub-folder `figures` of the simulation directory.
"""

import pathlib
from matplotlib import pyplot

import petibmpy


simudir = pathlib.Path(__file__).absolute().parents[1]

# Read 3D forces and convert to force coefficients.
filepath = simudir / 'output' / 'forces-0.txt'
t, fx, fy, fz = petibmpy.read_forces(filepath)
rho, u_inf = 1.0, 1.0  # density and freestream speed
dyn_pressure = 0.5 * rho * u_inf**2  # dynamic pressure
c = 1.0  # chord length
Lz = 3.2 * c  # spanwise length
coeff = 1 / (dyn_pressure * c * Lz)  # scaling factor for force coefficients
cd, cl, cz = petibmpy.get_force_coefficients(fx, fy, fz, coeff=coeff)
cd_avg, cl_avg = petibmpy.get_time_averaged_values(t, cd, cl,
                                                   limits=(40.0, 80.0))

# Read 2D forces and convert to force coefficients.
rootdir = simudir.parent
simudir2d = rootdir / 'snake2d2k35'
filepath = simudir2d / 'output' / 'forces-0.txt'
t2, fx2, fy2 = petibmpy.read_forces(filepath)
coeff = 1 / (dyn_pressure * c)
cd2, cl2 = petibmpy.get_force_coefficients(fx2, fy2, coeff=coeff)
cd2_avg, cl2_avg = petibmpy.get_time_averaged_values(t2, cd2, cl2,
                                                     limits=(40.0, 80.0))
cd_reldiff = (cd2_avg - cd_avg) / cd_avg * 100.0
cl_reldiff = (cl2_avg - cl_avg) / cl_avg * 100.0
print('Case\t<CD>\t\t<CL>')
print('3D\t{:.4f}\t\t{:.4f}'.format(cd_avg, cl_avg))
print('2D\t{:.4f} ({:.1f}%)\t{:.4f} ({:.1f}%)'
      .format(cd2_avg, cd_reldiff, cl2_avg, cl_reldiff))

# Plot force coefficients over time.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.plot(t, cd, label='$C_D$ (3D)')
ax.plot(t, cl, label='$C_L$ (3D)')
ax.plot(t2, cd2, label='$C_D$ (2D)', 
        color='black', linewidth=0.75, linestyle='--')
ax.plot(t2, cl2, label='$C_L$ (2D)',
        color='black', linewidth=0.75, linestyle='-')
ax.legend(ncol=2, frameon=False, prop={'size': 14})
ax.set_xlim(0.0, 80.0)
ax.set_ylim(0.55, 3.5)
fig.tight_layout()

# Save figure as PNG file.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'forceCoefficientsCompare2D.pdf'
fig.savefig(str(filepath), dpi=300)
