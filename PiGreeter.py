""" Main file of the project"""
import wave

import numpy as np
import cv2
import cv2.face as face
import os
import re
#import pyaudio

import gui
import processing

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
        names = processing.load_names()
    except:
        print("Training model from photos")
        images, labels, names = processing.load_images_labels("./trainingData", face_cascade)
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

        if 0 == int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % 10:
            # Histogram equalization - consider using CLAHE if does not work well
            gray = cv2.equalizeHist(gray)

            # Add flag to only look for one face at a time ? 
            faces = processing.detect_faces(face_cascade, gray)
            gui.draw_faces(faces, frame)

            # Recognize !
            nbrs = processing.recognize_faces(faces, recognizer, gray)
            for nbr in nbrs: 
                gui.drawString("Recognized " + names[nbr], frame, (0, -5), (50, 50, 200), 0.6, cv2.FONT_HERSHEY_COMPLEX, 1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            recognizer.save("trainedModel.yml")
            processing.save_names(names)
            break

        cv2.imshow("PiGreeter", frame)

    cap.release()
    cv2.destroyAllWindows()