""" Main file of the project"""
import cv2
import numpy as np
import pyaudio
import wave

CHUNK = 1024

if __name__ == "__main__":
    """ main    
    """

    cap = cv2.VideoCapture("faceDetection.mp4")
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #profileCascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

    wf = wave.open("speech.wav", 'rb')
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

    while(True):
        ret, frame = cap.read()
        if (ret is False):
            print("End of file")
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5
        )

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        # Profile detection - does not work with sample video
        # profiles = profileCascade.detectMultiScale(
        #     gray,
        #     scaleFactor=1.2,
        #     minNeighbors=5
        # )

        # for (x,y,w,h) in profiles:
        #     cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("Video", frame)
        
    cap.release()
    cv2.destroyAllWindows()
