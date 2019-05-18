import scipy as sc
import numpy as np
from matplotlib import pyplot as plt

# https://en.wikipedia.org/wiki/Gaussian_function
def Gaussian(x,a,b,c):
    up = ((x-b)**2.0)/(2.0*c**2.0)
    return a*np.exp(-up)

# https://en.wikipedia.org/wiki/Relativistic_Breit-Wigner_distribution
def BreitWigner(e,a,m,g):
    gamma = np.sqrt(m**2.0*(m**2.0 + g**2.0))
    k = (2.0*np.sqrt(2.0)*m*g*gamma)/(np.pi*np.sqrt(m**2.0 + gamma))
    lower = (e**2.0 - m**2.0)**2.0 + m**2.0*g**2.0
    return a*k/lower

def exponential(x,a,b,c):
    return a*np.exp(-b*x) + c

def linear(x,m,b):
    return m*x + b


class FittingResult(object):
    def __init__(self,func,xdata,popt,pcov,label="Result"):
        self.func = func
        self.xdata = xdata
        self.popt = popt
        self.pcov = pcov
        self.label = label
        
    def __repr__(self):
        errs = np.sqrt(np.diag(self.pcov))
        return "Parameters:\n{}".format(
            "\n".join(["\tx{} = {} +- {}".format(i,x,errs[i]) for i,x in enumerate(self.popt)])    
        )

    def plot(self,show=False):
        ydata = [self.func(x, *self.popt) for x in self.xdata]
        plt.plot(self.xdata,ydata,label=self.label+".Fit")
        plt.legend()
        if show:
            plt.show()

