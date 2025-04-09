# apollinaire

[![Anaconda-Server Badge](https://anaconda.org/conda-forge/apollinaire/badges/license.svg)](https://anaconda.org/conda-forge/apollinaire)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/apollinaire/badges/version.svg)](https://anaconda.org/conda-forge/apollinaire)
[![Documentation Status](https://readthedocs.org/projects/apollinaire/badge/?version=latest)](https://apollinaire.readthedocs.io/en/latest/?badge=latest)
[![Static Badge](https://img.shields.io/badge/reference-paper-orange)](https://www.aanda.org/articles/aa/abs/2022/07/aa43330-22/aa43330-22.html)

Python tools for helioseismic and asteroseismic frameworks.  This package
provides functions and framework designed for helioseismic and asteroseismic
instruments data managing and analysis.  

The core of the package is the ``peakbagging`` library, which provides a full
framework to extract oscillation modes parameters from solar and stellar power
spectra. 

## Getting Started

### Prerequisites

The apollinaire package core framework is written in Python 3.
The following Python package are necessary to use ``apollinaire`` : 
- numpy
- scipy
- pandas
- matplotlib
- h5py
- emcee
- corner
- pathos
- dill
- statsmodels
- numba
- george
- astropy
- tqdm

### Installing

With conda:

`conda install -c conda-forge apollinaire`

With pip:

`pip install apollinaire` 

You can also install the most recent version of apollinaire by cloning the GitLab repository:

`git clone https://gitlab.com/sybreton/apollinaire.git`

### Documentation

Documentation is available on [Read the Docs](https://apollinaire.readthedocs.io).

## Authors

Software development:

* **Sylvain N. Breton** - Maintainer - (INAF - Osservatorio astrofisico di Catania)

Contributors are listed below:

* **Rafael A. García** - Contributor - (CEA Saclay)
* **Vincent Delsanti** - Contributor - (CentraleSupélec)
* **Jérôme Ballot** - Contributor - (IRAP - Université de Toulouse)

## Acknowledgements 

If you use ``apollinaire`` in your work, please cite the ``apollinaire`` reference paper
([Breton et al., 2022](https://ui.adsabs.harvard.edu/abs/2022A%26A...663A.118B/abstract)),
the Astrophysics Source Code Library 
[code record](https://ascl.net/2306.022),  
and provide a link to the GitLab repository. You will find more [detailed citing instructions
in the documentation](https://apollinaire.readthedocs.io/en/latest/usage/citing_apollinaire.html). 
