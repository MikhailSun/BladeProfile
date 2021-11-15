import geometry_primitives as gp
import numpy as np
import makecharts as mc
from matplotlib import pyplot as plt
from scipy.interpolate import UnivariateSpline

class profile:
        def __init__(self,betta1, betta2, chord, gamma):
                self.betta1=betta1
                self.betta2 = betta2
                self.chord=chord
                self.gamma=gamma
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

        def set_thikness(self,x_thikness, y_thikness):
                self.thikness=UnivariateSpline(x_thikness, y_thikness, s=0.1)
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
                self.LE_fi_min=fi_min
                self.LE_fi_max = fi_max

        def prepare_trailing_edge(self):
                # расчет выходной кромки
                OUTLET_X, OUTLET_Y = self.get_camber_line_coordinates(1)
                OUTLET_R  = self.thikness(1) / 2
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
                self.TE_fi_min=fi_min
                self.TE_fi_max = fi_max

        def get_LE_coordinates(self,t):
                L=self.LE_fi_max-self.LE_fi_min
                fi=t*L+self.LE_fi_min
                return self.INLET_circ.get_coordinates(fi)

        def get_TE_coordinates(self,t):
                L=self.TE_fi_max-self.TE_fi_min
                fi=t*L+self.TE_fi_min
                return self.OUTLET_circ.get_coordinates(fi)

        def get_camber_line_coordinates(self,t):
                x,y,z= self.camber_line.get_coordinates(t)
                return x,y

        def get_suction_side_coordinates(self,t):
                x0, y0 = self.get_camber_line_coordinates(t)
                normal = self.camber_line.get_eq_of_normal_in_pnt(t)
                return normal.get_cooordinates_by_offset(x0, self.thikness(t) / 2)

        def get_pressure_side_coordinates(self, t):
                x0, y0 = self.get_camber_line_coordinates(t)
                normal = self.camber_line.get_eq_of_normal_in_pnt(t)
                return normal.get_cooordinates_by_offset(x0, -self.thikness(t) / 2)

        def build_profile(self):
                x_or_y_max = max(self.points[3][0], self.points[3][1])
                xlim = (0 - 0.1 * x_or_y_max, x_or_y_max * 1.1)
                ylim = (0 - 0.1 * x_or_y_max, x_or_y_max * 1.1)

                # средняя линия
                X = [];Y = []
                # спинка и корытце
                X_line = []; Y_line = []
                X_line2 = []; Y_line2 = []
                X_LE = []; Y_LE = []
                X_TE = []; Y_TE = []

                for t in np.arange(0, 1.00001, 0.001):
                        x,y=self.get_camber_line_coordinates(t)
                        X.append(x); Y.append(y)
                        x_offset, y_offset =self.get_pressure_side_coordinates(t)
                        x_offset2, y_offset2 =self.get_suction_side_coordinates(t)
                        X_line.append(x_offset); Y_line.append(y_offset)
                        X_line2.append(x_offset2); Y_line2.append(y_offset2)
                        x_LE, y_LE =self.get_LE_coordinates(t)
                        X_LE.append(x_LE); Y_LE.append(y_LE)
                        x_TE, y_TE =self.get_TE_coordinates(t)
                        X_TE.append(x_TE); Y_TE.append(y_TE)

                Fig = mc.Chart(points_for_plot=[{'x': X_LE, 'y': Y_LE, 'lw': 1},
                                                {'x': X_TE, 'y': Y_TE, 'lw': 1},
                                                {'x': X, 'y': Y, 'lw': 0.4, 'ls': '--'},
                                                {'x': X_line, 'y': Y_line, 'lw': 1},
                                                {'x': X_line2, 'y': Y_line2, 'lw': 1}], title='Blade', xlim=xlim,
                               ylim=ylim, xlabel='X', ylabel='Y', dpi=150, figure_size=(5, 5))

                plt.show()


