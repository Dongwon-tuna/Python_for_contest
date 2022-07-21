import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt

def canny(image): #Canny 해주기 위한 알고리즘
    gray = cv2.cvtColor(lane_image,cv2.COLOR_RGB2GRAY) #흑백을 반전시키는 이유는 차선을 분석할 때 보다 쉽게 차선을 검출하기 위함, RGB는 3 Channel, Gray는 1 Channel
    blur = cv2.GaussianBlur(gray, (5,5),0)#가우시안 블러를 활용하면 노이즈 줄임(가우스 함수로 이미지 블러링)
    canny = cv2.Canny(blur,50,150)#Canny활용하여 이미지 및 영상의 윤곽선만 보여줌
    return canny

def region_of_interest(img): #도로의 지역을 마스크를 통하여 표시
    height = img.shape[0]
    polygons = np.array([
        [(600, height), (1200, height), (900,400)]
        ])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(canny, mask)
    return masked_image

def display_lines(img, lines):
    line_image = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1),(x2, y2), (255,0,0), 10)
    return line_image   



img = cv2.imread("C:/Users/Dongwon/Documents/GitHub/Python_for_contest/OpenCV/imgs/Road_in_Norway.jpg")
lane_image = np.copy(img)
canny = canny(lane_image)
cropped_image = region_of_interest(canny)
lines  = cv2.HoughLinesP(cropped_image, 2, np.pi/180,100 )
line_image = display_lines(lane_image, lines)

if img is None: #사진의 경로가 옳지 않거나, 사진에 오류가 있는 경우 예외처리 해줌
    print('Image load failed')
    sys.exit()

#plt.imshow(canny) 
#plt.show()
cv2.imshow("result", line_image )
cv2.waitKey(0)


