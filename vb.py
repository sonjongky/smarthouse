import cv2
frame=cv2.imread('Sơn.1.jpg')
frame = cv2.resize(frame, (0, 0), fx=1/2, fy=1/2)
cv2.imshow("aaa",img)