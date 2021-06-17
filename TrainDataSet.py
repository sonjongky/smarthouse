from imutils import paths
import face_recognition
import pickle
import cv2
import os
import imutils            
#get paths of each file in folder named Images
#Images here contains my data(folders of various persons)
dataSet =r"C:\Users\ADMIN\Desktop\New folder\doan\Dataset"
knownEncodings = []
knownNames = []
for root, dirs, files in os.walk(dataSet, topdown=False):# root ,thu muc,file
    
        for f in files:
            img= cv2.imread(root+"\\"+f)
            name = f.split(".")[0]
           # print("file:",f)
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(rgb, width=750)
            #Use Face_recognition to locate faces
            boxes = face_recognition.face_locations(rgb)# mode=hog
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            
            # loop over the encodings
            for encoding in encodings:
                print(name)
                knownEncodings.append(encoding)
                knownNames.append(name)
   

data = {"encodings": knownEncodings, "names": knownNames}
#use pickle to save data into a file for later use
f = open("face_data_son", "wb")
"""
g=open("face_encodes1","wb")
g.write(pickle.dumps(knownEncodings))

h=open("y_label1","wb")
h.write(pickle.dumps(knownNames))
"""
f.write(pickle.dumps(data))
f.close()
#g.close()

      
       

