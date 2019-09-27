import msgpack as msg
import msgpack_numpy as m
import numpy as np
from io import BytesIO
import json
from pathlib import Path

from ICalcify.branches import Branch

m.patch()

class Tree(object):
    def __init__(self):
        self.metadata = {}
        self.branches = {}

    def from_dict(tree_dict):
        tTree = Tree()
        branches = tree_dict.pop('branches',False)
        if branches:
            tTree.metadata = tree_dict
            for key in branches:
                tTree.branches[key] = Branch(key,branches[key]['subtype'],branches[key]['branch'])
        else:
            raise RuntimeError('No \'Branches\' field in input dictionary.')
        return tTree

    def _ipython_key_completions_(self):
        return list(self.branches.keys()) + list(self.metadata.keys())

    def __getitem__(self, key):
        if key in self.metadata:
            return self.metadata[key]
        elif key in self.branches:
            return self.branches[key]
        else:
            raise KeyError("\'{}\' not in metadata, or branches".format(key))

    def __contains__(self, key):
        if key in self.metadata:
            return True
        elif key in self.branches:
            return True
        else:
            return False

    def __repr__(self):
        out = "Name: {}\n".format(self.metadata['Name'])
        out += "Branches: \n"
        for branch in self.branches:
            out += "\t{}\n".format(self.branches[branch].__repr__())
        return out

    def __str__(self):
        out = "Name: {}\n".format(self.metadata['Name'])
        for key in self.metadata:
            if not key == 'Name':
                out += "{}: {}\n".format(key, self.metadata[key])
        out += "{} branches: \n".format(len(self.branches))
        for branch in self.branches:
            out += "\t{}\n".format(self.branches[branch].__repr__())
        return out
