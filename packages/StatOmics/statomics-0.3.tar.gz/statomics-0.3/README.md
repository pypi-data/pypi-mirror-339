# StatOmics

StatOmics is a Python package that integrates powerful R-based statistical tools — primarily for proteomics data preprocessing and analysis — into a clean Python interface using [RPy2](https://rpy2.github.io/). It allows researchers and data scientists to leverage domain-specific R functions without writing R code.


## Requirements

This package requires:

- Python 3.8+
- R (version ≥ 4.1)
- R packages (see below)


### Required R Packages

Make sure the following R packages are installed before using the package:

- dplyr
- matrixStats
- stats


## Module Structure
- StatOmics/r_interface.py: Bridge for sourcing and calling R functions
- StatOmics/Preprocessing/: Preprocessing scripts
- StatOmics/Analysis/: Analysis scripts
- tests/: Examples usages and tests