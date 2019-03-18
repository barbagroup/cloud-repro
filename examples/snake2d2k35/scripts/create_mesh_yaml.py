"""Generate the YAML node "mesh" with details of the Cartesian grid."""

import sys
import pathlib
import numpy
from matplotlib import pyplot

import petibmpy


# Info about the 2D structured Cartesian grid.
width = 0.004  # minimum grid spacing in the x- and y- directions
ratio = 1.01  # stretching ratio
info = [{'direction': 'x', 'start': -15.0,
         'subDomains': [{'end': -0.52,
                         'width': width,
                         'stretchRatio': ratio,
                         'reverse': True,
                         'precision': 2},
                        {'end': 3.48,
                         'width': width,
                         'stretchRatio': 1.0},
                        {'end': 15.0,
                         'width': width,
                         'stretchRatio': ratio,
                         'precision': 2}]},
        {'direction': 'y', 'start': -15.0,
         'subDomains': [{'end': -2.0,
                         'width': width,
                         'stretchRatio': ratio,
                         'reverse': True,
                         'precision': 2},
                        {'end': 2.0,
                         'width': width,
                         'stretchRatio': 1.0},
                        {'end': 15.0,
                         'width': width,
                         'stretchRatio': ratio,
                         'precision': 2}]}]

mesh = petibmpy.CartesianStructuredMesh()
mesh.create(info)
mesh.print_parameters()

simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'mesh.yaml'
mesh.write_yaml_file(filepath)
