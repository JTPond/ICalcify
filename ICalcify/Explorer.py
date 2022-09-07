import msgpack as msg
import msgpack_numpy as m
import numpy as np
from io import BytesIO
import json
from pathlib import Path

from ICalcify.Tree import read, Tree

m.patch()

def New(fnames,buffer=False):
    trees = dict([read(f,buffer=buffer,retname=True) for f in fnames])
    return Explorer(trees)

class Explorer(object):
    def __init__(self, trees):
        self.trees = trees

    def _ipython_key_completions_(self):
        return list(self.trees.keys())

    def __getitem__(self, key):
        if key in self.trees:
            if callable(self.trees[key]):
                self.trees[key] = (self.trees[key])()
            return self.trees[key]
        else:
            raise KeyError("\'{}\' not valid Tree".format(key))

    def __setitem__(self, name: str, tree: Tree) -> None:
        self.trees[name] = tree

    def __contains__(self, key):
        if key in self.trees:
            return True
        else:
            return False

    def __repr__(self):
        out = ""
        for key in self.trees:
            if callable(self.trees[key]):
                out += "\t{}: *buffered\n".format(key)
            else:
                out += "\t{}: {} branches\n".format(key,len(self.trees[key]))
        if len(self) == 0:
            out += '\tEMPTY'
        return out

    def _repr_html_(self):
        out = ""
        for key in self.trees:
            if callable(self.trees[key]):
                out += "<h2>{}: &#8250;</h2>".format(key)
            else:
                out += "<h2>{}: &#8964;</h2> <div style=\"margin: 20px;\">{}</div>".format(key,self.trees[key]._repr_html_())
        if len(self) == 0:
            out += '<h1>EMPTY</h1>'
        return out

    def __iter__(self):
        return self.trees.__iter__()

    def __len__(self):
        return self.trees.__len__()

    def load_all(self):
        for key in self.trees:
            if callable(self.trees[key]):
                self.trees[key] = (self.trees[key])()
