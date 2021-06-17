import cv2
import numpy as np
import face_recognition as fr
import os
import time
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
print("Nhập tên : ")
name=input()
print("Starting ................")
cap = cv2.VideoCapture(0)
time.sleep(3)
count=1
while True:
        _, frame = cap.read()# _true  or false . img: data lay dc 
        img=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        #img=cv2.imread(r"D:\FaceDetect\facend\face_rec\faces\vy4.png")
        face_locations = fr.face_locations(img,model='hog')
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# convent chuyen anh ve anh xam(du lieu anh,mauGRB(blue,red,green)->gray)
    # faces = face_cascade.detectMultiScale(gray,1.1,3)#nhan dien khuon mat 
        for (top, right, bottom, left) in face_locations: #x,y toa do diem tinh tien ngang doc
        # print(x,y,w,h)fhnfnf
            cv2.rectangle(img, (left-20, top-40), (right+20, bottom+20), (255, 0, 0), 2)
            img_drop=frame[top:bottom,left:right]
            
            if not os.path.exists("Dataset/"+name):
                os.makedirs("Dataset/"+name)
            cv2.imwrite("Dataset/"+name+"/"+name+"."+str(count)+".jpg",img_drop)
            time.sleep(1)
            cv2.imshow("Face",img_drop)   
            count=count+1
            print(count)
        cv2.imshow('DETECTION FACE', frame)
        if count>10:
                break   
        if cv2.waitKey(1) & 0xFF == ord('q'):
             break
    

cap.release() # giai phong bo nho
cv2.destroyAllWindows()  # huy no đi
