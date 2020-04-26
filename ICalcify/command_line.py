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
    parser.add_argument("-b", "--buffer", help="Buffer reading of Tree files in the Explorer", action="store_true")
    parser.add_argument("filename", type=str, nargs='*', help="Filepaths to open as Tree. Must contain file extension. [.jsonc, .msg]")
    args = parser.parse_args()
    fnames = args.filename
    Explorer = ic.New(fnames,buffer=args.buffer)
    str_exp = str(Explorer)
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

Explorer:

{}"""
    embed(header=header.format(str_exp))
if __name__ == '__main__':
    main()
