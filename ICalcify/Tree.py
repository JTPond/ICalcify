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

def read_jsonc(filename):
    if type(filename) == str:
        with open(filename,"r") as f:
            return Tree.from_dict(json.loads(f.read()))
    elif type(filename) == Path:
        with filename.open("r") as f:
             return Tree.from_dict(json.loads(f.read()))


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
        return "Branch(Name: '{}', Type: '{}', Length: {})".format(self.name,self.dtype,self.__len__())

    def __str__(self):
        ll = self.__len__()
        if ll > 20:
            return "Name: '{}'\n{}\n...\n{}\nType: '{}', Len: {}".format(self.name,"\n".join([str(x) for x in self.branch[:10]]),
                                                                        "\n".join([str(x) for x in self.branch[-10:]]),self.dtype,ll)
        else:
            return "Name: '{}'\n{}\nType: '{}', Len: {}".format(self.name,"\n".join([str(x) for x in self.branch]),self.dtype,ll)

                
class StringBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array(branch)
        super().__init__(name,'String',branch)

class FloatBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array(branch,dtype=np.float64)
        super().__init__(name,'f64',branch)

class ThreeVecBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array(branch)
        super().__init__(name,'ThreeVec',branch)

class ThreeMatBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array(branch)
        super().__init__(name,'ThreeMat',branch)

class FourVecBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array(branch)
        super().__init__(name,'FourVec',branch)

class FourMatBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array(branch)
        super().__init__(name,'FourMat',branch)

class BinBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array([np.array([np.float64(x[0]),np.array(x[1],dtype=np.float64)]) for x in branch])
        super().__init__(name,'Bin',branch)

    def __str__(self):
        return "Name: '{}'\n{}\n...\n{}\nType: '{}', Len: {}".format(self.name,"\n".join(["{}, range({}, {})".format(int(x[0]),x[1][0],x[1][1]) for x in self.branch[:10]]),
                                                                    "\n".join(["{}, range({}, {})".format(int(x[0]),x[1][0],x[1][1]) for x in self.branch[-10:]]),self.dtype,self.__len__())

class PointBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array(branch)
        super().__init__(name,'Point',branch)


def Branch(name, dtype, branch):
    if dtype == 'String':
        return StringBranch(name,branch)
    elif dtype == 'f64':
        return FloatBranch(name,branch)
    elif dtype == 'ThreeVec':
        return ThreeVecBranch(name,branch)
    elif dtype == 'ThreeMat':
        return ThreeMatBranch(name,branch)
    elif dtype == 'FourVec':
        return FourVecBranch(name,branch)
    elif dtype == 'FourMat':
        return FourMatBranch(name,branch)
    elif dtype == 'Bin':
        return BinBranch(name,branch)
    elif dtype == 'Point':
        return PointBranch(name,branch)
    else:
        raise ValueError('Argument, \'dtype\' is not an accepted value.')


class Tree(object):
    def __init__(self):
        self.metadata = {}
        self.branches = {}
        self.plots = {}
        self.fits = {}
        
    def from_dict(tree_dict):
        tTree = Tree()
        branches = tree_dict.pop('branches',False)
        plots = tree_dict.pop('plots',{})
        fits = tree_dict.pop('fits',{})
        if branches:
            tTree.metadata = tree_dict
            for key in branches:
                tTree.branches[key] = Branch(key,branches[key]['subtype'],branches[key]['branch'])
        else:
            raise RuntimeError('No \'Branches\' field in input dictionary.')
        for key in plots:
            tTree.plots[key] = Branch(key,plots[key]['subtype'],plots[key]['branch'])
        for key in fits:
            tTree.fits[key] = Branch(key,fits[key]['subtype'],fits[key]['branch'])
        return tTree

    def __getitem__(self, key):
        if key in self.metadata:
            return self.metadata[key]
        elif key in self.branches:
            return self.branches[key]
        else:
            raise KeyError("\'{}\' not in metadata, or branches".format(key))

    def __repr__(self):
        out = "Name: {}\n".format(self.metadata['Name'])
        out += "Branches: \n"
        for branch in self.branches:
            out += "\t{}\n".format(self.branches[branch].__repr__())
        out += "Plots: \n"
        for branch in self.plots:
            out += "\t{}\n".format(self.plots[branch].__repr__())
        out += "Fits: \n"
        for branch in self.fits:
            out += "\t{}\n".format(self.fits[branch].__repr__())
        return out

    def __str__(self):
        out = "Name: {}\n".format(self.metadata['Name'])
        for key in self.metadata:
            if not key == 'Name':
                out += "{}: {}\n".format(key, self.metadata[key])
        out += "{} branches: \n".format(len(self.branches))
        for branch in self.branches:
            out += "\t{}\n".format(self.branches[branch].__repr__())
        out += "{} plots: \n".format(len(self.plots))
        for branch in self.plots:
            out += "\t{}\n".format(self.plots[branch].__repr__())
        out += "{} fits: \n".format(len(self.fits))
        for branch in self.fits:
            out += "\t{}\n".format(self.fits[branch].__repr__())
        return out
