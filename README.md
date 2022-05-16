# Face Recognition based Attendance System

The project was developed to faclitate automated attendance where students just pass through a camera and the system automatically marks the attendance by recognizing the face.

### Tools & Libraries used

- Python3
- Pandas
- Flask
- OpenCV
- face_recognition
- cmake (required for face_recognition)
- openpyxl
- numpy

## Instructions to run the application

To begin, first clone the repository onto your local machine and install the dependencies using below command

```
git clone https://github.com/kskd1804/face_recognition.git
cd face_recognition
pip install -r requirements.txt
```

Now that you have all the required dependencies installed, lets try to understand the directory structure. The structure is as follows:

- `database`: Folder which contains the database files such as the `students.xlsx` and `attendance.xlsx`. The `students.xlsx` is the file which holds all the student information and their corresponding image names. `attendance.xlsx` file holds the attendance information of all students.

- `dataset`: This folder holds the images of the students. If the image of student X is in the file `X_img.jpg`, then the same should be entered in the `students.xlsx` file in the `Image` column.

- `templates`: Holds the HTML views
- `server.py`: The Flask server which runs the whole application. You will have to run this file to start the application.
- `recognition.py`: Holds all the code related to recognition and tagging.
- `requirements.txt` - Holds the python requirements for the project.


To begin the application, first insert the persons whose attendance must be tracked in the dataset folder (say the filename is ABC.jpg). Now open the `students.xlsx` file and insert a row with the students information and the filename ABC.jpg under the Image column.

Finally run the below command to start the application
```
python server.py
```
This should start the server on the port 5000. You can access the server by open the url http://localhost:5000 on your browser.

The website shows that activity tag i.e. LOGIN/LOGOUT under the name of the student. Additonally, you can open the attendance.xlsx file to view the attendance log.