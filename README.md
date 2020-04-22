# ICalcify

An interactive tool, using embeded IPython, for exploring and analysing Trees produced by the [Calcify Rust crate](https://crates.io/crates/calcify "Calcify crates.io entry").
Includes plotting and fitting tools.

## Installation

Clone the repository and from inside run:

`(sudo) python(3) setup.py install`

This will install the `icalcify` command line tool and the ICalcify library.

## Usage examples
### Example 1: from the calcify/examples/universe\_in\_a\_box
#### Startup

Run:

`icalcify [-h] [filename [filename ...]]`, where filename is a .msg, or .jsonc Tree file from Calcify. The extension is required.

Try `icalcify *.msg` when you have a lot of Trees to browse.

This will open the an IPython shell with a variable called `Explorer` of type ICalcify.Explorer.

```
Python 3.5.3 (default, Sep 27 2018, 17:25:39)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.2.0 -- An enhanced Interactive Python. Type '?' for help.


Welcome to ICalcify. All commands must be valid Python3
IPython version and kernel information above, as usual.

Namespaces included:
    ICalcify as ic
    ICalcify.fitting as ft
    numpy as np
    scipy as sc
    scipy.optimize as opt
    matplotlib.pyplot as plt
    plt.show as show

Explorer:

    	universe: 10 branches

```

We can save some writing by starting with:

`In [1]: Tree = Explorer['universe']`

#### Plotting

From here you can run:

`In [1]: Tree['fin_hist'].plot(True)`
(The plot function takes a boolean argument that defaults to False which can call plt.show() if set to True)

which opens a pyplot window such as:

![Ex1](img/img_1.png?raw=true "Example 1")

To show multiple plots:

```
In [1]: Tree['mid2_hist'].plot()

In [2]: Tree['fin_hist'].plot(True)
```

or

```
In [1]: Tree['mid2_hist'].plot()

In [2]: Tree['fin_hist'].plot()

In [3]: show()
```

will give you:

![Ex2](img/img_2.png?raw=true "Example 2")

You can also get a scatter plot of ThreeVec branches with:

`In [1]: Tree['mid2_state'].scatter(True)`

![Ex3](img/img_3.png?raw=true "Example 3")

#### Fitting

Built in fitting functions include Gaussian, BrietWigner, exponential, and linear.

To do a fit run:

```
In [1]: Tree['mid2_hist'].fit(ft.Gaussian)
Out[1]:
Parameters:
        x0 = 7.8031859841299775 +- 0.48292339703133214
        x1 = 0.8229363430601933 +- 0.023861344606247444
        x2 = 0.31201350865832883 +- 0.026763654689396284
```

or

```
In [1]: FitRes = Tree['mid2_hist'].fit(ft.Gaussian)

In [2]: FitRes
Out[2]
Parameters:
        x0 = 7.8031859841299775 +- 0.48292339703133214
        x1 = 0.8229363430601933 +- 0.023861344606247444
        x2 = 0.31201350865832883 +- 0.026763654689396284

In [3]: type(FitRes)
Out[3]: ICalcify.fitting.FittingResult
```

To plot the result over the original:

```
In [1]: Tree['mid2_hist'].plot()

In [2]: Tree['mid2_hist'].fit(ft.Gaussian).plot(True)
```

![Ex4](img/img_4.png?raw=true "Example 4")
