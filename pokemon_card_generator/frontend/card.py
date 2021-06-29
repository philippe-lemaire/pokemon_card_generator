from flask import Flask, render_template
from pathlib import Path
import os

base_path = os.getcwd()
set_path = "static/image"
image_name = "SM135_hires"
image_full_name = image_name + ".png"

full_path = os.path.join(set_path, image_full_name)


base_path2 = Path(os.getcwd()).parents[1]
set_path2 = "/raw_data/images/test/"
image_name2 = "SM135_hires"
image_full_name2 = image_name2 + ".png"

full_path2 = os.path.join(set_path2, image_full_name2)

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def show_index():
    return render_template("index.html", background_image=full_path)
