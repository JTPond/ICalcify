# Release Notes

### 0.1.2: 2026-11-10

* Python 3.15 and NumPy 2.x readiness
* Migrated packaging to PEP 621 `pyproject.toml`
* Removed stale `base` and `regression` imports
* Added `@staticmethod` decorators to `from_dict` constructors and fixed `PointBinBranch` inhomogeneous array creation

### 0.1.1: 2022-01-16

* Supports new calcify::PointBin type
    * Plot 2D hist


* Added plt.figure so the ion environment works

### 0.1 2020-06-06

* *END SUPPORT FOR JSONC in favor of JSON*

### 0.0.6 2020-05-13

* Support Object Branches

### 0.0.5 2020-04-26

* Added buffered reading of Trees into the Explorer

* Added better Jupyter support

### 0.0.4: 2020-04-21

* Added Explorer class and the ability to read more than one file from the command line.

* Added iterability to Branches for element-wise iteration. And to Explorers and Trees for iterating over keys.