"""
Functions to generate plots of the flow field with VisIt.
"""

import os
import sys
import yaml


def visit_check_version(version):
    # Check version of VisIt.
    script_version = '2.12.1'
    tested_versions = [script_version, '2.13.2']
    print('VisIt version: {}\n'.format(version))
    if version not in tested_versions:
        print('[warning] You are using VisIt-{}.'.format(version))
        print('[warning] This script was created with VisIt-{}.'
              .format(script_version))
        print('[warning] This script was tested with versions: {}.'
              .format(tested_versions))
        print('[warning] It may not work as expected')
    return


def visit_plot_pseudocolor_2d(xdmf_path, name,
                              value_range=(-5.0, 5.0),
                              curve2d_paths=None,
                              config_view=None,
                              out_dir=os.getcwd(), out_prefix='wake2d_',
                              figsize=(1024, 1024),
                              visit_dir=None, visit_arch='linux-x86_64',
                              state=None, states=None,
                              states_range=[0, None, 1]):
    # Import VisIt package.
    if visit_dir is None:
        visit_dir = os.environ.get('VISIT_DIR')
        if visit_dir is None:
            raise ValueError('Provide VisIt installation path or '
                             'set env variable VISIT_DIR')
    sys.path.append(os.path.join(visit_dir, visit_arch,
                    'lib', 'site-packages'))
    import visit

    visit.LaunchNowin()

    # Check version of VisIt.
    visit_check_version(visit.Version())

    # Create database correlation with optional Curve2D files.
    num_bodies = 0
    databases = [str(xdmf_path)]
    if curve2d_paths is not None:
        num_bodies = len(curve2d_paths)
        databases = [str(path) for path in curve2d_paths]
        databases.append(str(xdmf_path))
    visit.CreateDatabaseCorrelation('common', databases[num_bodies:], 0)

    # Open the file with the coordinates of the immersed boundary.
    if num_bodies > 0:
        for i in range(num_bodies):
            visit.OpenDatabase(databases[i], 0)
            # Add plot the mesh points.
            visit.AddPlot('Curve', 'curve', 1, 1)
            # Set attributes of the curve.
            CurveAtts = visit.CurveAttributes()
            CurveAtts.lineWidth = 1
            CurveAtts.curveColorSource = CurveAtts.Custom
            CurveAtts.curveColor = (0, 0, 0, 255)
            CurveAtts.showLegend = 0
            CurveAtts.showLabels = 0
            visit.SetPlotOptions(CurveAtts)

    # Open the XMF file for the spanwise-averaged z-component of the vorticity.
    visit.OpenDatabase(databases[-1], 0)
    # Add a pseudocolor plot of the scalar field.
    visit.AddPlot('Pseudocolor', name, 1, 1)
    # Set attributes of the pseudocolor.
    PseudocolorAtts = visit.PseudocolorAttributes()
    PseudocolorAtts.minFlag = 1
    PseudocolorAtts.min = value_range[0]
    PseudocolorAtts.maxFlag = 1
    PseudocolorAtts.max = value_range[1]
    PseudocolorAtts.colorTableName = 'viridis'
    visit.SetPlotOptions(PseudocolorAtts)

    # Parse the 2D view configuration file.
    if config_view is not None:
        with open(str(config_view), 'r') as infile:
            config_view = yaml.load(infile)['View2DAtts']
    # Set attributes of the view.
    View2DAtts = visit.View2DAttributes()
    for key, value in config_view.items():
        if type(value) is list:
            value = tuple(value)
        setattr(View2DAtts, key, value)
    visit.SetView2D(View2DAtts)

    # Remove time and user info.
    AnnotationAtts = visit.AnnotationAttributes()
    AnnotationAtts.userInfoFlag = 0
    AnnotationAtts.timeInfoFlag = 1
    visit.SetAnnotationAttributes(AnnotationAtts)

    visit.DrawPlots()
    visit.SetActiveWindow(1)

    visit.Source(os.path.join(visit_dir, visit_arch, 'bin', 'makemovie.py'))
    visit.ToggleCameraViewMode()

    # Create output directory if necessary.
    if not os.path.isdir(str(out_dir)):
        os.makedirs(str(out_dir))

    # Loop over the states to render and save the plots.
    if state is not None:
        states = [state]
    elif states is None:
        if states_range[1] is None:
            states_range[1] = visit.TimeSliderGetNStates()
        else:
            states_range[1] += 1
        states = range(*states_range)

    for state in states:
        print('[state {}] Rendering and saving figure ...'.format(state))
        visit.SetTimeSliderState(state)

        RenderingAtts = visit.RenderingAttributes()
        visit.SetRenderingAttributes(RenderingAtts)

        SaveWindowAtts = visit.SaveWindowAttributes()
        SaveWindowAtts.outputToCurrentDirectory = 0
        SaveWindowAtts.outputDirectory = str(out_dir)
        SaveWindowAtts.fileName = '{}{:0>4}'.format(out_prefix, state)
        SaveWindowAtts.family = 0
        SaveWindowAtts.format = SaveWindowAtts.PNG
        SaveWindowAtts.width = figsize[0]
        SaveWindowAtts.height = figsize[1]
        SaveWindowAtts.quality = 100
        SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
        visit.SetSaveWindowAttributes(SaveWindowAtts)

        visit.SaveWindow()

    os.remove('visitlog.py')
    sys.exit(0)
    return


