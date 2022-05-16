from crypt import methods
from flask import Flask, Response, render_template, request, redirect, url_for
import recognition

app = Flask(__name__)

images_dir = "./dataset/"
encodings, labels = recognition.load_images()

@app.route("/feed")
def stream():
    global encodings
    global labels
    return Response(recognition.feed(encodings=encodings, labels=labels), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def home():
    return render_template("capture.html")

if __name__ == "__main__":
    app.run()