import face_recognition
import imutils
import pickle
import time
import cv2
import os
import asyncio
import numpy as np
from imutils.video  import VideoStream
from imutils.video import FPS
import serial                                    # import serial library
import websockets
from threading import Thread
import threading
#mo cong COM6
#arduino = serial.Serial(port="COM6",baudrate= 9600)   # create serial object named arduino
#Đường dẫn hiện tại
current_path=os.getcwd()
#biến kiểm tra người hợp lệ (chủ ngôi nhà)
isOwn=False  
# time trước
prev_frame_time = 0
#Font chữ
font = cv2.FONT_HERSHEY_SIMPLEX
font = cv2.FONT_HERSHEY_DUPLEX

####Server  esp
# importing the requests library
import requests
  
# api-endpoint
URL = "http://192.168.1.105:3000"
  

  
# defining a params dict for the parameters to be sent to the API
PARAMS = None




uri='ws://192.168.1.105:3000'
#ws= WebSocket('ws://'+URL+'/ws')

#load DataSet
data = pickle.loads(open(r'face_data_son', "rb").read())


count=0
#URl video
url = "http://192.168.1.184:8080/video"

#Lấy Video từ Url

#camera = VideoStream(url,framerate=32,resolution=(250,180)).start()

#Lấy video
#cap=cv2.VideoCapture(0)
vs = VideoStream(src=0).start()
#Mở cửa 

async def hello(uri,data):
    async with websockets.connect(uri) as websocket:
        await websocket.send(str(data))
       




async def RunServo_Open():
    pos_close=0
    #Góc mở cửa : 0 -> 180
    pos_open=90
    a={"value":pos_open}
   # arduino.write(str(pos_open).encode())                          # write position to serial port
    
    #r = requests.get(url = URL, params = a)
    async with websockets.connect(uri) as websocket:
      await websocket.send(str(pos_open))
    
       # await websocket.recv()


   
    print("Mo cua :_____________________________________")
    time.sleep(1)
               # read serial port for arduino echo
   # arduino.write(str(pos_close).encode()) 
   # print("Dong cua :___")  


async def RunServo_Close():
    pos_close=0
    pos_open=90
   # arduino.write(str(pos_close).encode())                          # write position to serial port
    a={"value":pos_close}
   # arduino.write(str(pos_open).encode())                          # write position to serial port


    async with websockets.connect(uri) as websocket:
      await websocket.send(str(pos_close))
     
    
    print("Đang đóng cửa :_______________________________")
    time.sleep(1)
               # read serial port for arduino echo
             
   # arduino.write(str(pos_close).encode()) 
   # print("Dong cua :___")  







t1=None
# time trước
time_pre=None
# time sau
time_next=None
# Mảng time
arr_time=[]



