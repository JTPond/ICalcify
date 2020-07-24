import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import linregress

class RegResult(object):
    """Takes a scipy linregress output"""


    def __init__(self, xdata, slope, intercept, r_value, p_value, std_err):
        self.xdata = xdata
        self.slope = slope
        self.intercept = intercept
        self.r_value = r_value
        self.p_value = p_value
        self.std_err = std_err

    def __repr__(self):
        return "Slope: {:.3f}, Intercept: {:.3f}, R: {:.3f}, P: {:.3f}, Err: {:.3f}".format(self.slope, self.intercept, self.r_value, self.p_value, self.std_err)

    def __repr_html__(self):
        return "<h3>Slope: {:.3f}, Intercept: {:.3f}, R: {:.3f}, P: {:.3f}, Err: {:.3f}</h3>".format(self.slope, self.intercept, self.r_value, self.p_value, self.std_err)

    def plot(self,show=False):
        ydata = [self.slope*x + self.intercept for x in self.xdata]
        plt.plot(self.xdata,ydata,label="Reg({:.3f}x + {:.3f})".format(self.slope,self.intercept))
        plt.legend()
        if show:
            plt.show()
