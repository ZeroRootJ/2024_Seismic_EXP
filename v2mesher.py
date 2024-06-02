import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import LinearNDInterpolator
from v2pointcloud import draw_points
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import RANSACRegressor, LinearRegression
from sklearn.preprocessing import StandardScaler
from scipy.spatial import Delaunay

import pickle


def draw_horizon(file_path, ax):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)

    # print(data)
    # 3. 데이터 추출
    points = []
    for i in range(len(data)):
        if data[i][2]:
            try:
                temp = int(data[i][2])
                points.append((data[i][0], data[i][1], 873-data[i][2]))
            except:
                pass
    triangulation = np.array(points)

    x_min, y_min, z_min = triangulation.min(axis=0)
    x_max, y_max, z_max = triangulation.max(axis=0)
    x_range = x_max - x_min
    y_range = y_max - y_min
    z_range = z_max - z_min

    x_vals = np.linspace(x_min, x_max, 1000)
    y_vals = np.linspace(y_min, y_max, 1000)
    # z_vals = np.linspace(z_min, z_max, int(z_range))

    interp = LinearNDInterpolator(triangulation[:, :2], triangulation[:, 2])
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = interp(X, Y)

    # print(X, Y, X)
    # ax.plot_surface(X, Y, Z, cmap='seismic', edgecolor='none')
    # ax.plot_surface(X, Y, Z, edgecolor='none', alpha=0.7, cmap='viridis')
    ax.plot_surface(X, Y, Z, edgecolor='none', alpha=0.7)


fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel('X Axis')
ax.set_ylabel('Z Axis')
ax.set_zlabel('Y Axis')
ax.set_zlim(0, 873)
ax.set_box_aspect([1, 1, 870 / 270])


# See Horizons
files = ['Horizons/savefile_2.pkl', 'Horizons/savefile_4.pkl', 'Horizons/savefile_5.pkl', 'Horizons/savefile_9.pkl',
         'Horizons/savefile_Mark.pkl', 'Horizons/savefile_Moo.pkl']
for f in files:
    draw_horizon(f, ax)


# See Faults

points = pickle.load(open('fault.pkl', 'rb'))
scaler = StandardScaler()
points_scaled = scaler.fit_transform(points)

planes = pickle.load(open('faultplanes.pkl', 'rb'))
colors = plt.cm.Spectral(np.linspace(0, 1, len(planes)))
print(len(planes))
for i, (a, b, c, plane_points) in enumerate(planes):
    # 원래 스케일로 되돌리기
    plane_points_original = scaler.inverse_transform(plane_points)
    # ax.scatter(plane_points_original[:, 0], plane_points_original[:, 1], plane_points_original[:, 2], c=[colors[i]],
    #            marker='o', alpha=0.6, s=1)
    if len(plane_points_original) > 3:  # 최소 3개의 점이 있어야 삼각형 서피스를 만들 수 있음
            hull = Delaunay(plane_points_original[:, :2])
            ax.plot_trisurf(plane_points_original[:, 0], plane_points_original[:, 1], plane_points_original[:, 2], triangles=hull.simplices, color=colors[i], alpha=0.5)


plt.show()