from flask import Flask, render_template
import os

image_name = "SM135_hires"
img_path = "../../raw_data/images/"
set_path = "test"
set_full_path = img_path + set_path
image_full_name = image_name + ".png"
full_path = os.path.join(img_path, set_path, image_full_name)


PEOPLE_FOLDER = os.path.join("static", "image")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = PEOPLE_FOLDER


@app.route("/")
@app.route("/index")
def show_index():
    full_filename = os.path.join(app.config["UPLOAD_FOLDER"], "SM135_hires.png")
    return render_template("index.html", background_image=full_filename)
