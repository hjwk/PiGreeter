""" Main file of the project"""
import wave

import numpy as np
import cv2
import cv2.face as face
import pyaudio

def detect_faces(grayscale, cascade):
    "Detects faces using a haarcascade in a grayscale image"
    return cascade.detectMultiScale(
        grayscale,
        scaleFactor=1.2,
        minNeighbors=5
    )

def draw_faces(faces, img):
    "Draws rectanges around faces"
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

def load_images():
    "Loads images for the recognizer module"
    pass

if __name__ == "__main__":
    """ main
    The flow of this program will be the following:
        1. Grab a frame from the webcam
        2. Detect faces in the frame (haarcascade)
        3. Preprocess faces (histogram equalization)
        4. Recognize faces (LBPH)
        5. Output appropriate greeting (pyaudio ? espeek ?)
    """
    print(help(cv2.face))
    cap = cv2.VideoCapture("faceDetection.mp4")
    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    recognizer = face.createLBPHFaceRecognizer()

    wf = wave.open("audio/speech.wav", 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(1024)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()

    p.terminate()

    while True:
        ret, frame = cap.read()
        if ret is False:
            print("End of file")
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detect_faces(gray, face_cascade)
        draw_faces(faces, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("Video", frame)

    cap.release()
    cv2.destroyAllWindows()