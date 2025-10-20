
from flask import Flask, render_template, request
import os
import cv2
import numpy as np
from utils import detect_plate_and_text

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", result={"text": "No file uploaded."})

        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", result={"text": "No selected file."})

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "uploaded.jpg")
        file.save(file_path)

        image = cv2.imread(file_path)
        plate_img, text = detect_plate_and_text(image)

        if plate_img is not None:
            result_path = os.path.join(app.config['UPLOAD_FOLDER'], "plate_result.jpg")
            cv2.imwrite(result_path, plate_img)
            result = {"text": text, "img_path": result_path}
        else:
            result = {"text": "No plate detected", "img_path": None}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
