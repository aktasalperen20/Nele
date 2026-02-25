from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import hashlib

app = Flask(__name__)


UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def simple_ai_analysis(filename):
   
    hash_object = hashlib.md5(filename.encode())
    hash_digest = hash_object.hexdigest()
    hash_int = int(hash_digest, 16)

    types = ["Schürfwunde", "Schnittwunde", "Verbrennung"]
    depths = ["oberflächlich", "mitteltief", "tief"]

    type_index = hash_int % len(types)
    depth_index = (hash_int // len(types)) % len(depths)

    return f"Wunden-Typ: {types[type_index]}, Tiefe: {depths[depth_index]}"


@app.route("/")       
def home():
    return render_template("Untitled-1.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        file = request.files.get("image")
        if not file or file.filename == "":
            return render_template("Untitled-2.html",
                                   image_url=None,
                                   result_text="Keine Datei ausgewählt!",
                                   warning=True)

        if not allowed_file(file.filename):
            return render_template("Untitled-2.html",
                                   image_url=None,
                                   result_text="Nur Bilddateien erlaubt!",
                                   warning=True)

        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        image_url = f"/static/uploads/{filename}"
        result_text = simple_ai_analysis(filename)  

        return render_template("Untitled-2.html",
                               image_url=image_url,
                               result_text=result_text,
                               warning=True)

    
    return render_template("Untitled-2.html",
                           image_url=None,
                           result_text="",
                           warning=False)

if __name__ == "__main__":
    app.run(debug=True)
