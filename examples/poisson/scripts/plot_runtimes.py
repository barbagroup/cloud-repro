"""Plot the time-to-solution versus the number of nodes."""

import pathlib
from matplotlib import pyplot, gridspec
import numpy


def get_filepaths(casedir, prefix='stdout_run', suffix='.txt', niter=5):
    """Get the file paths with data to read.

    Parameters
    ----------
    casedir : pathlib.Path object
        Directory that contains the files to read.
    prefix : string (optional)
        Common prefix of the file names; default: 'stdout_run'.
    suffix : string (optional)
        Common suffix of the file names; default: '.txt'.
    niter : integer (optional)
        Number of repeated runs (i.e., number of files to read).

    Returns
    -------
    filepaths : list of pathlib.Path objects
        The file paths.

    """
    filepaths = [casedir / (prefix + str(i + 1) + suffix)
                 for i in range(niter)]
    return filepaths


def amgxwrapper_poisson_read_runtimes(*filepaths):
    """Read the runtimes to solve the system for multiple runs.

    Parameters
    ----------
    filepaths : tuple of strings or pathlib.Path objects
        Path of the files to read.

    Returns
    -------
    runtimes : list of floats
        The runtimes.

    """
    runtimes = []
    for filepath in filepaths:
        with open(filepath, 'r') as infile:
            prev_line = ''
            for line in infile:
                if 'Solve Time:' in line:
                    if not prev_line.startswith('Warm-up'):
                        runtime = float(line.split(' ')[-1])
                        runtimes.append(runtime)
                prev_line = line
    return runtimes


def amgxwrapper_poisson_read_iterations(filepath):
    """Read the number of iterations to solve the system.

    Parameters
    ----------
    filepath : string or pathlib.Path object
        Path of the file to read.

    Returns
    -------
    nites : integer
        The number of iterations.

    """
    with open(filepath, 'r') as infile:
        for i, line in enumerate(infile):
            if 'Iterations' in line:
                nites = int(line.split(' ')[-1])
                break
    return nites


def get_runtime_stats(runtimes, scale=1.0):
    """Get the smalest, biggest, and mean runtimes of the series.

    Parameters
    ----------
    runtimes : list of floats
        The runtimes of the series.
    scale : float (optional)
        A scale coefficient; default: 1.0.

    Returns
    -------
    (min, max, mean) : tuple of 3 floats
        The smallest, biggest, and mean runtimes.

    """
    return (min(runtimes) * scale,
            max(runtimes) * scale,
            numpy.mean(runtimes) * scale)


def store_runtime_stats(data, nodes, stats):
    """Store the runtime stats in a dictionary.

    Parameters
    ----------
    data : dictionary
        Runtime data of the series.
    nodes : integer
        Number of nodes used for the series.
    stats : tuple or list of 3 floats
        Smallest, biggest, and mean runtimes of the series.

    """
    data['nodes'].append(nodes)
    data['min'].append(stats[0])
    data['max'].append(stats[1])
    data['means'].append(stats[2])
    return data


def gather_arrays(data, keys=['nodes', 'min', 'max', 'means']):
    """Gather data items into tuple.

    Parameters
    ----------
    data : dictionary
        Dictionary with the runtime data.
    keys : list of strings (optional)
        Disctionary keys to consider in the tuple;
        default: "['nodes', 'min', 'max', 'means']".

    Returns
    -------
    res : tuple of lists
        Data gathered into a tuple.

    """
    for key, value in data.items():
        data[key] = numpy.array(value)
    return tuple(data[key] for key in keys)


rootdir = pathlib.Path(__file__).absolute().parents[1]


data = {'Colonial One': {}, 'Azure': {}}
# Get runtimes data for PETSc runs on Colonial One.
nodes = [1, 2, 4, 8]
subdata = {'nodes': [], 'min': [], 'max': [], 'means': []}
for n in nodes:
    casedir = rootdir / f'colonialone/petsc/{n:0>2}_short/output'
    filepaths = get_filepaths(casedir)
    runtimes = amgxwrapper_poisson_read_runtimes(*filepaths)
    store_runtime_stats(subdata, n, get_runtime_stats(runtimes))
data['Colonial One']['PETSc'] = gather_arrays(subdata)
# Get runtimes data for AmgX runs on Colonial One.
nodes = [1, 2, 4, 8]
subdata = {'nodes': [], 'min': [], 'max': [], 'means': []}
for n in nodes:
    casedir = rootdir / f'colonialone/amgx/{n:0>2}_ivygpu/output'
    filepaths = get_filepaths(casedir)
    runtimes = amgxwrapper_poisson_read_runtimes(*filepaths)
    nites = amgxwrapper_poisson_read_iterations(filepaths[0])
    store_runtime_stats(subdata, n, get_runtime_stats(runtimes,
                                                      scale=1.0 / nites))
data['Colonial One']['AmgX'] = gather_arrays(subdata)
# Get runtimes data for PETSc runs on Azure.
nodes = [1, 2, 4, 8]
subdata = {'nodes': [], 'min': [], 'max': [], 'means': []}
for n in nodes:
    casedir = rootdir / f'azure/petsc/{n:0>2}_h16r/output'
    filepaths = get_filepaths(casedir)
    runtimes = amgxwrapper_poisson_read_runtimes(*filepaths)
    store_runtime_stats(subdata, n, get_runtime_stats(runtimes))
