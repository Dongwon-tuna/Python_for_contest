import cv2
import numpy as np

net = cv2.dnn.readNet("C:\yolov3.weights","C:\yolov3.cfg")
classes = []

with open("C:\coco.names","r") as f:
    classes = [line.strip() for line in f.readlines()]

print(classes)
layer_names = net.getLayerNames()
outputlayers = [layer_names[i- 1] for i in net.getUnconnectedOutLayers()]


img = cv2.imread("C:\room.jpg")

cv2.imshow("Image",img)

cv2.destroyAllWindows()




