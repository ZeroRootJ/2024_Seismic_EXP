import pickle
import matplotlib.pyplot as plt

def draw_points(file_path, color, ax):
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
    sc = ax.scatter(x, y, z, c=color, marker='o', s=1, alpha=0.2,)
    return x, y, z

if __name__ == '__main__':
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('TIN Interpolated 3D Plane')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Z Axis')
    ax.set_zlabel('Y Axis')
    ax.set_zlim(0, 873)
    ax.set_box_aspect([1, 1, 870 / 270])

    draw_points('savefile4.pkl', 'green')
    # draw_horizon('pklfault.pkl','red')

    plt.show()