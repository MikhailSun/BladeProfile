from scipy.optimize import minimize
import numpy as np
from scipy.optimize import Bounds

def func(x,y,z):
    return (x-z)**2+y

res=minimize(func, 0.5, args=(1.5,1.7), bounds=[(-0.5,3)])

print(res)