import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
path = 'database'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
#SVM training model
svm = SVM()svm.fit(X_train, y_train)

Next, we plot the decision boundary and support vectors.

def f(x, w, b, c=0):
    return (-w[0] * x - b + c) / w[1]plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap='user')

# function to map images to database entries
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids #returns vectors of ids and matching image numbers

print ("\n [INFO] Training recognizer....")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi


print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
