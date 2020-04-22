import msgpack as msg
import msgpack_numpy as m
import numpy as np
from io import BytesIO
import json
from pathlib import Path

from ICalcify.Tree import Tree

m.patch()

class Explorer(object):
    def __init__(self, trees):
        self.trees = trees

    def _ipython_key_completions_(self):
        return list(self.trees.keys())

    def __getitem__(self, key):
        if key in self.trees:
            return self.trees[key]
        else:
            raise KeyError("\'{}\' not valid Tree".format(key))

    def __contains__(self, key):
        if key in self.trees:
            return True
        else:
            return False

    def __repr__(self):
        out = ""
        for tree in self.trees:
            out += "\t{}: {} branches\n".format(tree,len(self.trees[tree]))
        if len(self) == 0:
            out += '\tEMPTY'
        return out

    def __iter__(self):
        return self.trees.__iter__()

    def __len__(self):
        return self.trees.__len__()
