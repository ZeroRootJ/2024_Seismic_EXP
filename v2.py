import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import sys
from matplotlib.widgets import Button, CheckButtons
from scipy.interpolate import interp1d


class DragHandler:
    global points
    def __init__(self, ax):
        self.ax = ax
        self.press = None
        self.cidpress = ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        self.press = (event.xdata, event.ydata)
        print(f"Mouse pressed at: {self.press}")

    def on_release(self, event):
        self.press = None
        print(f"Mouse released at: ({event.xdata}, {event.ydata})")

    def on_motion(self, event):
        if self.press is None:
            return
        if event.inaxes != self.ax:
            return
        xpress, ypress = self.press
        xdata, ydata = event.xdata, event.ydata

        if isXline is True:
            p = (int(event.xdata), current_Xline * 10, int(event.ydata))
            points.append(p)
        else:
            p = (current_Inline * 10, int(event.xdata), int(event.ydata))
            points.append(p)

        draw_annotations()
        # print(f"Mouse dragged to: ({xdata}, {ydata}) with delta: ({dx}, {dy})")


def read_np(data_folder):
    Inline = []
    Xline = []

    for i in range(1, 29):
        i = str(i).zfill(2)
        isection = np.load(os.path.join(data_folder, f"Inline_{i}.npy"))
        Inline.append(isection)


    for i in range(1, 24):
        i = str(i).zfill(2)
        xsection = np.load(os.path.join(data_folder, f"Xline_{i}.npy"))

        Xline.append(xsection)

    return Inline, Xline



def interpolate_points():
    global points, isXline, current_Xline, current_Inline
    X = []
    Y = []
    if isXline is True:
        for p in points:
            if p[1] == current_Xline*10:
                X.append(p[0])
                Y.append(p[2])

        points = [p for p in points if p[1] != current_Xline * 10]
        X_new = np.linspace(0, 270, 271).astype(int)
        f = interp1d(X, Y, kind='linear', fill_value='extrapolate')
        Y_new = f(X_new)

        for i in range(len(X_new)):
            p = (X_new[i], current_Xline*10, Y_new[i])
            points.append(p)
    else:
        for p in points:
            if p[0] == current_Inline*10:
                X.append(p[1])
                Y.append(p[2])

        points = [p for p in points if p[0] != current_Inline * 10]
        X_new = np.linspace(0, 220, 221).astype(int)
        f = interp1d(X, Y, kind='linear', fill_value='extrapolate')
        Y_new = f(X_new)

        for i in range(len(X_new)):
            p = (current_Inline*10, X_new[i], Y_new[i])
            points.append(p)

def on_prev_button_click(event):
    global isXline, current_Xline, current_Inline, Inline, Xline
    if isXline is True:
        if current_Xline > 0:
            current_Xline -= 1
            ax.cla()
            ax.set_title(f'Xline {current_Xline}')
            ax.imshow(Xline[current_Xline], cmap='seismic')
    else:
        if current_Inline > 0:
            current_Inline -= 1
            ax.cla()
            ax.set_title(f'Inline {current_Inline}')
            ax.imshow(Inline[current_Inline], cmap='seismic')
    draw_annotations()


def on_next_button_click(event):
    global isXline, current_Xline, current_Inline, Inline, Xline
    if isXline is True:
        if current_Xline < len(Xline) - 1:
            current_Xline += 1
            ax.cla()
            ax.set_title(f'Xline {current_Xline}')
            ax.imshow(Xline[current_Xline], cmap='seismic')
    else:
        if current_Inline < len(Inline) - 1:
            current_Inline += 1
            ax.cla()
            ax.set_title(f'Inline {current_Inline}')
            ax.imshow(Inline[current_Inline], cmap='seismic')
    draw_annotations()


# Define the callback function
def on_view_change_button_click(label):
    global isXline, current_Xline, current_Inline, Inline, Xline
    # Check the current state of the toggle button
    if isXline is True:
        # If the toggle button is on, change the label to 'Inline'
        isXline = False
        ax.cla()
        ax.set_title(f'Inline {current_Inline}')
        ax.imshow(Inline[current_Inline], cmap='seismic')
        button_view_change.label.set_text('Inline')


    else:
        # If the toggle button is off, change the label to 'Xline'
        isXline = True
        ax.cla()
        ax.set_title(f'Xline {current_Xline}')
        ax.imshow(Xline[current_Xline], cmap='seismic')
        button_view_change.label.set_text('Xline')

    draw_annotations()

