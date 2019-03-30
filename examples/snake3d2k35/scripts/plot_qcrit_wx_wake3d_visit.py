"""Plot the isosurfaces of the Q-criterion at save time steps.

The isosurfaces are colored with the streamwise vorticity.
"""

import numpy
import os
import pathlib
import sys

scriptdir = pathlib.Path(__file__).absolute().parents[3] / 'misc'
if scriptdir not in sys.path:
    sys.path.insert(0, str(scriptdir))
from visitplot import *


simudir = pathlib.Path(__file__).absolute().parents[1]
xdmfdir = simudir / 'output'
config_view = simudir / 'scripts' / 'visit_view3d.yaml'
figdir = simudir / 'figures'
prefix = 'qcrit_wx_wake3d_'

visit_plot_qcrit_wx_3d(xdmfdir,
                       wx_range=(-5.0, 5.0),
                       q_value=1.0,
                       config_view=config_view,
                       out_dir=figdir, out_prefix=prefix,
                       figsize=(880, 372),
                       visit_dir=os.environ.get('VISIT_DIR'),
                       state=20)
