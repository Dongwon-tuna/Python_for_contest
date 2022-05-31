import cv2
from tracker import *

# Create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("C:\kroad.mp4") #필요한 영상을 첨부하면 된다.

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape
    print(height,width)

    # Extract Region of interest
    #roi = frame[340: 720,500: 800] 
    roi = frame[0: 2000,0: 2000] #움직임을 포착하는 범위
    

    # 1. Object Detection
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 3000:             #area값은 영상의 화질 및 필요에 따라서 조정 가능하다.   대부분의 영상은 100정도??
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)


            detections.append([x, y, w, h])

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        #cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)  #인원수를 세서 박스 위에 표시
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

    #cv2.imshow("roi", roi)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()