def draw_annotations():
    global points, isXline, current_Xline, current_Inline, scatter_plot

    if scatter_plot is not None:
        scatter_plot.remove()

    X = []
    Y = []

    if isXline is True:
        for p in points:
            if p[1] == current_Xline*10:
                X.append(p[0])
                Y.append(p[2])
    else:
        for p in points:
            if p[0] == current_Inline*10:
                X.append(p[1])
                Y.append(p[2])

    scatter_plot = ax.scatter(X, Y, c='green', s=5)
    fig.canvas.draw()


def on_interpolate_button_click(event):
    interpolate_points()
    draw_annotations()


def on_dblclick(event):
    global points, isXline, current_Xline, current_Inline
    if event.dblclick:
        if button_erase.get_status()[0]:
            # Erase points that are +- 5 pixels away from the clicked point
            if isXline is True:
                points = [p for p in points if p[1] != current_Xline*10 or p[0] < event.xdata - 5 or p[0] > event.xdata + 5 or p[2] < event.ydata - 5 or p[2] > event.ydata + 5]
            else:
                points = [p for p in points if p[0] != current_Inline*10 or p[1] < event.xdata - 5 or p[1] > event.xdata + 5 or p[2] < event.ydata - 5 or p[2] > event.ydata + 5]
            #print(points)
        else:
            if isXline is True:
                p = (int(event.xdata), current_Xline*10, int(event.ydata))
                points.append(p)
            else:
                p = (current_Inline*10, int(event.xdata), int(event.ydata))
                points.append(p)
        draw_annotations()


def on_erase_button_click(label):
    #print(button_erase.get_status()[0])
    pass


def on_key_press(event):
    global points, isXline, current_Xline, current_Inline
    if event.key == 'ctrl+z':
        if len(points) > 0:
            points.pop()
            draw_annotations()
    elif event.key == 'enter':
        with open('savefile.pkl', 'wb') as f:
            pickle.dump(points, f)


Inline, Xline = read_np("npData")

isXline = True
scatter_plot = None

current_Xline = 0
current_Inline = 0

points = None
try:
    with open('savefile.pkl', 'rb') as f:
        points = pickle.load(f)
except:
    points = []


fig, ax = plt.subplots(figsize=(8, 8), num='Seismic Exploration Final Project')
ax.set_title(f'Xline {current_Xline}')
ax.imshow(Xline[current_Xline], cmap='seismic')
draw_annotations()

button_next_ax = plt.axes([0.8, 0.05, 0.1, 0.075])  # This creates a new axes where the button will be
button_next = Button(button_next_ax, 'Next')

button_prev_ax = plt.axes([0.7, 0.05, 0.1, 0.075])  # Adjust the position and size as needed
button_prev = Button(button_prev_ax, 'Prev')

button_view_change_ax = plt.axes([0.7, 0.15, 0.2, 0.075])  # Adjust the position and size as needed
button_view_change = Button(button_view_change_ax, 'Inline')

button_interpolate_ax = plt.axes([0.7, 0.25, 0.2, 0.075])
button_interpolate = Button(button_interpolate_ax, 'Interpolate')

button_erase_ax = plt.axes([0.7, 0.35, 0.2, 0.075])  # Adjust the position and size as needed
button_erase = CheckButtons(button_erase_ax, ['Erase'])



button_prev.on_clicked(on_prev_button_click)
button_next.on_clicked(on_next_button_click)
button_view_change.on_clicked(on_view_change_button_click)
button_interpolate.on_clicked(on_interpolate_button_click)
button_erase.on_clicked(on_erase_button_click)

fig.canvas.mpl_connect('button_press_event', on_dblclick)
fig.canvas.mpl_connect('key_press_event', on_key_press)

dh = DragHandler(ax)



plt.show()