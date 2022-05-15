from os import listdir
from os.path import join
import face_recognition
import cv2
from pathlib import Path
import numpy as np

def load_images(images_dir):
    print("Loading the image dataset...")
    print("Please wait...")
    images = [join(images_dir, f) for f in listdir(images_dir) if f != ".DS_Store"]
    labels = [Path(f).stem for f in listdir(images_dir) if f != ".DS_Store"]
    encodings = []
    for image in images:
        encoding = face_recognition.face_encodings(face_recognition.load_image_file(image))[0]
        encodings.append(encoding)
    return encodings, labels


def feed(encodings, labels):
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:,:,::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = labels[best_match_index]
            names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, names):
            top *= 4
            right *= 4
            left *= 4
            bottom *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)

            cv2.rectangle(frame, (left, bottom-35), (right, bottom), (0,0,255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left+6, bottom-6), font, 1.0, (255, 255, 255), 1)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')