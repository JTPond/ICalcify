import msgpack as msg
import msgpack_numpy as m
import numpy as np
from io import BytesIO
import json
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import linregress
from ICalcify.fitting import FittingResult
from ICalcify.regression import RegResult
m.patch()

class ObjectBranch(object):
    def __init__(self, name, dtype, branch):
        self.name = name
        self.dtype = dtype
        if type(branch) == list:
            self.branch = np.array(branch)
        elif type(branch) == np.array or type(branch) == np.ndarray:
            self.branch = branch
        else:
            raise TypeError('Argument \'Branch\' must be of type list, or numpy.(nd)array, got {}'.format(type(branch)))

    def __len__(self):
        return len(self.branch)

    def __repr__(self):
        return "{{Name: '{}', Type: '{}', Length: {}}}".format(self.name,self.dtype,self.__len__())

    def __str__(self):
        ll = self.__len__()
        if ll > 20:
            return "Name: '{}'\n{}\n...\n{}\nType: '{}', Len: {}".format(self.name,"\n".join([str(x) for x in self.branch[:10]]),
                                                                        "\n".join([str(x) for x in self.branch[-10:]]),self.dtype,ll)
        else:
            return "Name: '{}'\n{}\nType: '{}', Len: {}".format(self.name,"\n".join([str(x) for x in self.branch]),self.dtype,ll)

    def __iter__(self):
        return self.branch.__iter__()

    def __next__(self):
        return self.branch.__next__()

    def _repr_html_(self):
        return "<h3><b>'{}':</b> Type: '{}', Length: {}</h3>".format(self.name,self.dtype,self.__len__())

    def cut(self,callable):
        return Branch(f"{self.name}_Cut",self.dtype,self.branch[[callable(x) for x in self.branch]])


class StringBranch(ObjectBranch):
    def __init__(self,name,branch):
        branch = np.array(branch)
        super().__init__(name,'String',branch)

class FloatBranch(ObjectBranch):
    def __init__(self,name,branch):
        branch = np.array(branch,dtype=np.float64)
        super().__init__(name,'f64',branch)

    def against(self, other):
        if not type(other) == FloatBranch:
            raise TypeError("Other branch must be of type FloatBranch")
        if not len(self.branch) == len(other.branch):
            raise RuntimeError("Both self and other branch must be the same length.")
        return PointBranch(f"{self.name} X {other.name}",np.array([[x,y] for x,y in zip(self.branch,other.branch)]))

    def plot(self,show=False):
        # f, ax = plt.subplots()
        plt.plot(np.arange(self.__len__()),self.branch,label=self.name)
        plt.legend()
        if show:
            plt.show()

class ThreeVecBranch(ObjectBranch):
    def __init__(self,name,branch):
        if len(branch) > 0:
            if type(branch[0]) == dict:
                branch = np.array(list(map(ThreeVecBranch.from_dict,branch)))
        branch = np.array(branch)
        super().__init__(name,'ThreeVec',branch)

    def from_dict(obj):
        return np.array([obj['x0'],obj['x1'],obj['x2']])

    def scatter(self,show=False):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.branch[:,0],self.branch[:,1],self.branch[:,2],marker='o')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        if show:
            plt.show()

class ThreeMatBranch(ObjectBranch):
    def __init__(self,name,branch):
        if len(branch) > 0:
            if type(branch[0]) == dict:
                branch = np.array(list(map(ThreeMatBranch.from_dict,branch)))
        branch = np.array(branch)
        super().__init__(name,'ThreeMat',branch)

    def from_dict(obj):
        return np.array([np.array([obj[ky]['x0'],obj[ky]['x1'],obj[ky]['x2']]) for ky in obj])

class FourVecBranch(ObjectBranch):
    def __init__(self,name,branch):
        if len(branch) > 0:
            if type(branch[0]) == dict:
                branch = np.array(list(map(FourVecBranch.from_dict,branch)))
        branch = np.array(branch)
        super().__init__(name,'FourVec',branch)

    def from_dict(obj):
        return np.array([obj['x0'],obj['x1'],obj['x2'],obj['x3']])

class FourMatBranch(ObjectBranch):
    def __init__(self,name,branch):
        if len(branch) > 0:
            if type(branch[0]) == dict:
                branch = np.array(list(map(FourMatBranch.from_dict,branch)))
        branch = np.array(branch)
        super().__init__(name,'FourMat',branch)

    def from_dict(obj):
        return np.array([np.array([obj[ky]['x0'],obj[ky]['x1'],obj[ky]['x2'],obj[ky]['x3']]) for ky in obj])

class BinBranch(ObjectBranch):
    def __init__(self,name,branch):
        if len(branch) > 0:
            if type(branch[0]) == dict:
                branch = np.array(list(map(BinBranch.from_dict,branch)))
            else:
                branch = np.array([np.array([np.float64(x[0]),np.array(x[1],dtype=np.float64)],dtype='object') for x in branch])
        super().__init__(name,'Bin',branch)

    def from_dict(obj):
        return np.array([obj['count'],np.array(obj['range'])])

    def __str__(self):
        return "Name: '{}'\n{}\n...\n{}\nType: '{}', Len: {}".format(
                self.name,"\n".join(["{}, range({}, {})".format(int(x[0]),x[1][0],x[1][1]) for x in self.branch[:10]]),
                "\n".join(["{}, range({}, {})".format(int(x[0]),x[1][0],x[1][1]) for x in self.branch[-10:]]),self.dtype,self.__len__())

    def plot(self,show=False):
        # f, ax = plt.subplots()
        x = []
        y = []
        for bin in self.branch:
            x += list(bin[1])
            y += [bin[0],bin[0]]
        plt.plot(x,y,label=self.name)
        plt.legend()
        if show:
            plt.show()

    def fit(self,func):
        x = []
        y = []
        for bin in self.branch:
            x.append(bin[1].mean())
            y.append(bin[0])
        popt, pcov = curve_fit(func,x,y)
        return FittingResult(func,x,popt,pcov,self.name)


class PointBranch(ObjectBranch):
    def __init__(self,name,branch):
        if len(branch) > 0:
            if type(branch[0]) == dict:
                branch = np.array(list(map(PointBranch.from_dict,branch)))
        branch = np.array(branch)
        super().__init__(name,'Point',branch)

    def from_dict(obj):
        return np.array([obj['x'],obj['y']])

    def plot(self,show=False):
        # f, ax = plt.subplots()
        plt.plot(self.branch[:,0],self.branch[:,1],label=self.name)
        plt.legend()
        if show:
            plt.show()

    def scatter(self,show=False):
        # f, ax = plt.subplots()
        plt.plot(self.branch[:,0],self.branch[:,1],marker='o',linestyle='',label=self.name)
        plt.legend()
        if show:
            plt.show()

    def fit(self,func):
        popt, pcov = curve_fit(func,self.branch[:,0],self.branch[:,1])
        return FittingResult(func,self.branch[:,0],popt,pcov,self.name)

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
    elif dtype == 'Object':
        return ObjectBranch(name,dtype,branch)
    else:
        raise ValueError(f"Argument, '{dtype}' is not an accepted value.")