data['Azure']['PETSc'] = gather_arrays(subdata)
# Get runtimes data for AmgX runs on Azure.
nodes = [1, 2, 4, 8]
subdata = {'nodes': [], 'min': [], 'max': [], 'means': []}
for n in nodes:
    casedir = rootdir / f'azure/amgx/{n:0>2}_nc24r/output'
    filepaths = get_filepaths(casedir)
    runtimes = amgxwrapper_poisson_read_runtimes(*filepaths)
    nites = amgxwrapper_poisson_read_iterations(filepaths[0])
    store_runtime_stats(subdata, n, get_runtime_stats(runtimes,
                                                      scale=1.0 / nites))
data['Azure']['AmgX'] = gather_arrays(subdata)
# Get runtimes data for AmgX runs on Azure.
nodes = [1, 2, 4, 8]
subdata = {'nodes': [], 'min': [], 'max': [], 'means': []}
for n in nodes:
    casedir = rootdir / f'azure/amgx/larger/{n:0>2}_nc24r/output'
    filepaths = get_filepaths(casedir)
    runtimes = amgxwrapper_poisson_read_runtimes(*filepaths)
    nites = amgxwrapper_poisson_read_iterations(filepaths[0])
    store_runtime_stats(subdata, n, get_runtime_stats(runtimes,
                                                      scale=1.0 / nites))
data['Azure']['AmgX-larger'] = gather_arrays(subdata)

# Create Matplotlib figures.
pyplot.rc('font', family='serif', size=14)
fig = pyplot.figure(figsize=(6.0, 6.0))
gs = gridspec.GridSpec(nrows=2, ncols=2, height_ratios=[2, 1])

# Plot time-to-solution versus number of nodes for PETSc runs.
ax1 = fig.add_subplot(gs[0, :])
ax1.text(numpy.log2(1.0), 2.5, 'PETSc')
ax1.set_xlabel('Number of nodes')
ax1.set_ylabel('Time (s)')
# Colonial One runs.
nodes, mins, maxs, means = data['Colonial One']['PETSc']
ax1.plot(numpy.log2(nodes), means, label='Colonial One', color='C0')
ax1.errorbar(numpy.log2(nodes), means,
             [means - mins, maxs - means],
             fmt='k', linewidth=0, ecolor='black', elinewidth=2,
             capthick=2, capsize=4, barsabove=True)
# Azure runs.
nodes, mins, maxs, means = data['Azure']['PETSc']
ax1.plot(numpy.log2(nodes), means, label='Azure', color='C1')
ax1.errorbar(numpy.log2(nodes), means,
             [means - mins, maxs - means],
             fmt='k', linewidth=0, ecolor='black', elinewidth=2,
             capthick=2, capsize=4, barsabove=True)
ax1.legend(frameon=False)
ax1.tick_params(axis='both')
ax1.set_xticks(numpy.log2([1, 2, 4, 8]))
ax1.set_xticklabels([1, 2, 4, 8])
ax1.set_ylim(0.0, 25.0)
ax1.set_yticks([0.0, 5.0, 10.0, 15.0, 20.0, 25.0])
ax1.set_yticklabels([0, 5, 10, 15, 20, 25])

# Plot time-to-solution versus number of nodes for AmgX runs.
ax2 = fig.add_subplot(gs[1, 0])
ax2.text(numpy.log2(1.0), 0.005, 'AmgX')
ax2.set_xlabel('Number of nodes')
ax2.set_ylabel('Time (s)')
nodes, mins, maxs, means = data['Colonial One']['AmgX']
ax2.plot(numpy.log2(nodes), means, label='Colonial One', color='C0')
ax2.errorbar(numpy.log2(nodes), means,
             [means - mins, maxs - means],
             fmt='k', linewidth=0, ecolor='black', elinewidth=2,
             capthick=2, capsize=4, barsabove=True)
nodes, mins, maxs, means = data['Azure']['AmgX']
ax2.plot(numpy.log2(nodes), means, label='Azure', color='C1')
ax2.errorbar(numpy.log2(nodes), means,
             [means - mins, maxs - means],
             fmt='k', linewidth=0, ecolor='black', elinewidth=2,
             capthick=2, capsize=4, barsabove=True)
ax2.tick_params(axis='both')
ax2.set_xticks(numpy.log2([1, 2, 4, 8]))
ax2.set_xticklabels([1, 2, 4, 8])
ax2.set_ylim(0.0, 0.05)
ax2.set_yticks([0.0, 0.025, 0.05])
ax2.set_yticklabels([0.0, 0.025, 0.05])

# Plot time-to-solution versus number of nodes for AmgX larger runs (Azure).
ax3 = fig.add_subplot(gs[1, 1])
ax3.text(numpy.log2(1.0), 0.02, 'AmgX')
ax3.set_xlabel('Number of nodes')
ax3.set_ylabel('Time (s)')
nodes, mins, maxs, means = data['Azure']['AmgX-larger']
ax3.plot(numpy.log2(nodes), means, label='Azure', color='C1')
ax3.errorbar(numpy.log2(nodes), means,
             [means - mins, maxs - means],
             fmt='k', linewidth=0, ecolor='black', elinewidth=2,
             capthick=2, capsize=4, barsabove=True)
ax3.tick_params(axis='both')
ax3.set_xticks(numpy.log2([1, 2, 4, 8]))
ax3.set_xticklabels([1, 2, 4, 8])
ax3.set_ylim(0.0, 0.2)
ax3.set_yticks([0.0, 0.1, 0.2])
ax3.set_yticklabels([0.0, 0.1, 0.2])

# Save the figure.
figdir = rootdir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'poisson_time_vs_nodes.pdf'
fig.tight_layout()
fig.savefig(str(filepath), dpi=300, bbox_inches='tight')

pyplot.show()