def visit_plot_contour_3d(xdmf_path, name,
                          value_range=(-5.0, 5.0),
                          p3d_paths=None,
                          config_view=None,
                          out_dir=os.getcwd(), out_prefix='wake3d_',
                          figsize=(1024, 1024),
                          visit_dir=None, visit_arch='linux-x86_64',
                          state=None, states=None,
                          states_range=[0, None, 1]):
    # Import VisIt package.
    if visit_dir is None:
        visit_dir = os.environ.get('VISIT_DIR')
        if visit_dir is None:
            raise ValueError('Provide VisIt installation path or '
                             'set env variable VISIT_DIR')
    sys.path.append(os.path.join(visit_dir, visit_arch,
                    'lib', 'site-packages'))
    import visit

    visit.LaunchNowin()

    # Check version of VisIt.
    visit_check_version(visit.Version())

    # Create database correlation with optional Point3D files.
    num_bodies = 0
    databases = [str(xdmf_path)]
    if p3d_paths is not None:
        num_bodies = len(p3d_paths)
        databases = [str(path) for path in p3d_paths]
        databases.append(str(xdmf_path))
    visit.CreateDatabaseCorrelation('common', databases[num_bodies:], 0)

    # Open the file with the coordinates of the immersed boundary.
    if num_bodies > 0:
        for i in range(num_bodies):
            visit.OpenDatabase(databases[i], 0, 'Point3D_1.0')
            # Add plot the mesh points.
            visit.AddPlot('Mesh', 'points', 1, 1)
            # Set attributes of the mesh plot.
            MeshAtts = visit.MeshAttributes()
            MeshAtts.legendFlag = 0
            MeshAtts.meshColor = (255, 204, 0, 1.0 * 255)
            MeshAtts.meshColorSource = MeshAtts.MeshCustom
            MeshAtts.pointSize = 0.05
            MeshAtts.pointType = MeshAtts.Point
            MeshAtts.pointSizePixels = 2
            MeshAtts.opacity = 1
            visit.SetPlotOptions(MeshAtts)

    # Open the XMF file for the z-component of the vorticity.
    visit.OpenDatabase(databases[-1], 0)
    # Add the plot of the contour of the z-component of the vorticity.
    visit.AddPlot('Contour', name, 1, 1)
    # Set attributes of the contour.
    ContourAtts = visit.ContourAttributes()
    ContourAtts.contourNLevels = 2
    ContourAtts.SetMultiColor(0, (0, 51, 102, 0.6 * 255))
    ContourAtts.SetMultiColor(1, (255, 0, 0, 0.6 * 255))
    ContourAtts.legendFlag = 1
    ContourAtts.minFlag = 1
    ContourAtts.maxFlag = 1
    ContourAtts.min = value_range[0]
    ContourAtts.max = value_range[1]
    visit.SetPlotOptions(ContourAtts)

    # Parse the 3D view configuration file.
    if config_view is not None:
        with open(str(config_view), 'r') as infile:
            config_view = yaml.load(infile)['View3DAtts']
    # Set attributes of the view.
    View3DAtts = visit.View3DAttributes()
    for key, value in config_view.items():
        if type(value) is list:
            value = tuple(value)
        setattr(View3DAtts, key, value)
    visit.SetView3D(View3DAtts)

    # Remove time and user info.
    AnnotationAtts = visit.AnnotationAttributes()
    AnnotationAtts.userInfoFlag = 0
    AnnotationAtts.timeInfoFlag = 0
    AnnotationAtts.axes3D.visible = 0
    AnnotationAtts.axes3D.triadFlag = 1
    AnnotationAtts.axes3D.bboxFlag = 0
    visit.SetAnnotationAttributes(AnnotationAtts)

    visit.DrawPlots()
    visit.SetActiveWindow(1)

    visit.Source(os.path.join(visit_dir, visit_arch, 'bin', 'makemovie.py'))
    visit.ToggleCameraViewMode()

    # Create output directory if necessary.
    if not os.path.isdir(str(out_dir)):
        os.makedirs(str(out_dir))

    # Loop over the states to render and save the plots.
    if state is not None:
        states = [state]
    elif states is None:
        if states_range[1] is None:
            states_range[1] = visit.TimeSliderGetNStates()
        else:
            states_range[1] += 1
        states = range(*states_range)

    for state in states:
        print('[state {}] Rendering and saving figure ...'.format(state))
        visit.SetTimeSliderState(state)

        RenderingAtts = visit.RenderingAttributes()
        visit.SetRenderingAttributes(RenderingAtts)

        SaveWindowAtts = visit.SaveWindowAttributes()
        SaveWindowAtts.outputToCurrentDirectory = 0
        SaveWindowAtts.outputDirectory = str(out_dir)
        SaveWindowAtts.fileName = '{}{:0>4}'.format(out_prefix, state)
        SaveWindowAtts.family = 0
        SaveWindowAtts.format = SaveWindowAtts.PNG
        SaveWindowAtts.width = figsize[0]
        SaveWindowAtts.height = figsize[1]
        SaveWindowAtts.quality = 100
        SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint
        visit.SetSaveWindowAttributes(SaveWindowAtts)

        visit.SaveWindow()

    os.remove('visitlog.py')
    sys.exit(0)
    return
