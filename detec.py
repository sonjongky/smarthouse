import face_recognition
import imutils
import pickle
import time
import cv2
import os
from PIL import Image, ImageDraw
#find path of xml file containing    file 
cascPathface = os.path.dirname(
 cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
# load the harcaascade in the cascade classifier
faceCascade = cv2.CascadeClassifier(cascPathface)
# load the known faces and embeddings saved in last file
data = pickle.loads(open(r'D:\FaceDetect\facend\hiii\face_data_k', "rb").read())
 
print("Streaming started")
video_capture = cv2.VideoCapture(0)
# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream
 #   ret, frame = video_capture.read()
    frame=cv2.imread(r'D:\FaceDetect\facend\hiii\Dataset\Khoa\khoa.13.jpg')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
 
    # convert the input frame from BGR to RGB 
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   # lanmark=face_recognition.face_landmarks(rgb)
  #  pil_image = Image.fromarray(frame)
   # for j in lanmark:
    #    d = ImageDraw.Draw(pil_image, 'RGBA')
       #  cv2.circle(frame, lanmark["chin"], 1, (0,255,0), 2)
  #

  #  print(lanmark)
    # the facial embeddings for face in input
    encodings = face_recognition.face_encodings(rgb)
    names = []
    # loop over the facial embeddings incase
    # we have multiple embeddings for multiple fcaes
    for encoding in encodings:
        #print(len(encoding))
       #Compare encodings with encodings in data["encodings"]
       #Matches contain array with boolean values and True for the embeddings it matches closely
       #and False for rest
        matches = face_recognition.compare_faces(data["encodings"],
         encoding,tolerance=0.4)
        print("Mathches: ",matches)
        facedistance=face_recognition.face_distance(data["encodings"],encoding)
        print("DIstance :" ,facedistance)
       # print(matches)
        #set name =inknown if no encoding matches
        name = "Unknown"
        # check to see if we have found a match
        if True in matches:
            #Find positions at which we get True and store them
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            print("MatchedID :" ,matchedIdxs)
            counts = {}
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                #Check the names at respective indexes we stored in matchedIdxs
                name = data["names"][i]
                print("name  : ",name)
                #increase count for the name we got
                counts[name] = counts.get(name, 0) + 1
              #  print(counts[name])
            #set name which has highest count
            print("COUNT: ",counts)
            name = max(counts, key=counts.get)
            print("Name chinh xac :",name)
 
 
        # update the list of names
        names.append(name)
        # loop over the recognized faces
        for ((x, y, w, h), name) in zip(faces, names):
            # rescale the face coordinates
            # draw the predicted face name on the image
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
             0.75, (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()