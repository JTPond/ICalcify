import msgpack as msg
import msgpack_numpy as m
import numpy as np
from io import BytesIO
import json
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from ICalcify.fitting import FittingResult
m.patch()

class BaseBranch(object):
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
        return "Branch(Name: '{}', Type: '{}', Length: {})".format(self.name,self.dtype,self.__len__())

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


class StringBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array(branch)
        super().__init__(name,'String',branch)

class FloatBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array(branch,dtype=np.float64)
        super().__init__(name,'f64',branch)

    def plot(self,show=False):
        # f, ax = plt.subplots()
        plt.plot(np.arange(self.__len__()),self.branch,label=self.name)
        plt.legend()
        if show:
            plt.show()

class ThreeVecBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array(branch)
        super().__init__(name,'ThreeVec',branch)

    def scatter(self,show=False):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.branch[:,0],self.branch[:,1],self.branch[:,2],marker='o')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        if show:
            plt.show()

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


class PointBranch(BaseBranch):
    def __init__(self,name,branch):
        branch = np.array(branch)
        super().__init__(name,'Point',branch)

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
        popt, pcov = curve_fit(func,self.branch[:,0],self.branch[:1])
        return FittingResult(func,self.branch[:0],popt,pcov,self.name)

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
