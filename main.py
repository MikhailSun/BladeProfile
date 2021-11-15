import numpy as np
import makecharts as mc
from matplotlib import pyplot as plt
import blade
import geometry_primitives as gp

points = [[0., 0., 0.],
            [0, 0.5, 0.],
            [0.5, 1, 0.],
            [1, 1, 0.]]
curve = gp.Bezier(points)
dx,dy,dz=curve.get_derivatives(0)
print(dx,dy,dz)





# углы входа и выхода
betta1 = np.deg2rad(40)
betta2 = np.deg2rad(60)
# длина хорды
chord = 20
# угол установки хорды
gamma = np.deg2rad(50)

# функция, задающая толщину вдоль средней линии
x_thikness = np.array([0., 0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.])
# y_thikness = np.array([0., 0.007, 0.0105, 0.0139, 0.0159, 0.0177, 0.0185, 0.0195, 0.02, 0.0195, 0.0181, 0.0152, 0.0112, 0.0067, 0.0037, 0.])
y_thikness = chord * np.array(
        [0.01, 0.01025, 0.0105, 0.0139, 0.0159, 0.0177, 0.0185, 0.0195, 0.02, 0.0195, 0.0181, 0.0152, 0.0112, 0.0067,
         0.0037, 0.0037])

test_profile = blade.profile(betta1, betta2, chord, gamma)
test_profile.set_thikness(x_thikness, y_thikness)
test_profile.build_profile()
