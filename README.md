# ICalcify

An interactive tool, using embeded IPython, for exploring and analysing Trees produced by the [Calcify Rust crate](https://crates.io/crates/calcify "Calcify crates.io entry").
Includes plotting and fitting tools.

## Installation

Clone the repository and from inside run:

`(sudo) python(3) setup.py install`

This will install the `icalcify` command line tool and the ICalcify library.

## Usage examples
### CLI
```
usage: icalcify [-h] [-b] [filename [filename ...]]

ICalcify Explorer: Interactive analysis tool for Calcify Trees.

positional arguments:
  filename      Filepaths to open as Tree. Must contain file extension.
                [.json, .msg]

optional arguments:
  -h, --help    show this help message and exit
  -b, --buffer  Buffer reading of Tree files in the Explorer

```
### Example 1: from the calcify/examples/universe\_in\_a\_box
#### Startup

Run:
`> icalcify universe.msg`
This will open the an IPython shell with a variable called `Explorer` of type ICalcify.Explorer.

```
Python <VERSION>
Type 'copyright', 'credits' or 'license' for more information
IPython <VERSION> -- An enhanced Interactive Python. Type '?' for help.


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

```python
In [1]: Tree = Explorer['universe']

In [2]: Tree
Out[2]:
Name: universe_in_a_box
	Desc: A Tree including branches for the simple universe in a box multiparticle simulation.
	Details: Universe Range: 1, Number of Particles: 500, Delta T: 0.01, Time steps: 2000, Total Time: 20
	Run on: 04/18/2020 17:23

In [3]: print(Tree)
Name: universe_in_a_box
10 branches:
	{Name: 'init_state', Type: 'ThreeVec', Length: 500}
	{Name: 'init_hist', Type: 'Bin', Length: 500}
	{Name: 'mid1_hist', Type: 'Bin', Length: 500}
	{Name: 'fin_state', Type: 'ThreeVec', Length: 500}
	{Name: 'mid2_state', Type: 'ThreeVec', Length: 500}
	{Name: 'mid1_state', Type: 'ThreeVec', Length: 500}
	{Name: 'fin_spread', Type: 'Point', Length: 404}
	{Name: 'init_spread', Type: 'Point', Length: 383}
	{Name: 'mid2_hist', Type: 'Bin', Length: 500}
	{Name: 'fin_hist', Type: 'Bin', Length: 500}

```
#### Buffered Explorer
`> icalcify -b universe.msg`

Will instead give you:

```python
Python 3.5.3 (default, Sep 27 2018, 17:25:39)

...

Explorer:

	universe: *buffered


In [1]: Explorer['universe']                                                                                                     
Out[1]:
Name: universe_in_a_box
	Desc: A Tree including branches for the simple universe in a box multiparticle simulation.
	Details: Universe Range: 1, Number of Particles: 500, Delta T: 0.01, Time steps: 2000, Total Time: 20
	Run on: 04/18/2020 17:23

In [2]: Explorer                                                                                                  
Out[2]: 	universe: 10 branches

```

`ICalcify.Explorer.load_all()` will load all buffered Trees into the Explorer.

#### ObjectBranches

If you have a FeedTree of subtype Object it will be read in as a regular tree of ObjectBranches where the data is read in verbatim as python dicts. These branches implement `__iter__(self)` so they should be easy for the user to convert to whatever type they like.

#### Plotting

From here you can run:

```python
In [1]: Tree['fin_hist'].plot(True)
```
(The plot function takes a boolean argument that defaults to False which can call plt.show() if set to True)

which opens a pyplot window such as:

![Ex1](img/img_1.png?raw=true "Example 1")

To show multiple plots:

```python
In [1]: Tree['mid2_hist'].plot()

In [2]: Tree['fin_hist'].plot(True)
```

or

```python
In [1]: Tree['mid2_hist'].plot()

In [2]: Tree['fin_hist'].plot()

In [3]: show()
```

will give you:

![Ex2](img/img_2.png?raw=true "Example 2")

You can also get a scatter plot of ThreeVec branches with:

```python
In [1]: Tree['mid2_state'].scatter(True)
```

![Ex3](img/img_3.png?raw=true "Example 3")

To show multiple figures without blocking call:

```python
In [1]: plt.ion()

In [2]: Tree['fin_hist'].plot(True)
```

#### Fitting

Built in fitting functions include Gaussian, BrietWigner, exponential, and linear.

To do a fit run:

```python
In [1]: Tree['mid2_hist'].fit(ft.Gaussian)
Out[1]:
Parameters:
	x0 = 1.340 +- 0.044
	x1 = 0.878 +- 0.021
	x2 = 0.519 +- 0.030

```

or

```python
In [1]: FitRes = Tree['mid2_hist'].fit(ft.Gaussian)

In [2]: FitRes
Out[2]
Parameters:
	x0 = 1.340 +- 0.044
	x1 = 0.878 +- 0.021
	x2 = 0.519 +- 0.030


In [3]: type(FitRes)
Out[3]: ICalcify.fitting.FittingResult
```

To plot the result over the original:

```python
In [1]: Tree['mid2_hist'].plot()

In [2]: Tree['mid2_hist'].fit(ft.Gaussian).plot(True)
```

![Ex4](img/img_4.png?raw=true "Example 4")

#### Other

If you have two `FloatBranch`s,

```python
In [1]: g = ic.Branch('g','f64',[1.0,2.0,3.0])
   ...: h = ic.Branch('h','f64',[2.0,4.0,6.0])
```
then you can plot them against each other,

```python
In [2]: type(g.against(h))                   
Out[2]: ICalcify.branches.PointBranch

In [3]: g.against(h).scatter(True)
```

![Ex5](img/img_6.png?raw=true "Example 5")

If you want to filter/cut a Branch,

```python
In [1]: bib = ic.Branch('Time','Bin',[[i,[i,i]] for i in range(300)])

In [2]: print(bib)
Out[2]: Name: 'Time'
    0, range(0.0, 0.0)
    1, range(1.0, 1.0)
    2, range(2.0, 2.0)
    3, range(3.0, 3.0)
    4, range(4.0, 4.0)
    5, range(5.0, 5.0)
    6, range(6.0, 6.0)
    7, range(7.0, 7.0)
    8, range(8.0, 8.0)
    9, range(9.0, 9.0)
    ...
    290, range(290.0, 290.0)
    291, range(291.0, 291.0)
    292, range(292.0, 292.0)
    293, range(293.0, 293.0)
    294, range(294.0, 294.0)
    295, range(295.0, 295.0)
    296, range(296.0, 296.0)
    297, range(297.0, 297.0)
    298, range(298.0, 298.0)
    299, range(299.0, 299.0)
    Type: 'Bin', Len: 300

In [3]: print(bib.cut(lambda x: x[1][0] > 100))
Out[3]: Name: 'Time_Cut'
    101, range(101.0, 101.0)
    102, range(102.0, 102.0)
    103, range(103.0, 103.0)
    104, range(104.0, 104.0)
    105, range(105.0, 105.0)
    106, range(106.0, 106.0)
    107, range(107.0, 107.0)
    108, range(108.0, 108.0)
    109, range(109.0, 109.0)
    110, range(110.0, 110.0)
    ...
    290, range(290.0, 290.0)
    291, range(291.0, 291.0)
    292, range(292.0, 292.0)
    293, range(293.0, 293.0)
    294, range(294.0, 294.0)
    295, range(295.0, 295.0)
    296, range(296.0, 296.0)
    297, range(297.0, 297.0)
    298, range(298.0, 298.0)
    299, range(299.0, 299.0)
    Type: 'Bin', Len: 199
```

#### Jupyter

![Ex7](img/img_5.png?raw=true "Example 7")
