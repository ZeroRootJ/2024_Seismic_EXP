import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import LinearNDInterpolator


def draw_horizon(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)

    # print(data)
    # 3. 데이터 추출
    x = []
    y = []
    z = []
    for i in range(len(data)):
        if data[i][2]:
            try:
                temp = int(data[i][2])
                x.append(data[i][0])
                y.append(data[i][1])
                z.append(873-data[i][2])
            except:
                pass

    # TIN 보간된 3D 면 플롯
    global ax
    sc = ax.scatter(x, y, z, c=z, cmap='viridis', marker='o', s=2, alpha=0.6,)


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