import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import LinearNDInterpolator


def draw_horizon(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)

    # 3. 데이터 추출
    points = []
    for i in range(len(data)):
        try:
            int(data[i][2])
            if data[i][2] > 10:
                points.append((data[i][0], data[i][1], 873-data[i][2]))
        except:
            pass

    # 4. TIN 보간을 위한 삼각형화
    triangulation = np.array(points)

    # 5. TIN 보간 수행
    x_min, y_min, z_min = triangulation.min(axis=0)
    x_max, y_max, z_max = triangulation.max(axis=0)
    x_range = x_max - x_min
    y_range = y_max - y_min
    z_range = z_max - z_min

    # 삼각형 보간을 위한 x, y, z 값 배열 생성
    x_vals = np.linspace(x_min, x_max, int(x_range))
    y_vals = np.linspace(y_min, y_max, int(y_range))
    z_vals = np.linspace(z_min, z_max, int(z_range))

    # 6. TIN 보간
    interp = LinearNDInterpolator(triangulation[:, :2], triangulation[:, 2])
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = interp(X, Y)

    # 7. 3D 평면 그리기

    # TIN 보간된 3D 면 플롯
    global ax
    print(X, Y, X)
    ax.plot_surface(X, Y, Z, cmap='seismic', edgecolor='none')


fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('TIN Interpolated 3D Plane')
ax.set_xlabel('X Axis')
ax.set_ylabel('Z Axis')
ax.set_zlabel('Y Axis')
ax.set_zlim(0, 873)
ax.set_box_aspect([1, 1, 870 / 270])


draw_horizon('savefile.pkl')

plt.show()