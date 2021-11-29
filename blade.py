#TODO! сделать расчет максимального прогиба профиля по заданному параметру
#TODO! сделать расчет горла

import geometry_primitives as gp
import numpy as np
import makecharts as mc
from matplotlib import pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import root_scalar


class profile():
    def __init__(self, betta1, betta2, chord, gamma):
        self.betta1 = betta1
        self.betta2 = betta2
        self.chord = chord
        self.gamma = gamma
        L_inlet = chord / 3
        x1 = np.sin(betta1) * L_inlet
        y1 = np.cos(betta1) * L_inlet
        x3 = np.sin(gamma) * chord
        y3 = np.cos(gamma) * chord
        L_outlet = chord / 3
        x2 = x3 - np.sin(betta2) * L_outlet
        y2 = y3 - np.cos(betta2) * L_outlet
        self.points = [[0., 0., 0.],
                       [x1, y1, 0.],
                       [x2, y2, 0.],
                       [x3, y3, 0.]]
        self.camber_line = gp.Bezier(self.points)
        self.array_of_plots=[]
        self.plot_of_profile=[]
        self.scatter_of_center_of_mass=[]
        self.xc=0.
        self.yc = 0.

    def set_thikness(self, x_thikness, y_thikness):
        self.thikness = UnivariateSpline(x_thikness, y_thikness, s=0.1)
        self.prepare_leading_edge()
        self.prepare_trailing_edge()

    def prepare_leading_edge(self):
        # расчет входной кромки
        INLET_X, INLET_Y = self.get_camber_line_coordinates(0)
        INLET_R = self.thikness(0) / 2
        self.INLET_circ = gp.Circle(INLET_X, INLET_Y, INLET_R)
        norm1 = self.camber_line.get_eq_of_normal_in_pnt(0)
        _x1, _y1 = norm1.get_cooordinates_by_offset(INLET_X, INLET_R)
        fi1 = self.INLET_circ.find_nearest_fi_by_coordinates(_x1, _y1)
        _x2, _y2 = norm1.get_cooordinates_by_offset(INLET_X, -INLET_R)
        fi2 = self.INLET_circ.find_nearest_fi_by_coordinates(_x2, _y2)
        fi_min = min(fi1, fi2);
        fi_max = max(fi1, fi2)
        x_temp, y_temp, _temp = self.camber_line.get_coordinates(-0.01)
        fi_mid = self.INLET_circ.find_nearest_fi_by_coordinates(x_temp, y_temp)
        if fi_mid > fi_max:
            fi_min += 2 * np.pi
            fi_min, fi_max = fi_max, fi_min
        elif fi_mid < fi_min:
            fi_max -= 2 * np.pi
            fi_min, fi_max = fi_max, fi_min
        self.LE_fi_min = fi_min
        self.LE_fi_max = fi_max

    def prepare_trailing_edge(self):
        # расчет выходной кромки
        OUTLET_X, OUTLET_Y = self.get_camber_line_coordinates(1)
        OUTLET_R = self.thikness(1) / 2
        self.OUTLET_circ = gp.Circle(OUTLET_X, OUTLET_Y, OUTLET_R)
        norm2 = self.camber_line.get_eq_of_normal_in_pnt(1)
        _x1, _y1 = norm2.get_cooordinates_by_offset(OUTLET_X, OUTLET_R)
        fi1 = self.OUTLET_circ.find_nearest_fi_by_coordinates(_x1, _y1)
        _x2, _y2 = norm2.get_cooordinates_by_offset(OUTLET_X, -OUTLET_R)
        fi2 = self.OUTLET_circ.find_nearest_fi_by_coordinates(_x2, _y2)
        fi_min = min(fi1, fi2)
        fi_max = max(fi1, fi2)
        x_temp, y_temp, _temp = self.camber_line.get_coordinates(1.01)
        fi_mid = self.OUTLET_circ.find_nearest_fi_by_coordinates(x_temp, y_temp)
        if fi_mid > fi_max:
            fi_min += 2 * np.pi
            fi_min, fi_max = fi_max, fi_min
        elif fi_mid < fi_min:
            fi_max -= 2 * np.pi
            fi_min, fi_max = fi_max, fi_min
        self.TE_fi_min = fi_min
        self.TE_fi_max = fi_max

    def get_LE_coordinates(self, t):
        L = self.LE_fi_max - self.LE_fi_min
        fi = t * L + self.LE_fi_min
        return self.INLET_circ.get_coordinates(fi)

    def get_TE_coordinates(self, t):
        L = self.TE_fi_max - self.TE_fi_min
        fi = t * L + self.TE_fi_min
        return self.OUTLET_circ.get_coordinates(fi)

    def get_camber_line_coordinates(self, t):
        x, y, z = self.camber_line.get_coordinates(t)
        return x, y

    def get_suction_side_coordinates(self, t):
        x0, y0 = self.get_camber_line_coordinates(t)
        normal = self.camber_line.get_eq_of_normal_in_pnt(t)
        return normal.get_cooordinates_by_offset(x0, -self.thikness(t) / 2)

    def get_pressure_side_coordinates(self, t):
        x0, y0 = self.get_camber_line_coordinates(t)
        normal = self.camber_line.get_eq_of_normal_in_pnt(t)
        return normal.get_cooordinates_by_offset(x0, self.thikness(t) / 2)

    # основная функция для получения координат профиля по параметры t от 0 до 1
    def get_coordinates_of_profile(self, t, centered=False):
        t=t%1
        if (0 <= t < 0.25):
            t = (0.25 - t) / 0.25
            x, y = self.get_LE_coordinates(t)
        elif 0.25 <= t < 0.5:
            t = (t - 0.25) / 0.25
            x, y = self.get_suction_side_coordinates(t)
        elif 0.5 <= t < 0.75:
            t = (0.25 - (t - 0.5)) / 0.25
            x, y = self.get_TE_coordinates(t)
        elif 0.75 <= t <= 1:
            t = (0.25 - (t - 0.75)) / 0.25
            x, y = self.get_pressure_side_coordinates(t)
        if centered:
            x=x-self.xc
            y=y-self.yc
        return x, y

    def find_left_pnt_of_profile(self):
        fun = lambda t: self.get_coordinates_of_profile(t)[0]
        res1 = minimize(fun, 0, bounds=[(0, 0.375)])  # Bounds(min_fi,max_fi)
        res2 = minimize(fun, 1, bounds=[(0.875, 1)])
        return res1.x[0] if res1.x < res2.x else res2.x[0]

    def find_right_pnt_of_profile(self):
        fun = lambda t: 1 / self.get_coordinates_of_profile(t)[0]
        res1 = minimize(fun, 0, bounds=[(0.375, 0.875)])  # Bounds(min_fi,max_fi)
        return res1.x[0]

    def calculate_coordinates_of_profile(self, centered=False):
        X = [];
        Y = []
        for t in np.arange(0, 1.00001, 0.001):
            x, y = self.get_coordinates_of_profile(t, centered)
            X.append(x);
            Y.append(y)
        self.plot_of_profile=[{'x': X, 'y': Y, 'lw': 1}, *self.array_of_plots]

    def build_profile(self, plots=[], centered=False):

        if len(plots)>0:
            self.Figure = mc.Chart(points_for_plot=[*plots],
                                   title='Profiles centered', xlabel='X', ylabel='Y', dpi=150, figure_size=(5, 5))
        elif centered:
            x_or_y_max = max(self.points[3][0], self.points[3][1])
            xlim = (0 - 0.1 * x_or_y_max-self.xc, x_or_y_max * 1.1-self.xc)
            ylim = (0 - 0.1 * x_or_y_max-self.yc, x_or_y_max * 1.1-self.yc)
            self.Figure=mc.Chart(points_for_plot=self.plot_of_profile,
                            title='Profile centered', xlim=xlim,
                            ylim=ylim, xlabel='X', ylabel='Y', dpi=150, figure_size=(5, 5))
        else:
            x_or_y_max = max(self.points[3][0], self.points[3][1])
            xlim = (0 - 0.1 * x_or_y_max, x_or_y_max * 1.1)
            ylim = (0 - 0.1 * x_or_y_max, x_or_y_max * 1.1)
            self.Figure = mc.Chart(points_for_plot=self.plot_of_profile,
                                   points_for_scatter=self.scatter_of_center_of_mass,
                                   title='Blade', xlim=xlim,
                                   ylim=ylim, xlabel='X', ylabel='Y', dpi=150, figure_size=(5, 5))
        return self.Figure

    def build_profile_by_parts(self):
        x_or_y_max = max(self.points[3][0], self.points[3][1])
        xlim = (0 - 0.1 * x_or_y_max, x_or_y_max * 1.1)
        ylim = (0 - 0.1 * x_or_y_max, x_or_y_max * 1.1)

        # средняя линия
        X = [];
        Y = []
        # спинка и корытце
        X_line = [];
        Y_line = []
        X_line2 = [];
        Y_line2 = []
        X_LE = [];
        Y_LE = []
        X_TE = [];
        Y_TE = []

        for t in np.arange(0, 1.00001, 0.001):
            x, y = self.get_camber_line_coordinates(t)
            X.append(x);
            Y.append(y)
            x_offset, y_offset = self.get_pressure_side_coordinates(t)
            x_offset2, y_offset2 = self.get_suction_side_coordinates(t)
            X_line.append(x_offset);
            Y_line.append(y_offset)
            X_line2.append(x_offset2);
            Y_line2.append(y_offset2)
            x_LE, y_LE = self.get_LE_coordinates(t)
            X_LE.append(x_LE);
            Y_LE.append(y_LE)
            x_TE, y_TE = self.get_TE_coordinates(t)
            X_TE.append(x_TE);
            Y_TE.append(y_TE)

        return mc.Chart(points_for_plot=[{'x': X_LE, 'y': Y_LE, 'lw': 1},
                                         {'x': X_TE, 'y': Y_TE, 'lw': 1},
                                         {'x': X, 'y': Y, 'lw': 0.4, 'ls': '--'},
                                         {'x': X_line, 'y': Y_line, 'lw': 1},
                                         {'x': X_line2, 'y': Y_line2, 'lw': 1}], title='Blade', xlim=xlim,
                        ylim=ylim, xlabel='X', ylabel='Y', dpi=150, figure_size=(5, 5))

    def get_center_of_mass(self, tolerance=100):

        t_min = self.find_left_pnt_of_profile()
        t_max = self.find_right_pnt_of_profile()
        if t_min>t_max:
            t_max+=1 #эту штуку я ни разу не тестировал
        x_min, _y = self.get_coordinates_of_profile(t_min)
        x_max, _y = self.get_coordinates_of_profile(t_max)
        dx = (x_max - x_min) / tolerance
        fun_to_find_t_thru_x = lambda t, x: x - float(self.get_coordinates_of_profile(t)[0])
        S_entire=0
        S_xc=0
        S_yc=0
        for x_i in np.arange(x_min + dx / 2, x_max * 1.000001, dx):
            t1 = root_scalar(fun_to_find_t_thru_x, args=(x_i), method='toms748', bracket=[t_min, t_max]).root
            y_max=self.get_coordinates_of_profile(t1)[1]
            t2 = root_scalar(fun_to_find_t_thru_x, args=(x_i), method='toms748', bracket=[t_max, t_min+1]).root
            y_min = self.get_coordinates_of_profile(t2)[1]
            S=(y_max-y_min)*dx
            S_xc+=S*x_i
            S_yc+=S*(y_max+y_min)/2
            S_entire+=S
            #ниже - для визуализации алгоритма поиска центра масс
            # self.array_of_plots.append({'x': [x_i-dx/2, x_i+dx/2, x_i+dx/2, x_i-dx/2, x_i-dx/2], 'y': [y_max, y_max, y_min, y_min, y_max],'c':'black', 'lw':0.3, 'ls':'--'})

        self.xc=S_xc/S_entire
        self.yc = S_yc / S_entire
        self.scatter_of_center_of_mass=[{'x':self.xc, 'y':self.yc, 's':100, 'marker':"+", 'c':'red'}]
        print(f"center of mass: x={self.xc} y={self.yc}")
        return self.xc,self.yc



