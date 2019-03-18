"""Generate figures of the 2D pseudocolor of the 2D vorticity field."""

import os
import sys
import pathlib

root_dir = pathlib.Path(__file__).absolute().parents[3]
scripts_dir = root_dir / 'misc'
if root_dir not in sys.path:
    sys.path.insert(0, str(scripts_dir))
from visitplot import *


simudir = pathlib.Path(__file__).absolute().parents[1]
xdmfpath = simudir / 'output' / 'postprocessing' / 'wz' / 'wz.xmf'
name = 'wz'
config_view = simudir / 'scripts' / 'visit_view2d.yaml'
curve2dpath = simudir / 'output' / 'snake2d35.curve'
figdir = simudir / 'figures'
prefix = 'wz_wake2d_'

visit_plot_pseudocolor_2d(xdmfpath, name,
                          value_range=(-5.0, 5.0),
                          curve2d_paths=[curve2dpath],
                          config_view=config_view,
                          out_dir=figdir, out_prefix=prefix,
                          figsize=(1024, 1024),
                          visit_dir=os.environ.get('VISIT_DIR'))
