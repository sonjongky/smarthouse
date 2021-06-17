from imutils import paths
import face_recognition
import pickle
import cv2
import os
 
#get paths of each file in folder named Images
#Images here contains my data(folders of various persons)
imagePaths = list(paths.list_images(r'C:\Users\Admin\Desktop\thong'))
knownEncodings = []
knownNames = []
# loop over the image paths
try:
    for (i, imagePath) in enumerate(imagePaths):
       # print(i,imagePaths)
        # extract the person name from the image path
        name = imagePath.split(os.path.sep)[-1].split(".")[0]
        print(name)
        # load the input image and convert it from BGR (OpenCV ordering)c
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #Use Face_recognition to locate faces
        boxes = face_recognition.face_locations(rgb,model='hog')#hog
        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)
        # loop over the encodings
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)
except:
    print("Loi :")
#save emcodings along with their names in dictionary data
data = {"encodings": knownEncodings, "names": knownNames}
#use pickle to save data into a file for later use
f = open("face_enc_kin", "wb")
f.write(pickle.dumps(data))
f.close()