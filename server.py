from flask import Flask, Response, render_template
import recognition

app = Flask(__name__)

images_dir = "./dataset/"
encodings, labels = recognition.load_images(images_dir)

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