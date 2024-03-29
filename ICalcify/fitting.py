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

def poly2(x, a,b,c):
    return a + b*(x) + c*(x**2.0)

def poly3(x, a,b,c,d):
    return a + b*(x) + c*(x**2.0) + d*(x**3.0)

def poly4(x, a,b,c,d,e):
    return a + b*(x) + c*(x**2.0) + d*(x**3.0) + e*(x**4.0)


class FittingResult(object):
    def __init__(self,func,xdata,popt,pcov,label="Result"):
        self.func = func
        self.xdata = xdata
        self.popt = popt
        self.pcov = pcov
        self.label = label
        self.errs = np.sqrt(np.diag(self.pcov))

    def __repr__(self):
        return "Parameters:\n{}".format(
            "\n".join(["\tx{} = {:.3f} +- {:.3f}".format(i,x,self.errs[i]) for i,x in enumerate(self.popt)])
        )

    def _repr_html_(self):
        return "<h3>Parameters:</h3><ul>{}</ul>".format(
            "\n".join(["<li>x{} = {:.3f} +- {:.3f}</li>".format(i,x,self.errs[i]) for i,x in enumerate(self.popt)])
        )

    def plot(self,show=False,error=False):
        if show:
            plt.figure()
        ydata = [self.func(x, *self.popt) for x in self.xdata]
        plt.plot(self.xdata,ydata,label=self.label+".Fit")
        plt.legend()
        if error:
            peydata = [self.func(x, *(o+e for o,e in zip(self.popt,self.errs))) for x in self.xdata]
            neydata = [self.func(x, *(o-e for o,e in zip(self.popt,self.errs))) for x in self.xdata]
            plt.fill_between(self.xdata,peydata,neydata,alpha=0.6)
        if show:
            plt.show()
