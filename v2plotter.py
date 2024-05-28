import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import LinearNDInterpolator


def draw_horizon(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)

    # 3. 데이터 추출
    X = []
    Y = []
    Z = []

    for i in range(len(data)):
        try:
            int(data[i][2])
            if data[i][2] > 10:
                X.append(data[i][0])
                Y.append(data[i][1])
                Z.append(873 - data[i][2])

        except:
            pass

    global ax

    ax.scatter(X, Y, Z, c='green', s=5)


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