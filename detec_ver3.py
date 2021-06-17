import face_recognition
import imutils
import pickle
import time
import cv2
import os
import numpy as np


current_path=os.getcwd()

#find path of xml file containing haarcascade file 
cascPathface = os.path.dirname(
 cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
# load the harcaascade in the cascade classifier
faceCascade = cv2.CascadeClassifier(cascPathface)
# load the known faces and embeddings saved in last file
data = pickle.loads(open(r'D:\FaceDetect\facend\hiii\face_data_k', "rb").read())
font = cv2.FONT_HERSHEY_DUPLEX
print("Streaming started")\

url = "http://192.168.1.184:8080/video"
#cap = cv2.VideoCapture(0)
count=0

# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream
    ##ret, frame = cap.read()
    frame=cv2.imread(r'D:\FaceDetect\facend\hiii\Dataset\Khoa\khoa.13.jpg')
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
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
       
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()