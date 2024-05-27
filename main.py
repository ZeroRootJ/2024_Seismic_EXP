import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import sys


def draw_guide():
    global horizon_3d
    if len(horizon_3d) > 0:
        prev_horizon = horizon_3d[-1]
        if len(prev_horizon) > 0:
            plt.scatter(*zip(*prev_horizon), color='green', alpha=0.5, s=10)  # Scatter plot data points (x, y
            plt.plot(*zip(*prev_horizon), color='green', alpha=0.5)  # Connect the scatter plot data points
            fig.canvas.draw()


def draw_annotations(alpha=1.0):
    if len(horizon_2d) > 0:
        plt.scatter(*zip(*horizon_2d), color='green', alpha=alpha, s=10)  # Scatter plot data points (x, y
    if len(horizon_2d) > 1:
        plt.plot(*zip(*horizon_2d), color='green', alpha=alpha)  # Connect the scatter plot data points

    fig.canvas.draw()


def remove_annotations():
    for scatter in ax.collections:
        scatter.remove()
    for line in ax.lines:
        line.remove()
    fig.canvas.draw()


def on_dblclick(event):
    global horizon_2d
    if event.dblclick:
        x, y = int(event.xdata), int(event.ydata)
        horizon_2d.append([x, y])

        draw_annotations()


        # Debug
        # print('button=%d, xdata=%f, ydata=%f' %
        #       (event.button, event.xdata, event.ydata))
        # print(horizon_2d)


def on_key_press(event):
    global horizon_2d, current_xline, horizon_3d
    if event.key == 'ctrl+z':
        horizon_2d.pop()
        remove_annotations()
        draw_guide()

        draw_annotations()

        if current_xline > 0:  # Draw the previous annotations
            draw_annotations()

    elif event.key == 'enter':
        ax.cla()
        current_xline += 1
        horizon_3d.append(horizon_2d)

        if current_xline < len(Xline):
            plt.imshow(Xline[current_xline], cmap='seismic')
            horizon_2d = []
            draw_guide()
            fig.canvas.draw()
        else:
            with open('horizon_3d.pkl', 'wb') as f:
                pickle.dump(horizon_3d, f)
            print("Annotations completed")
            sys.exit()
            #print(horizon_3d)
            #print(len(horizon_3d))





Inline = []
Xline = []
# data_folder = os.path.join(os.path.dirname(__file__), 'npData')
data_folder = "npData"

for i in range(1, 29):
    i = str(i).zfill(2)
    isection = np.load(os.path.join(data_folder, f"Inline_{i}.npy"))
    Inline.append(isection)

    # print(isection.shape)
    # plt.figure(figsize=(5,20))  # Create a new figure with size 10x10
    # plt.imshow(isection, cmap='seismic')
    # plt.show()
    # break

for i in range(1, 24):
    i = str(i).zfill(2)
    xsection = np.load(os.path.join(data_folder, f"Xline_{i}.npy"))

    Xline.append(xsection)

    # plt.figure(figsize=(5, 20))  # Create a new figure with size 10x10
    # plt.imshow(xsection, cmap='seismic')
    # plt.savefig("Xline_example.png")
    # plt.show()



# Inline = np.array(Inline)
# Xline = np.array(Xline)
# print(Inline.shape)
# print(Xline.shape)

# print(Xline.max(), Xline.min())

# print(len(Xline))

horizon_3d = []
horizon_2d = []
current_xline = 0

fig, ax = plt.subplots(figsize=(12, 12), num='Seismic Exploration Final Project')
plt.imshow(Xline[current_xline], cmap='seismic')
fig.canvas.mpl_connect('button_press_event', on_dblclick)
fig.canvas.mpl_connect('key_press_event', on_key_press)

plt.show()



# print(Inline[0].shape)