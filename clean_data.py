import cv2
import glob
import pandas as pd
# from pandas import DataFrame
import numpy as np
import os


#Directories
data_dir = "Data/Data_Training/"
labels_file = "Data/training_GT_labels_v2.json"
save_path = "Data/saved_GT_labels.json"

labels = pd.read_json(labels_file)
images_reg = data_dir + "*.JPG"
images_path = sorted(glob.glob(images_reg))

at_savepoint = False
print "Run"

for path in images_path:
    print path
    filename = (os.path.basename(path))
    print filename
    if filename == "IMG_3660.JPG":
        at_savepoint = True

    if at_savepoint:
        coords = np.array(labels.loc[0][filename])
        coords = np.reshape(coords, (-1, 2))

        print coords

        img = cv2.imread(path)
        img = cv2.polylines(img, [np.int32(coords)], True, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.imshow("img", img)
        # cv2.waitKey()
        key = cv2.waitKey()

        if key == ord(' '):
            print "Bad image - removing " + path
            print labels.head(0)
            del labels[filename]
            print labels.head(0)
            os.remove(path)
            labels.to_json(save_path)