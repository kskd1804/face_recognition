from os import listdir
from os.path import join
import face_recognition
import cv2
from pathlib import Path
import numpy as np
import pandas as pd
from datetime import datetime

def load_images():
    print("Loading the image dataset...")
    print("Please wait...")
    images_dir = "./dataset/"
    df_students = pd.read_excel("./database/students.xlsx", header=0)
    images = df_students['Image'].values.tolist()
    images = [(join(images_dir, f), f) for f in images]
    labels = []
    encodings = []
    for path, image in images:
        try:
            encoding = face_recognition.face_encodings(face_recognition.load_image_file(path))[0]
            encodings.append(encoding)
            name = df_students[df_students["Image"] == image]["Name"].reset_index(drop=True)[0]
            rollno = df_students[df_students["Image"] == image]["RollNo"].reset_index(drop=True)[0]
            labels.append((rollno, name))
        except Exception as e:
            print(f"Missing file: { path }")
            print(e)
    return encodings, labels

def mark_attendance(rollno, name):
    timestamp = datetime.now()
    tag = "LOGIN"
    startrow = 1
    try:
        df_attendance = pd.read_excel("./database/attendance.xlsx", header=0)
        startrow = len(df_attendance) + 1
        print(df_attendance)
        if len(df_attendance) > 0:
            df_marked = df_attendance[df_attendance["Date"].dt.date == datetime.now().date()]["Activity"]
            tag  = "LOGOUT" if len(df_marked) > 0 and df_marked[len(df_marked)-1] == "LOGIN" else "LOGIN"
    except Exception as e:
        print("Error:", e)
    df = pd.DataFrame([[timestamp, rollno, name, tag]], columns=['Date', 'RollNo', 'StudentName', 'Activity'])
    with pd.ExcelWriter("./database/attendance.xlsx", if_sheet_exists='overlay', mode='a', engine="openpyxl") as writer:
        df.to_excel(writer, index=False, header=False, startrow=startrow)
    print("Mark Attendance", name, rollno, tag)
    return tag

def feed(encodings, labels):
    video_capture = cv2.VideoCapture(0)
    memory = [0]*len(labels)
    tags = ["LOGIN"]*len(labels)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:,:,::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        identifiers = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(encodings, face_encoding)
            identifier = ("Unknown", "Unknown") # first element is rollno, second element is name

            face_distances = face_recognition.face_distance(encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                identifier = (*labels[best_match_index], best_match_index)
                identifiers.append(identifier)

        for (top, right, bottom, left), (rollno, name, index) in zip(face_locations, identifiers):
            top *= 4
            top += 20
            right *= 4
            right += 20
            left *= 4
            left += 20
            bottom *= 4
            bottom += 20
            tag = tags[index]
            stamp = datetime.now().timestamp()
            if stamp - memory[index] >= 5:
                tag = mark_attendance(rollno, name)
            memory[index] = stamp
            tags[index] = tag
            cv2.rectangle(frame, (left, top), (right, bottom), (255,0,255), 2)
            cv2.rectangle(frame, (left, bottom-35), (right, bottom), (255,0,255), cv2.FILLED)
            cv2.rectangle(frame, (left, bottom-70), (right, bottom), (255,0,255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left+6, bottom-40), font, 1.0, (255, 255, 255), 1)
            cv2.putText(frame, tag+" success", (left+6, bottom-6), font, 1.0, (255, 255, 255), 1)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    print(load_images())