#
# def build_blade():
#
#         thikness = UnivariateSpline(x_thikness, y_thikness, s=0.1)
#         X_thikness=[]; Y_thikness=[]
#         # for t in np.arange(0,1.00001,0.001):
#         #         th = thikness(t)
#         #         X_thikness.append(t)
#         #         Y_thikness.append(th)
#         # Fig2=mc.Chart(points_for_plot=[{'x':X_thikness,'y':Y_thikness}], points_for_scatter=[{'x':x_thikness,'y':y_thikness}],title='Thikness',xlabel='X',ylabel='Y',dpi=150,figure_size=(10,10))
#
#         L_inlet=chord/3
#         x1=np.sin(betta1)*L_inlet
#         y1=np.cos(betta1)*L_inlet
#
#         x3=np.sin(gamma)*chord
#         y3=np.cos(gamma)*chord
#
#         L_outlet=chord/3
#         x2=x3-np.sin(betta2)*L_outlet
#         y2=y3-np.cos(betta2)*L_outlet
#
#
#         points=[[0., 0., 0.],
#                 [x1, y1, 0.],
#                 [x2, y2, 0.],
#                 [x3, y3, 0.]]
#         # X_points=[x[0] for x in points]
#         # Y_points=[x[1] for x in points]
#         curve = gp.Bezier(points)
#         # x0, y0, z0 = curve.get_coordinates(0.01)
#         # normal = curve.get_eq_of_normal_in_pnt(0.01)
#         # X_norm=[]; Y_norm=[]
#         # for _th in np.arange(-1, 1, 0.001):
#         #         x,y=normal.get_cooordinates_by_offset(x0, _th)
#         #         X_norm.append(x)
#         #         Y_norm.append(y)
#
#
#
#         #средняя линия
#         X=[]; Y=[]; Z=[]
#         for t in np.arange(0,1.00001,0.001):
#                 x,y,z=curve.get_coordinates(t)
#                 X.append(x)
#                 Y.append(y)
#                 Z.append(z)
#
#         #спинка и корытце
#         X_line=[]; Y_line=[]
#         X_line2=[]; Y_line2=[]
#         for t in np.arange(0,1.00001,0.001):
#                 x0, y0, z0 = curve.get_coordinates(t)
#                 normal = curve.get_eq_of_normal_in_pnt(t)
#                 x_offset, y_offset=normal.get_cooordinates_by_offset(x0, thikness(t)/2)
#                 x_offset2, y_offset2=normal.get_cooordinates_by_offset(x0, -thikness(t)/2)
#                 X_line.append(x_offset)
#                 Y_line.append(y_offset)
#                 X_line2.append(x_offset2)
#                 Y_line2.append(y_offset2)
#
#
#         #расчет входной кромки
#         INLET_X, INLET_Y, _temp=curve.get_coordinates(0)
#         INLET_R=thikness(0)/2
#         INLET_circ=gp.Circle(INLET_X, INLET_Y, INLET_R)
#         norm1=curve.get_eq_of_normal_in_pnt(0)
#         _x1,_y1=norm1.get_cooordinates_by_offset(INLET_X,INLET_R)
#         fi1= INLET_circ.find_nearest_fi_by_coordinates(_x1, _y1)
#         _x2,_y2=norm1.get_cooordinates_by_offset(INLET_X,-INLET_R)
#         fi2= INLET_circ.find_nearest_fi_by_coordinates(_x2, _y2)
#         fi_min=min(fi1, fi2); fi_max=max(fi1, fi2)
#         x_temp, y_temp, _temp = curve.get_coordinates(-0.01)
#         fi_mid=INLET_circ.find_nearest_fi_by_coordinates(x_temp, y_temp)
#         if fi_mid > fi_max:
#                 fi_min+=2*np.pi
#                 fi_min, fi_max = fi_max, fi_min
#         elif fi_mid<fi_min:
#                 fi_max -= 2 * np.pi
#                 fi_min, fi_max = fi_max, fi_min
#         X_circle1=[]; Y_circle1=[]
#         for fi in np.arange(fi_min, fi_max, 0.001):
#                 x, y =INLET_circ.get_coordinates(fi)
#                 X_circle1.append(x)
#                 Y_circle1.append(y)
#
#         #расчет выходной кромки
#         OUTLET_X, OUTLET_Y, _temp=curve.get_coordinates(1)
#         OUTLET_R=thikness(1)/2
#         OUTLET_circ=gp.Circle(OUTLET_X, OUTLET_Y, OUTLET_R)
#         norm2=curve.get_eq_of_normal_in_pnt(1)
#         _x1,_y1=norm2.get_cooordinates_by_offset(OUTLET_X,OUTLET_R)
#         fi1= OUTLET_circ.find_nearest_fi_by_coordinates(_x1, _y1)
#         _x2,_y2=norm2.get_cooordinates_by_offset(OUTLET_X,-OUTLET_R)
#         fi2= OUTLET_circ.find_nearest_fi_by_coordinates(_x2, _y2)
#         fi_min=min(fi1, fi2); fi_max=max(fi1, fi2)
#         x_temp, y_temp, _temp = curve.get_coordinates(1.01)
#         fi_mid=OUTLET_circ.find_nearest_fi_by_coordinates(x_temp, y_temp)
#         if fi_mid > fi_max:
#                 fi_min+=2*np.pi
#                 fi_min, fi_max = fi_max, fi_min
#         elif fi_mid<fi_min:
#                 fi_max -= 2 * np.pi
#                 fi_min, fi_max = fi_max, fi_min
#         X_circle2=[]; Y_circle2=[]
#         for fi in np.arange(fi_min, fi_max, 0.001):
#                 x, y =OUTLET_circ.get_coordinates(fi)
#                 X_circle2.append(x)
#                 Y_circle2.append(y)
#
#
#         x_or_y_max=max(x3, y3)
#         xlim=(0-0.1*x_or_y_max, x_or_y_max*1.1)
#         ylim=(0-0.1*x_or_y_max, x_or_y_max*1.1)
#         Fig=mc.Chart(points_for_plot=[{'x':X_circle1,'y':Y_circle1,'lw':1},{'x':X_circle2,'y':Y_circle2,'lw':1},{'x':X,'y':Y, 'lw':0.4, 'ls':'--'}, {'x':X_line,'y':Y_line,'lw':1}, {'x':X_line2,'y':Y_line2,'lw':1}],title='Blade',xlim=xlim,ylim=ylim,xlabel='X',ylabel='Y',dpi=150,figure_size=(5,5))
#
#
#         plt.show()