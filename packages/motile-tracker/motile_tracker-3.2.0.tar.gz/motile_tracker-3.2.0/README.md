# Motile Tracker

[![tests](https://github.com/funkelab/motile_tracker/workflows/tests/badge.svg)](https://github.com/funkelab/motile_tracker/actions)
[![codecov](https://codecov.io/gh/funkelab/motile_tracker/branch/main/graph/badge.svg)](https://codecov.io/gh/funkelab/motile_tracker)

The full documentation of the plugin can be found [here](https://funkelab.github.io/motile_tracker/).

An application for interactive tracking with [motile](https://github.com/funkelab/motile)
Motile is a library that makes it easy to solve tracking problems using optimization
by framing the task as an Integer Linear Program (ILP).
See the motile [documentation](https://funkelab.github.io/motile)
for more details on the concepts and method.

----------------------------------

## Installation

This application depends on [motile](https://github.com/funkelab/motile), which in
turn depends on gurobi and ilpy. These dependencies must be installed with
conda before installing the plugin with pip.

    conda create -n motile-tracker python=3.10
    conda activate motile-tracker
    conda install -c conda-forge -c funkelab -c gurobi ilpy
    pip install motile-tracker

## Running Motile Tracker

To run the application:
* activate the conda environment created in the [Installation Step](#installation)

    conda activate motile-tracker

* Run:

    python -m motile_tracker

or

    motile_tracker

## Issues

If you encounter any problems, please
[file an issue](https://github.com/funkelab/motile_tracker/issues)
along with a detailed description.
