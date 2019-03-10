import cv2
import glob
import pandas as pd
# from pandas import DataFrame
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

data_dir = "data/images/me/"
labels_file = "data/images/me/hand_labelled.json"
save_file = "data/images/me/hand_labelled.json"

#Scaling factor to make plot bigger or smaller
resize = 3.5

# If you want to skip ahead, eg to image IMG_0252.JPG, the change to goto_file="IMG_0252.JPG"
# Else goto_file = ""
goto_file = ""

index=range(0,1)
columns=[]

labels = pd.DataFrame(index=index, columns=columns)
if os.path.isfile(labels_file):
    labels = pd.read_json(labels_file)
else:
    f = open(labels_file, "w+")
    f.close()

images_reg = data_dir + "*.JPG"
images_path = sorted(glob.glob(images_reg))


i = 0
idx = 0
selected_points = []
polygon_complete = False
polygon = np.array([])

def press(event):
    print(event.key)
    global idx
    global selected_points
    global polygon

    if event.key == 'right' or event.key == ' ':
        idx = idx+1
        print(idx)
        selected_points = []
        polygon = np.array(selected_points)
        plt.close()

    if event.key == 'left':
        idx = idx-1
        print(idx)
        selected_points = []
        polygon = np.array(selected_points)
        plt.close()

    if event.key == 'escape':
        selected_points = []
        polygon = np.array(selected_points)
        plt.close()

def onclick(event):
    global selected_points
    global polygon_complete
    global polygon
    global img
    global idx

    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))

    point = [int(event.xdata), int(event.ydata)]
    selected_points.append(point)
    print(selected_points)
    polygon = np.array(selected_points)
    plt.close()


    if len(selected_points) == 4:
        print("Done")
        polygon_complete = True
        selected_points = []
        idx = idx+1
        plt.close()


# Skip ahead to image goto_file
json_file = ""
if goto_file != "":
    while json_file != goto_file:
        path = images_path[idx]
        json_file = (os.path.basename(path))
        if json_file != goto_file:
            idx = idx+1

#Resize the plot
fig_size = plt.rcParams["figure.figsize"]
print "Current size:", fig_size
fig_size = [fig_size[0] * resize, fig_size[1] * resize]
plt.rcParams["figure.figsize"] = fig_size

# plt.ion()
# fig = plt.figure()
# ax = fig.add_subplot(111)

while idx < len(images_path):

    path = images_path[idx]
    # print(path)
    filename = (os.path.basename(path))
    print("Labelling image ", filename)
    img = cv2.imread(path)

    fig, ax = plt.subplots()

    fig.canvas.mpl_connect('key_press_event', press)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    img = cv2.polylines(img, [np.int32(polygon)], True, (255, 0, 0), 1, cv2.LINE_AA)
    imgplot = ax.imshow(img)

    plt.show()

    if polygon_complete:
        if filename in labels:
            labels.drop(filename, axis=1, inplace=True)

        labels[filename] = np.array2string(polygon.flatten(), separator=',')
        labels.to_json(save_file)
        # polygon = np.array(selected_points)

    polygon_complete = False
