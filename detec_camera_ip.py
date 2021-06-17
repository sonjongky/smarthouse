import face_recognition
import imutils
import pickle
import time
import cv2
import os
import numpy as np
from imutils.video  import VideoStream
from imutils.video import FPS
import serial                                    # import serial library

from threading import Thread
import threading

arduino = serial.Serial(port="COM6",baudrate= 9600)   # create serial object named arduino
current_path=os.getcwd()

isOwn=False  # chu nha

prev_frame_time = 0
font = cv2.FONT_HERSHEY_SIMPLEX
# used to record the time at which we processed current frame
new_frame_time = 0









#find path of xml file containing haarcascade file 
cascPathface = os.path.dirname(
 cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
# load the harcaascade in the cascade classifier
faceCascade = cv2.CascadeClassifier(cascPathface)
# load the known faces and embeddings saved in last file
data = pickle.loads(open('face_data_2', "rb").read())
font = cv2.FONT_HERSHEY_DUPLEX
print("Streaming started")

url = "http://192.168.1.27:8080/video"
camera = VideoStream(url,framerate=32,resolution=(250,180)).start()
count=0




def RunServo_Open():
    pos_close=0
    pos_open=90
    arduino.write(str(pos_open).encode())                          # write position to serial port
    print("Mo cua :___")
    time.sleep(1)
               # read serial port for arduino echo
   # arduino.write(str(pos_close).encode()) 
   # print("Dong cua :___")  


def RunServo_Close():
    pos_close=0
    pos_open=90
    arduino.write(str(pos_close).encode())                          # write position to serial port
    print("Dong cua :___")
    time.sleep(1)
               # read serial port for arduino echo
   # arduino.write(str(pos_close).encode()) 
   # print("Dong cua :___")  







t1=None

time_pre=None
time_next=None

arr_time=[]


# loop over frames from the video file stream
while True:
    
    if isOwn:
      t1=time.time()
      print("Now:",t1)
    else:
      if t1!=None:
        t2=time.time()-t1
        if t2> 3:# hon 3s dong Servo
          print("tao dong cua",t2)
          servo2 = threading.Thread(target=RunServo_Close)
          servo2.start()
          servo2.join()
          t1=None
    isOwn=False
    t=time.time()
    # grab the frame from the threaded video stream
    frame = camera.read()
    frame = cv2.resize(frame, (0, 0), fx=1/4, fy=1/4)
 #   frame=cv2.imread(r"D:\FaceDetect\facend\face_rec\tung2.jpg")
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    
   # rgb = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
  #  frame = frame[:,:,::-1]
    # the facial embeddings for face in input
    face_locations = face_recognition.face_locations(rgb)
    unknown_face_encodings = face_recognition.face_encodings(rgb, face_locations)

   # print(len(unknown_face_encodings))








    
    names = []
    # loop over the facial embeddings incase
    # we have multiple embeddings for multiple fcaes
    for encoding in unknown_face_encodings:
        #print(len(encoding))
       #Compare encodings with encodings in data["encodings"]
       #Matches contain array with boolean values and True for the embeddings it matches closely
       #and False for rest
        matches = face_recognition.compare_faces(data["encodings"],
         encoding,tolerance=0.4)
      #  print("Mathches: ",matches)
        facedistance=face_recognition.face_distance(data["encodings"],encoding)
        print("DIstance :" ,facedistance)
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
            best_match_index = np.argmin(facedistance)
            name=data["names"][best_match_index]
            print("Name:", name)
            print("Do chinh xac :",conf_min)
          
            isOwn  = True
          ##  Run Servo
            


            time_pre=time.time()
            
            if len(arr_time)!=0:
              if time_pre-arr_time[0]>1:
                servo1 = threading.Thread(target=RunServo_Open)
                servo1.start()
                servo1.join()
                arr_time.clear()
              else:
                arr_time.clear()
                
            else:
                servo1 = threading.Thread(target=RunServo_Open)
                servo1.start()
                servo1.join()
            arr_time.append(time_pre)


            ### > 2s thi mo cua else time pre=time curr
            

        # update the list of names
        print("Min conf :",min(facedistance))
        names.append(name)
        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(face_locations, names):
            # rescale the face coordinates
            # draw the predicted face name on the image
            crop_img=rgb[top:bottom,left:right]
            cv2.imshow('detail',crop_img) 
            count=count+1
            cv2.rectangle(frame, (left-20, top-40), (right+20, bottom+20), (255, 0, 0), 2)
            cv2.putText(frame, name, (left , bottom + 15), font, 1.0, (255, 255, 0), 2)
          
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    # converting the fps into integer
    fps = int(fps)
  
    # converting the fps to string so that we can display it on frame
    # by using putText function
    fps = str(fps)
  
    # puting the FPS count on the frame
    cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_4)   
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


