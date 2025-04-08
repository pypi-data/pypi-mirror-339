<div align="center">

![logo](./docs/img/buzz.svg){width=25%}

[![python version](https://img.shields.io/pypi/pyversions/hvlbuzz.svg?logo=python&logoColor=white)](https://pypi.org/project/hvlbuzz)
[![latest version](https://img.shields.io/pypi/v/hvlbuzz.svg)](https://pypi.org/project/hvlbuzz)
[![pipeline status](https://gitlab.com/ethz_hvl/hvlbuzz/badges/main/pipeline.svg)](https://gitlab.com/ethz_hvl/hvlbuzz/-/commits/main)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![code linter: Ruff](
https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](
https://github.com/astral-sh/ruff)

HVLBuzz is a simulation tool to calculate the surface gradient of
overhead power lines and predict the audible noise and electromagnetic
field at ground.

[Install](#installation) •
[Usage](#usage) •
[📖 Docs](https://ethz_hvl.gitlab.io/hvlbuzz/)

</div>

# HVLBuzz

## Installation

 Operating System    | Download                                                                              
---------------------|---------------------------------------------------------------------------------------
 🪟 Windows (64 bit) | [![](./docs/img/get_windows.svg)](../-/jobs/artifacts/main/raw/dist/buzz.zip?job=exe) 
 🐧 Linux            | `pip install hvlbuzz`                                                                 
 🍏 Mac              | `pip install hvlbuzz`                                                                 

## Development setup

It is recommended that you use a Python virtual envioronement to run
HVLBuzz. Run the following command to create folder called `kivy_venv`
inside which your environement will live. **The latest version of
Python this code has been tested with was 3.10**

```sh
python -m venv kivy_venv
```

Activate your virtual environement by running

```sh
kivy_venv\Scripts\activate.bat # 🪟
. kivy_venv/bin/activate # 🐧 / 🍏
```

Then install hvlbuzz into your environement as follows

```sh
pip install .
pip install garden.matplotlib/
```

This will also install an executable python script in your environments `bin` folder.

## Usage

To run the binary obtained in the install part, run

```sh
hvlbuzz
```

Alternatively, the module is can also be started from python:

```sh
python -m hvlbuzz
```

or

```sh
python hvlbuzz
```

## Compiling your own packaged version

The source code can also be compiled by yourself using
[PyInstaller](https://www.pyinstaller.org/) using the provided
[hvlbuzz/buzz.spec](hvlbuzz/buzz.spec) file.

```bash
pyinstaller hvlbuzz/buzz.spec
```

A `buzz.exe` binary will be available in a (newly created if
non-existing) `dist\buzz` folder.

## Credits

Originally, HVLBuzz was developed by Aldo Tobler under the supervision of
Christian M. Franck, Sören Hedtke and support by Mikołaj Rybiński at
ETH Zurich's High Voltage Laboratory.

Currently, it is maintained by FKH Zürich.

This tool is completely free to use as is and only requires freely
available [Python](https://www.python.org/) libraries to run. The GUI
is based on the [Kivy](https://kivy.org/#home) framework, while the
mathematical computations and plot generation rely the widely used
[NumPy](https://numpy.org/) and [Matplotlib](https://matplotlib.org/).