# loop over frames from the video file stream
while True:
    # Người hợp lệ ( chủ nhà)
    if isOwn:
      # Bắt đầu đếm 
      t1=time.time()

      #print("Now:",t1)

    else:
      if t1!=None:
        # Thời gian khuôn mặt hợp lệ ra khỏi Camera
        t2=time.time()-t1
        if t2> 3:# hon 3s dong Servo (Đóng cửa)
          print("Đóng cửa sau :",t2,' s')
          asyncio.get_event_loop().run_until_complete(
            hello(uri,0))
         # servo2.join()
          t1=None
    # Đặt false cho vòng lặp tiếp     
    isOwn=False
    
    # grab the frame from the threaded video stream
    # ret: true or false ( có  ảnh), frame :khung ảnh

    frame=vs.read()
   #ret,frame = cap.read()
    # resize frame 1/4

    frame = cv2.resize(frame, (0, 0), fx=1/2, fy=1/2)
  
    # Chuyển ảnh BGR sang RGB
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    rgb = imutils.resize(rgb, width=750)
   # rgb = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
  #  frame = frame[:,:,::-1]
    # the facial embeddings for face in input
    r = frame.shape[1] / float(rgb.shape[1])
    #Trả về box tọa độ khuôn mặt : x,y,h,w
    face_locations = face_recognition.face_locations(rgb)
    # mã hóa khuôn mặt thành vector 128 chieu
    unknown_face_encodings = face_recognition.face_encodings(rgb, face_locations)

   # print(len(unknown_face_encodings))








    
    names = []
    # loop over the facial embeddings incase
    # we have multiple embeddings for multiple fcaes

    # duyet từng khuon mặt
    for encoding in unknown_face_encodings:
        #print(len(encoding))
       #Compare encodings with encodings in data["encodings"]
       #Matches contain array with boolean values and True for the embeddings it matches closely
       #and False for rest
       #kiêm tra phải khuon mặt trong tập dữ liệu, ngưỡng khoảng cách Euclid=0.4
        matches = face_recognition.compare_faces(data["encodings"],
         encoding,tolerance=0.4)
      #  print("Mathches: ",matches)
        # Mảng khoang cahc Euclid
        facedistance=face_recognition.face_distance(data["encodings"],encoding)
        #print("DIstance :" ,facedistance)
       # print(matches)
        #set name =inknown if no encoding matches
        name = "???"
        # check to see if we have found a match

        #kiemtra chu nha
        


        if True in matches:
            #Find positions at which we get True and store them
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
          #  print("MatchedID :" ,matchedIdxs)
            counts = {}
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                #Check the names at respective indexes we stored in matchedIdxs
                name = data["names"][i]
             #   print("name  : ",name)
                #increase count for the name we got
                counts[name] = counts.get(name, 0) + 1
              #  print(counts[name])
            #set name which has highest count
          #  name=max(counts,key=counts.get)
           # print("COUNT: ",counts)
            conf_min = min([facedistance[i] for i in matchedIdxs])
            # chỉ số của phần tử min trong mảng
            best_match_index = np.argmin(facedistance)
            name=data["names"][best_match_index]
            print("Name:", name)
            print("Do chinh xac :",conf_min)
          
            isOwn  = True
          ##  Run Servo
            

            #time now
            time_pre=time.time()
            

            if len(arr_time)!=0:
              # Giảm số lần Tiến trình mở cửa
              # Thời gian giữa 2 khuôn mặt hợp lệ < 2s thì chỉ cẩn mở cửa 1 lần       
              if time_pre-arr_time[0]>2:
               # servo1 = threading.Thread(target=RunServo_Open)
               # servo1.start()
               # asyncio.run(RunServo_Close())
                asyncio.get_event_loop().run_until_complete(
                  hello(uri,90))
                #servo1.join()
                #print("Time 2 lần hợp lệ:  ____",time_pre-arr_time[0])
               # print(arr_time,time_pre)
                arr_time.clear()

              else:
                arr_time.clear()
                
            else: #else ni cho lần đầu:mảng arr =0 .mở cửa
                #servo1 = threading.Thread(target=RunServo_Open)
               # servo1.start()
                #asyncio.run(RunServo_Open())
                asyncio.get_event_loop().run_until_complete(
                  hello(uri,0))
                #servo1.join()
            arr_time.append(time_pre)


            ### > 2s thi mo cua else time pre=time curr
            

        # update the list of names
       # print("Min conf :",min(facedistance))
        names.append(name)
        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(face_locations, names):
            # rescale the face coordinates
            # draw the predicted face name on the image
            top = int(top * r)
            right = int(right * r)
            bottom = int(bottom * r)
            left = int(left * r)
            crop_img=rgb[top:bottom,left:right]
            #cv2.imshow('detail',crop_img) 
            count=count+1
            cv2.rectangle(frame, (left-20, top-40), (right+20, bottom+20), (255, 0, 0), 2)
            cv2.putText(frame, name, (left , bottom + 15), font, 1.0, (255, 255, 0), 2)
          
    
    
  
  
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()


