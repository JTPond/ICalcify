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

#### Jupyter

![Ex7](img/img_5.png?raw=true "Example 7")
