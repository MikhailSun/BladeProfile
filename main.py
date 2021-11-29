import numpy as np
import makecharts as mc
from matplotlib import pyplot as plt
import blade
import geometry_primitives as gp

# points = [[0., 0., 0.],
#             [0, 0.5, 0.],
#             [0.5, 1, 0.],
#             [1, 1, 0.]]
# curve = gp.Bezier(points)
# dx,dy,dz=curve.get_derivatives(0)
# print(dx,dy,dz)





# углы входа и выхода для разных сечений
betta1 = [np.deg2rad(65),np.deg2rad(30),np.deg2rad(20)]
betta2 = [np.deg2rad(60),np.deg2rad(50),np.deg2rad(45)]
# длина хорды
chord = [20,15,12]
# угол установки хорды
gamma = list([np.deg2rad(val) for val in [50, 40, 35]])

# функция, задающая толщину вдоль средней линии
x_thikness = np.array([0., 0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.])
# y_thikness = np.array([0., 0.007, 0.0105, 0.0139, 0.0159, 0.0177, 0.0185, 0.0195, 0.02, 0.0195, 0.0181, 0.0152, 0.0112, 0.0067, 0.0037, 0.])
y_thikness = np.array([0.01, 0.01025, 0.0105, 0.0139, 0.0159, 0.0177, 0.0185, 0.0195, 0.02, 0.0195, 0.0181, 0.0152, 0.0112, 0.0067,
         0.0037, 0.0037])

profiles=[]
coordinates_of_profiles=[]
for b1, b2, ch, ga in zip(betta1, betta2, chord, gamma):


    profile=blade.profile(b1, b2, ch, ga)
    profile.set_thikness(x_thikness, ch*y_thikness)
    profiles.append(profile)
    profile.get_center_of_mass(100)
    profile.calculate_coordinates_of_profile(centered=True)
    # profile.build_profile(centered=True) #для построения профилей по одному
    coordinates_of_profiles.append(profile.plot_of_profile[0])

profile.build_profile(plots=coordinates_of_profiles)

XXX=[]; YYY=[]; ZZZ=[]
for prof in coordinates_of_profiles:
    for x in prof['x']:
        XXX.append(float(x))
    for y in prof['y']:
        YYY.append(float(y))
L=len(coordinates_of_profiles[0]['x'])
l1=[0.5]*L; l2=[0.75]*L; l3=[1.]*L
ZZZ=[*l1, *l2, *l3]


fig3d = plt.figure(dpi=150)
ax3d = fig3d.add_subplot(111, projection='3d')
ax3d.set_xlabel('X')
ax3d.set_ylabel('Y')
ax3d.set_zlabel('Z')
ax3d.scatter(XXX, YYY, ZZZ, marker='.', c='blue', s=3)




