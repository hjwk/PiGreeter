""" Main file of the project"""
import wave

import cv2
import pyaudio

def detect_faces(grayscale, cascade):
    "Detects faces using a haarcascade in a grayscale image"
    return cascade.detectMultiScale(
        grayscale,
        scaleFactor=1.2,
        minNeighbors=5
    )

def draw_faces(faces, img):
    "Draws rectanges around faces "
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

CHUNK = 1024

if __name__ == "__main__":
    """ main
    The flow of this program will be the following:
        1. Grab a frame from the webcam
        2. Detect faces in the frame (haarcascade)
        3. Preprocess faces (histogram equalization)
        4. Recognize faces (eigenvalues ?)
        5. Output appropriate greeting (pyaudio)
    """

    cap = cv2.VideoCapture("faceDetection.mp4")
    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

    wf = wave.open("audio/speech.wav", 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

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
