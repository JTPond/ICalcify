import msgpack as msg
import msgpack_numpy as m
m.patch()
import numpy as np
from io import BytesIO
import json
from pathlib import Path

def read_msg(filename):
    if type(filename) == str:
        with open(filename,"rb") as f:
            return Tree.from_dict(msg.unpackb(f.read(),raw=False, object_hook=m.decode))
    elif type(filename) == Path:
        with filename.open("rb") as f:
             return Tree.from_dict(msg.unpackb(f.read(),raw=False, object_hook=m.decode))

class BaseBranch(object):
    def __init__(self, name, dtype, branch):
        self.name = name
        self.dtype = dtype
        if type(branch) == list:
            self.branch = np.array(branch)
        elif type(branch) == np.array or type(branch) == np.ndarray:
            self.branch = branch
        else:
            raise TypeError('Argument \'Branch\' must be of type list, or numpy.(nd)array, got {dt}'.format(dt=type(branch)))
        
    def __len__(self):
        return len(self.branch)
    
    def __repr__(self):
        return "Branch(Name: '{}', Type: '{}', Length: '{}')".format(self.name,self.dtype,self.__len__())
                
class BinBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array([np.array([np.float64(x[0]),np.array(x[1],dtype=np.float64)]) for x in branch])
        super().__init__(name,'Bin',branch)
        
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
                if branches[key]['subtype'] == 'Bin':
                    tTree.branches[key] = BinBranch(key,branches[key]['branch'])
                else:
                    tTree.branches[key] = BaseBranch(key,branches[key]['subtype'],branches[key]['branch'])
        else:
            raise RuntimeError('No \'Branches\' field in input dictionary.')
        return tTree
        
