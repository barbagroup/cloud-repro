# OSU Micro-Benchmarks

## Contents

* `azure`: input files to run the benchmarks on Microsoft Azure.
* `colonialone`: input files to run the benchmarks on Colonial One<sup>[1](#footnote_colonialone)</sup>.
* `scripts/plot_latency_bandwidth.py`: Python script to plot the results of the benchmarks.
* `figures/osu_latency_bandwidth.pdf`: Figure with the results of the benchmarks.

<a name="footnote_colonialone">1</a>: Colonial One is the HPC cluster at the George Washington University.

## Re-create the figure in the manuscript

All command-lines written below are run from the `README`'s directory.
To-regenerate the figure with the results of the OSU Micro-Benchmarks:

```shell
python scripts/plot_latency_bandwidth.py
```

The Python script saves the Matplotlib figure as a PDF file (`osu_latency_bandwidth.pdf`) in the `figures` folder (automatically created if not present).
