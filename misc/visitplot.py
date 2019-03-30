"""Functions to generate plots of the flow field with VisIt."""

import os
import sys
import yaml


def visit_check_version(version):
    # Check version of VisIt.
    script_version = '2.12.1'
    tested_versions = [script_version, '2.12.3']
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
            config_view = yaml.load(infile, Loader=yaml.FullLoader)
            config_view = config_view['View2DAtts']
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

    for i, state in enumerate(states):
        print('[state {}] Rendering and saving figure ...'.format(state))
        visit.SetTimeSliderState(state)

        if i == 0:
            visit.DrawPlots()

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
    visit.Close()
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
            config_view = yaml.load(infile, Loader=yaml.FullLoader)
            config_view = config_view['View3DAtts']
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

    for i, state in enumerate(states):
        print('[state {}] Rendering and saving figure ...'.format(state))
        visit.SetTimeSliderState(state)

        if i == 0:
            visit.DrawPlots()

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
    visit.Close()
    return


def visit_plot_qcrit_wx_3d(xdmf_dir,
                           wx_range=(-5.0, 5.0),
                           q_value=0.1,
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

    # Define some variables to get the q_crit and wx_cc.
    p_xdmf_path = os.path.join(str(xdmf_dir), 'p.xmf')
    visit.OpenDatabase(p_xdmf_path, 0)
    visit.DefineScalarExpression("operators/ConnectedComponents/p Grid", "cell_constant(<p Grid>, 0.)")
    visit.DefineCurveExpression("operators/DataBinning/1D/p Grid", "cell_constant(<p Grid>, 0)")
    visit.DefineScalarExpression("operators/DataBinning/2D/p Grid", "cell_constant(<p Grid>, 0)")
    visit.DefineScalarExpression("operators/DataBinning/3D/p Grid", "cell_constant(<p Grid>, 0)")
    visit.DefineScalarExpression("operators/Flux/p Grid", "cell_constant(<p Grid>, 0.)")
    visit.DefineCurveExpression("operators/Lineout/p", "cell_constant(<p>, 0.)")
    visit.DefineCurveExpression("operators/Lineout/time_derivative/p Grid_time", "cell_constant(time_derivative/p Grid_time, 0.)")
    visit.DefineCurveExpression("operators/Lineout/time_derivative/p Grid_lasttime", "cell_constant(time_derivative/p Grid_lasttime, 0.)")
    visit.DefineCurveExpression("operators/Lineout/time_derivative/p", "cell_constant(time_derivative/p, 0.)")
    visit.DefineScalarExpression("operators/ModelFit/model", "point_constant(<p Grid>, 0)")
    visit.DefineScalarExpression("operators/ModelFit/distance", "point_constant(<p Grid>, 0)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Sum/p", "cell_constant(<p>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Mean/p", "cell_constant(<p>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Variance/p", "cell_constant(<p>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Std. Dev./p", "cell_constant(<p>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Slope/p", "cell_constant(<p>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Residuals/p", "cell_constant(<p>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Sum/time_derivative/p Grid_time", "cell_constant(<time_derivative/p Grid_time>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Sum/time_derivative/p Grid_lasttime", "cell_constant(<time_derivative/p Grid_lasttime>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Sum/time_derivative/p", "cell_constant(<time_derivative/p>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Mean/time_derivative/p Grid_time", "cell_constant(<time_derivative/p Grid_time>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Mean/time_derivative/p Grid_lasttime", "cell_constant(<time_derivative/p Grid_lasttime>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Mean/time_derivative/p", "cell_constant(<time_derivative/p>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Variance/time_derivative/p Grid_time", "cell_constant(<time_derivative/p Grid_time>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Variance/time_derivative/p Grid_lasttime", "cell_constant(<time_derivative/p Grid_lasttime>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Variance/time_derivative/p", "cell_constant(<time_derivative/p>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Std. Dev./time_derivative/p Grid_time", "cell_constant(<time_derivative/p Grid_time>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Std. Dev./time_derivative/p Grid_lasttime", "cell_constant(<time_derivative/p Grid_lasttime>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Std. Dev./time_derivative/p", "cell_constant(<time_derivative/p>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Slope/time_derivative/p Grid_time", "cell_constant(<time_derivative/p Grid_time>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Slope/time_derivative/p Grid_lasttime", "cell_constant(<time_derivative/p Grid_lasttime>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Slope/time_derivative/p", "cell_constant(<time_derivative/p>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Residuals/time_derivative/p Grid_time", "cell_constant(<time_derivative/p Grid_time>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Residuals/time_derivative/p Grid_lasttime", "cell_constant(<time_derivative/p Grid_lasttime>, 0.)")
    visit.DefineScalarExpression("operators/StatisticalTrends/Residuals/time_derivative/p", "cell_constant(<time_derivative/p>, 0.)")
    visit.DefineVectorExpression("operators/SurfaceNormal/p Grid", "cell_constant(<p Grid>, 0.)")
    # Define cell-centered velocity vector field.
    ux_xdmf_path = os.path.join(str(xdmf_dir), 'u.xmf')
    uy_xdmf_path = os.path.join(str(xdmf_dir), 'v.xmf')
    uz_xdmf_path = os.path.join(str(xdmf_dir), 'w.xmf')
    vel_exp = ('{' +
               'pos_cmfe(<{}[0]id:u>, <p Grid>, 1.0),'.format(ux_xdmf_path) +
               'pos_cmfe(<{}[0]id:v>, <p Grid>, 0.0),'.format(uy_xdmf_path) +
               'pos_cmfe(<{}[0]id:w>, <p Grid>, 0.0)'.format(uz_xdmf_path) +
               '}')
    visit.DefineVectorExpression('velocity', vel_exp)
    # Define Q-criterion.
    qcrit_exp = ('q_criterion(' +
                 'gradient(velocity[0]),' +
                 'gradient(velocity[1]),' +
                 'gradient(velocity[2])' +
                 ')')
    visit.DefineScalarExpression('q_crit', qcrit_exp)
    # Define cell-centered streamwise vorticity.
    wx_xdmf_path = os.path.join(str(xdmf_dir), 'wx.xmf')
    wx_exp = 'pos_cmfe(<{}[0]id:wx>, <p Grid>, 0.0)'.format(wx_xdmf_path)
    visit.DefineScalarExpression('wx_cc', wx_exp)

    # Add a pseudocolor of the cell-centered streamwise vorticity.
    visit.AddPlot('Pseudocolor', 'wx_cc', 1, 1)
    PseudocolorAtts = visit.PseudocolorAttributes()
    PseudocolorAtts.minFlag = 1
    PseudocolorAtts.min = wx_range[0]
    PseudocolorAtts.maxFlag = 1
    PseudocolorAtts.max = wx_range[1]
    PseudocolorAtts.colorTableName = 'viridis'
    PseudocolorAtts.invertColorTable = 1
    PseudocolorAtts.opacityType = PseudocolorAtts.Constant
    PseudocolorAtts.opacity = 0.8
    PseudocolorAtts.legendFlag = 0
    visit.SetPlotOptions(PseudocolorAtts)

    # Add an isosurface of the Q-criterion.
    visit.AddOperator('Isosurface', 1)
    IsosurfaceAtts = visit.IsosurfaceAttributes()
    IsosurfaceAtts.variable = 'q_crit'
    IsosurfaceAtts.contourMethod = IsosurfaceAtts.Value
    IsosurfaceAtts.contourValue = (q_value)
    IsosurfaceAtts.scaling = IsosurfaceAtts.Linear
    visit.SetOperatorOptions(IsosurfaceAtts, 1)

    # Remove info about user, time, database, and legend.
    AnnotationAtts = visit.AnnotationAttributes()
    AnnotationAtts.userInfoFlag = 0
    AnnotationAtts.databaseInfoFlag = 0
    AnnotationAtts.timeInfoFlag = 0
    AnnotationAtts.legendInfoFlag = 0
    AnnotationAtts.axes3D.visible = 0
    AnnotationAtts.axes3D.triadFlag = 1
    AnnotationAtts.axes3D.bboxFlag = 0
    visit.SetAnnotationAttributes(AnnotationAtts)

    # Parse the 3D view configuration file.
    if config_view is not None:
        with open(str(config_view), 'r') as infile:
            config_view = yaml.load(infile, Loader=yaml.FullLoader)
            config_view = config_view['View3DAtts']
    # Set attributes of the view.
    View3DAtts = visit.View3DAttributes()
    for key, value in config_view.items():
        if type(value) is list:
            value = tuple(value)
        setattr(View3DAtts, key, value)
    visit.SetView3D(View3DAtts)

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

    for i, state in enumerate(states):
        print('[state {}] Rendering and saving figure ...'.format(state))
        visit.SetTimeSliderState(state)

        if i == 0:
            visit.DrawPlots()

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
    visit.CloseComputeEngine()
    visit.Close()
    return
