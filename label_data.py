import cv2
import glob
import pandas as pd
# from pandas import DataFrame
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

data_dir = "data/images/"
labels_file = "data/images/hand_labelled3.json"
save_file = "data/images/hand_labelled3.json"

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

    print(selected_points)
    point = [int(event.xdata), int(event.ydata)]
    print(point)
    selected_points.append(point)
    print(selected_points)
    polygon = np.array(selected_points)

    plt.close()
    # update_image(img, polygon)

    if len(selected_points) == 4:
        print("done")
        polygon_complete = True
        selected_points = []
        idx = idx+1
        plt.close()


# print labels.iloc[0][0]
# print labels.loc[0]["IMG_0005.JPG"]
# nparr = np.array([1, 2, 3, 4, 5, 6, 7, 8])
# arr = np.array2string(nparr)
# labels["timo"] = arr


while idx < len(images_path):

    path = images_path[idx]
    # print(path)
    filename = (os.path.basename(path))
    print(filename)
    img = cv2.imread(path)

    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('key_press_event', press)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)


    img = cv2.polylines(img, [np.int32(polygon)], True, (255, 0, 0), 5, cv2.LINE_AA)
    imgplot = ax.imshow(img)
    plt.show()

    if polygon_complete:
        if filename in labels:
            labels.drop(filename, axis=1, inplace=True)

        labels[filename] = np.array2string(polygon.flatten(), separator=',')
        labels.to_json(save_file)
        # polygon = np.array(selected_points)

    polygon_complete = False
