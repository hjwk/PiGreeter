""" Main file of the project"""
import wave

import numpy as np
import cv2
import cv2.face as face
import os
import re
#import pyaudio

import gui

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
    names = []
    label = -1
    personName = ""
    for image_path in images_paths:
        img = cv2.imread(image_path)
        newPerson = os.path.split(image_path)[1].split('_')[0]
        if newPerson != personName:
            personName = newPerson
            names.append(personName)
            label = label + 1
        faces = detect_faces(cascade, img)
        for (x, y, w, h) in faces:
            image_resized = cv2.resize( img[y: y + h, x: x + w], (128, 128) )
            image_resized = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
            images.append(image_resized)
            labels.append(label)
            cv2.imshow("Adding faces to training set...", image_resized)
            cv2.waitKey(50)

    cv2.destroyAllWindows()
    return images, labels, names

def process_faces(faces, img):
    "Crops image to separates faces"
    f = []
    for (x, y, w, h) in faces:
        f.append( img[y:y + h, x:x + w] )
    
    return f

def recognize_faces(faces, recognizer, frame):
    "Recognize faces in a list and reacts"
    nbr_predicted = []
    for (x, y, w, h) in faces:
        nbr_predicted.append(recognizer.predict(frame[y:y + h, x:x + h]))
 
    return nbr_predicted

def load_names():
    "Loads people's names from the names.yml file"
    with open('names.yml') as f:
        names = f.read().splitlines()

    return names

def save_names(names):
    "Saves people's names in a .yml file to be loaded later"
    namesFile = open("names.yml", 'w')
    for name in names:
        namesFile.write(name + '\n')
    
    namesFile.close()

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

    # Load model or train it
    try:
        print("Loading existing model")
        recognizer.load("trainedModel.yml")
        names = load_names()
    except:
        print("Training model from photos")
        images, labels, names = load_images_labels("./trainingData", face_cascade)
        recognizer.train( images, np.array(labels) )

    while True:
        ret, frame = cap.read()
        if ret is False:
            print("End of file/Camera not found")
            break
        else:
            if 3 == len(frame.shape):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif 4 == len(frame.shape):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
            else:
                gray = frame
        
        # Draw gui
        gui.drawString("MODE: Detection", frame, (0, -20), (10, 10, 250), 1.1, cv2.FONT_HERSHEY_COMPLEX, 1)

        # Histogram equalization - consider using CLAHE if does not work well
        gray = cv2.equalizeHist(gray)

        # Add flag to only look for one face at a time ? 
        faces = detect_faces(face_cascade, gray)
        gui.draw_faces(faces, frame)

        # Recognize !
        nbrs = recognize_faces(faces, recognizer, gray)
        for nbr in nbrs: 
            gui.drawString("Recognized " + names[nbr], frame, (0, -5), (50, 50, 200), 0.6, cv2.FONT_HERSHEY_COMPLEX, 1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            recognizer.save("trainedModel.yml")
            save_names(names)
            break

        cv2.imshow("PiGreeter", frame)

    cap.release()
    cv2.destroyAllWindows()