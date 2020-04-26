import msgpack as msg
import msgpack_numpy as m
import numpy as np
from io import BytesIO
import json
from pathlib import Path

from ICalcify.branches import Branch

m.patch()

def read_msg(filename):
    try:
        with filename.open("rb") as f:
            return Tree.from_dict(msg.unpackb(f.read(),raw=False, object_hook=m.decode))
    except Exception as e:
        print("{} raised {}, returning empty Tree".format(filename.name,repr(e)))
        return Tree()

def read_jsonc(filename):
    try:
        with filename.open("r") as f:
            return Tree.from_dict(json.loads(f.read()))
    except Exception as e:
        print("{} raised {}, returning empty Tree".format(filename.name,repr(e)))
        return Tree()

def read(filename, buffer=False, retname=False):
    filename = Path(filename)
    if buffer:
        return filename.stem, lambda fname=filename.resolve(True): read(fname)

    if filename.suffix == '.msg':
        Tree = read_msg(filename)
    elif filename.suffix == '.jsonc':
        Tree = read_jsonc(filename)
    else:
        raise ValueError("File extension must .msg, or .jsonc")

    if retname:
        return filename.stem, Tree

    return Tree

class Tree(object):
    def __init__(self):
        self.metadata = {}
        self.branches = {}

    def from_dict(tree_dict):
        tTree = Tree()
        branches = tree_dict.pop('branches',False)
        feeds = tree_dict.pop('datafeeds',False)
        if branches:
            tTree.metadata = tree_dict
            for key in branches:
                tTree.branches[key] = Branch(key,branches[key]['subtype'],branches[key]['branch'])
        elif feeds:
            tTree.metadata = tree_dict
            for key in feeds:
                tTree.branches[key] = Branch(key,tTree.metadata['SubType'],feeds[key])
        else:
            raise RuntimeError('Structure does not match Tree, or FeedTree specs')
        return tTree

    def _ipython_key_completions_(self):
        return list(self.branches.keys()) + list(self.metadata.keys())

    def __getitem__(self, key):
        if key in self.branches:
            return self.branches[key]
        elif key in self.metadata:
            return self.metadata[key]
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
        for key in self.metadata:
            if not key == 'Name':
                out += "\t{}: {}\n".format(key, self.metadata[key])
        return out

    def _repr_html_(self):
        out = "<h2><u>{}</u></h2>".format(self.metadata['Name'])
        for key in self.metadata:
            if not key == 'Name':
                out += "<h3 style=\"margin: 20px;\"><b>{}</b>: {}</h3>".format(key, self.metadata[key])
        out += "<h3 style=\"margin: 20px;\"><b>Branches</b>: {}</h3>".format(self.__len__())
        return out

    def __str__(self):
        out = "Name: {}\n".format(self.metadata['Name'])
        out += "{} branches: \n".format(len(self.branches))
        for branch in self.branches:
            out += "\t{}\n".format(self.branches[branch].__repr__())
        return out

    def __len__(self):
        return len(self.branches)

    def __iter__(self):
        return self.branches.__iter__()
