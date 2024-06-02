import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import DBSCAN
from scipy.spatial import Delaunay
import numpy as np
import pickle
from v2pointcloud import draw_points


fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('TIN Interpolated 3D Plane')
ax.set_xlabel('X Axis')
ax.set_ylabel('Z Axis')
ax.set_zlabel('Y Axis')
ax.set_zlim(0, 873)
ax.set_box_aspect([1, 1, 870 / 270])

x, y, z = draw_points('Horizons/savefile_fault.pkl', 'green', ax)
# draw_horizon('pklfault.pkl','red')

plt.show()