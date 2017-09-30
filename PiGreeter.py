""" Main file of the project"""
import wave

import numpy as np
import cv2
import cv2.face as face
import os
import re
#import pyaudio

def detect_eyes(cascade, grayscale):
    "Detects eyes in a grayscale image"
    pass

def detect_faces(cascade, grayscale):
    "Detects faces using a haarcascade in a grayscale image"
    return cascade.detectMultiScale(
        grayscale,
        scaleFactor=1.2,
        minNeighbors=5
    )

def load_images_labels(path, cascade):
    "Loads images from dataset"

    images_paths = [os.path.join(path, f) for f in os.listdir(path)]

    images = []
    labels = []
    label = -1
    personName = ""
    for image_path in images_paths:
        img = cv2.imread(image_path)
        newPerson = os.path.split(image_path)[1].split('_')[0]
        if newPerson != personName:
            personName = newPerson
            label = label + 1
        #label = int( re.findall(r'\d+', os.path.split(image_path)[1]) )
        faces = detect_faces(cascade, img)
        for (x, y, w, h) in faces:
            image_resized = cv2.resize( img[y: y + h, x: x + w], (128, 128) )
            image_resized = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
            images.append(image_resized)
            labels.append(label)
            cv2.imshow("Adding faces to training set...", image_resized)
            cv2.waitKey(500)

    cv2.destroyAllWindows()
    return images, labels

def process_faces(faces, img):
    "Crops image to separates faces"
    i = 0
    f = []
    for (x, y, w, h) in faces:
        f.append( img[y:y + h, x:x + w] )
    
    return f

def draw_faces(faces, img):
    "Draws rectanges around faces"
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

def recognize_faces(faces, recognizer, frame):
    "Recognize faces in a list and reacts"
    for (x, y , w, h) in faces:
        nbr_predicted = recognizer.predict(frame[y:y + h, x:x + h])
        if nbr_predicted == 0:
            print("Axel")
        elif nbr_predicted == 1:
            print("Delphine")
        elif nbr_predicted == 2:
            print("Guillaume")
        elif nbr_predicted == 3:
            print("Hubert")
        else:
            print("Oups")

if __name__ == "__main__":
    """ main
    The flow of this program will be the following:
        1. Grab a frame from the webcam
        2. Detect faces in the frame (haarcascade)
        3. Preprocess faces (histogram equalization)
        4. Recognize faces (LBPH)
        5. Output appropriate greeting (pyaudio ? espeek ?)
    """
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    recognizer = face.createLBPHFaceRecognizer()

    # Train
    images, labels = load_images_labels("./trainingData", face_cascade)
    recognizer.train( images, np.array(labels) )

    while True:
        ret, frame = cap.read()
        if ret is False:
            print("End of file")
            break
        else:
            if 3 == len(frame.shape):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif 4 == len(frame.shape):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
            else:
                gray = frame
        
        # Histogram equalization - consider using CLAHE if does not work well
        gray = cv2.equalizeHist(gray)

        # Add flag to only look for one face at a time ? 
        faces = detect_faces(face_cascade, gray)
        draw_faces(faces, frame)

        # Recognize !
        recognize_faces(faces, recognizer, gray)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("Video", frame)

    cap.release()
    cv2.destroyAllWindows()