#! /usr/bin/env python3
import ICalcify as ic
from IPython import embed
import numpy as np
import scipy as sc
from matplotlib import pyplot as plt
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="ICalcify Explorer: Interactive analysis tool for Calcify Trees.")
    parser.add_argument("filename", type=str, help="Filepath to open as Tree. Must contain file extension. [.jsonc, .msg]")
    args = parser.parse_args()
    try:
        if args.filename.split('.')[-1] == "msg":
            Tree = ic.read_msg(args.filename)
        elif args.filename.split('.')[-1] == "jsonc":
            Tree = ic.read_jsonc(args.filename)
        else:
            exit("Unsuported file extension: {}".format(args.filename.split('.')[1]))
    except IndexError:
        exit("Filename must contain file extension.")

    header = """Welcome to ICalcify. All commands must be valid Python3
    IPython version and kernel information above, as usual. 

    Namespace includes:
        ICalcify as ic
        numpy as np
        scipy as sc
        matplotlib.pyplot as plt

    Tree:

    {}
    """
    embed(header=header.format(str(Tree)))

    res = input('Save your work? [Y]/n: ')
    if res == 'n':
        exit(0)
    with open('test_tree.json',"w+") as f:
        f.write(json.dumps(Tree))
