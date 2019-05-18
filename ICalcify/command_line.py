#! /usr/bin/env python3
import ICalcify as ic
import ICalcify.fitting as ft
from IPython import embed
import numpy as np
import scipy as sc
import scipy.optimize as opt
from matplotlib import pyplot as plt
from matplotlib.pyplot import show
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="ICalcify Explorer: Interactive analysis tool for Calcify Trees.")
    parser.add_argument("filename", type=str, help="Filepath to open as Tree. Must contain file extension. [.jsonc, .msg]")
    args = parser.parse_args()
    fname = args.filename
    try:
        Tree = ic.read(fname)
        str_tree = str(Tree)
    except IOError:
        Tree = None
        str_tree = "Import error on {}".format(fname)
    header = """Welcome to ICalcify. All commands must be valid Python3
IPython version and kernel information above, as usual. 

Namespaces included:
    ICalcify as ic
    ICalcify.fitting as ft
    numpy as np
    scipy as sc
    scipy.optimize as opt
    matplotlib.pyplot as plt
    plt.show as show

Tree:

{}"""
    embed(header=header.format(str_tree))

