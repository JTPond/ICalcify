import msgpack as msg
import msgpack_numpy as m
m.patch()
import numpy as np
from io import BytesIO
import json
from pathlib import Path

from ICalcify.Tree import Tree

def read_msg(filename):
    if type(filename) == str:
        with open(filename,"rb") as f:
            return Tree.from_dict(msg.unpackb(f.read(),raw=False, object_hook=m.decode))
    elif type(filename) == Path:
        with filename.open("rb") as f:
             return Tree.from_dict(msg.unpackb(f.read(),raw=False, object_hook=m.decode))

def read_jsonc(filename):
    if type(filename) == str:
        with open(filename,"r") as f:
            return Tree.from_dict(json.loads(f.read()))
    elif type(filename) == Path:
        with filename.open("r") as f:
             return Tree.from_dict(json.loads(f.read()))

def read(filename):
    try:
        if filename.split('.')[-1] == "msg":
            Tree = read_msg(filename)
        elif filename.split('.')[-1] == "jsonc":
            Tree = read_jsonc(filename)
        else:
            raise IOError("Unsuported file extension: {}".format(filename.split('.')[1]))
        return Tree
    except IndexError:
        exit("Filename must contain file extension.")



