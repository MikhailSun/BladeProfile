import numpy as np
import math
from scipy.optimize import minimize
from scipy.optimize import Bounds

class Bezier:
    def __init__(self, points):
        self.pnts=points
        self.size=len(points)-1

    def basis(self, n, k):
        return math.factorial(n) / math.factorial(k) / math.factorial(n - k)

    def get_coordinates(self, t):
        res = []
        for i in range(3):
            j = 0
            _res = 0
            for pnt in self.pnts:
                _res += self.basis(self.size, j) * (1 - t) ** (self.size - j) * t ** j * pnt[i];
                j += 1
            res.append(_res)
        return res

    def get_derivatives(self, t):
        dt=0.00001
        x1,y1,z1=self.get_coordinates(t-dt)
        x2, y2, z2 = self.get_coordinates(t+dt)
        return (x2-x1)/(2*dt), (y2-y1)/(2*dt), (z2-z1)/(2*dt)

    def get_eq_of_normal_in_pnt(self,t):
        x0, y0, z0=self.get_coordinates(t)
        dx0, dy0, dz0 = self.get_derivatives(t)
        if 0<=dy0<0.0000000001:
            dy0=0.0000000001
        elif 0>=dy0>-0.0000000001:
            dy0 = -0.0000000001
        k=-dx0/dy0
        b=y0+x0*dx0/dy0
        return Line(k,b)

class Line:
    def __init__(self, k, b):
        self.k=k
        self.b=b

    def get_coordinates(self, x):
        return self.k*x+self.b

    def get_cooordinates_by_offset(self, x0, offset):
        y0=self.get_coordinates(x0)
        const1=-self.b*self.k + self.k*y0 + x0
        const2=(offset**2*self.k**2 + offset**2 - self.b**2 - 2*self.b*self.k*x0 + 2*self.b*y0 - self.k**2*x0**2 + 2*self.k*x0*y0 - y0**2)**0.5
        const3=(self.k**2 + 1)
        x1=(const1+const2)/const3
        x2=(const1-const2)/const3
        y1 = self.get_coordinates(x1)
        y2 = self.get_coordinates(x2)
        if offset>0:
            # return np.array([x1]), np.array([y1])
            return x1, y1
        else:
            # return np.array([x2]), np.array([y2])
            return x2, y2


class Circle:
    def __init__(self, x0, y0, R):
        self.X0=x0
        self.Y0 = y0
        self.R = R

    def get_coordinates(self,fi):
        x=self.X0+self.R*np.cos(fi)
        y = self.Y0 + self.R * np.sin(fi)
        # return np.array([x]), np.array([y])
        # return float(x), float(y)
        return x,y

    def find_nearest_fi_by_coordinates(self,x,y):
        min_fi=0; max_fi=np.pi/2
        dist=999999999
        root=np.nan
        while (max_fi<=2*np.pi):
            x0=((min_fi+max_fi)/2)
            res=minimize(self.distance_btwn_fi_and_set_coordinates,x0,args=(x,y),bounds=[(min_fi,max_fi)])#Bounds(min_fi,max_fi)
            if res.fun < dist:
                dist=res.fun
                root=res.x
            min_fi+=np.pi/2
            max_fi += np.pi / 2
        return root

    def distance_btwn_fi_and_set_coordinates(self, fi, x, y):
        x1, y1=self.get_coordinates(fi)
        return np.sqrt((x1-x)**2+(y1-y)**2)