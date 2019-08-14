"""Plots the latency and the bandwidth results from the OSU benchmark."""

import numpy
from matplotlib import pyplot
import pathlib
import re


def read_latency_bandwidth_data(filepath):
    """Read the latency or bandwidth data from a file.

    Parameters
    ----------
    filepath : string of pathlib.Path object
        File path with data to read.

    Returns
    -------
    sizes : list of integers
        Size of the messages.
    measures : list of floats
        Measure of the latency or bandwidth.

    """
    sizes, measures = [], []
    with open(filepath, 'r') as infile:
        for line in infile:
            if re.match(r'^\d+.*$', line):
                size, measure = line.strip().split()
                sizes.append(int(size))
                measures.append(float(measure))
    return sizes, measures


def get_latency_bandwidth_data(datadir, iterator, prefix='', suffix=''):
    """Read and average the latency or bandwidth over multiple runs.

    Parameters
    ----------
    datadir : pathlib.Path object
        Directory with latency or bandwidth data.
    iterator : range
        Range to iterate over.
    prefix : string, optional
        Prefix of the file to read; default: ''.
    suffix : string, optional
        Suffix of the file to read; default: ''.

    Returns
    -------
    size : list of integers
        Size of the messages.
    data : numpy.ndarray
        Latency or bandwidth values averaged over the runs.

    """
    data = []
    for i in iterator:
        filepath = datadir / (prefix + str(i) + suffix)
        # Read latency or bandwidth for a single run.
        size, subdata = read_latency_bandwidth_data(filepath)
        data.append(subdata)
    # Average the measure over the runs.
    data = numpy.mean(data, axis=0)
    print(data)
    return size, data


rootdir = pathlib.Path(__file__).absolute().parents[1]

data = {}

# Get the latency and bandwidth results for Azure runs.
label = 'Azure Batch (NC24r)'
data[label] = {}
datadir = rootdir / 'azure' / 'output'
sizes, latencies = get_latency_bandwidth_data(datadir, range(1, 6),
                                              prefix='stdout_latency_run',
                                              suffix='.txt')
data[label]['latency'] = {'sizes': sizes, 'values': latencies}
sizes, bandwidths = get_latency_bandwidth_data(datadir, range(1, 6),
                                               prefix='stdout_bandwidth_run',
                                               suffix='.txt')
data[label]['bandwidth'] = {'sizes': sizes, 'values': bandwidths}
data[label]['kwargs'] = dict(color='C0', linestyle='-',
                             marker='o', markersize=6)

# Get the latency and bandwidth results for Colonial One runs.
label = 'Colonial One (Intel MPI)'
data[label] = {}
datadir = rootdir / 'colonialone' / 'output'
sizes, latencies = get_latency_bandwidth_data(datadir, range(1, 6),
                                              prefix='stdout_latency_run',
                                              suffix='.txt')
data[label]['latency'] = {'sizes': sizes, 'values': latencies}
sizes, bandwidths = get_latency_bandwidth_data(datadir, range(1, 6),
                                               prefix='stdout_bandwidth_run',
                                               suffix='.txt')
data[label]['bandwidth'] = {'sizes': sizes, 'values': bandwidths}
data[label]['kwargs'] = dict(color='C1', linestyle='--',
                             marker='o', markersize=6)

# Get the latency and bandwidth results for Colonial One runs with Intel MPI.
label = 'Colonial One (OpenMPI)'
data[label] = {}
datadir = rootdir / 'colonialone-openmpi' / 'output'
sizes, latencies = get_latency_bandwidth_data(datadir, range(5),
                                              prefix='stdout_latency_run',
                                              suffix='.txt')
data[label]['latency'] = {'sizes': sizes, 'values': latencies}
sizes, bandwidths = get_latency_bandwidth_data(datadir, range(5),
                                               prefix='stdout_bandwidth_run',
                                               suffix='.txt')
data[label]['bandwidth'] = {'sizes': sizes, 'values': bandwidths}
data[label]['kwargs'] = dict(color='C2', linestyle='-',
                             marker='o', markersize=6)

# Create a figure to display the latency and bandwidth results.
pyplot.rc('font', family='serif', size=14)
fig, (ax1, ax2) = pyplot.subplots(nrows=2, figsize=(6.0, 8.0))
# Plot the latency.
ax1.set_xlabel('Message size (bytes)')
ax1.set_ylabel(r'Point-to-point\nlatency ($\mu$s)')
ax1.grid()
key = 'latency'
for label, subdata in data.items():
    ax1.plot(subdata[key]['sizes'], subdata[key]['values'],
             label=label, **subdata['kwargs'])
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.legend()
# Plot the bandwidth.
ax2.set_xlabel('Message size (bytes)')
ax2.set_ylabel('Point-to-point\nbandwidth (MB/s)')
ax2.grid()
key = 'bandwidth'
for label, subdata in data.items():
    ax2.plot(subdata[key]['sizes'], subdata[key]['values'],
             label=label, **subdata['kwargs'])
ax2.set_xscale('log')
ax2.set_yscale('log')
fig.tight_layout()

# Save the figure.
figdir = rootdir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'osu_latency_bandwidth_all.pdf'
fig.savefig(str(filepath), dpi=300)

pyplot.show()
