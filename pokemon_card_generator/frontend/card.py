# %matplotlib inline
from flask import Flask, render_template
from pathlib import Path
import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

image_name = "dragon"
base_path = os.getcwd()
set_path = "static/cleaned_cards"
image_full_path = os.path.join(set_path, image_name + ".png")

# base_path2 = Path(os.getcwd()).parents[1]
# set_path2 = "/raw_data/images/test/"
# image_name2 = "SM135_hires"
# image_full_path2 = os.path.join(set_path2, image_name2 + ".png")

app = Flask(__name__)


@app.route("/")
@app.route("/index")

# def print_image_and_texts():
#     text1 = r"text d'ambiance"
#     fig = plt.figure(frameon=True, figsize=(80, 10), dpi=100.0)
#     plt.axis("off")

#     ax1 = plt.imshow(mpimg.imread(image_full_path), alpha=0.7)
#     plt.text(80, 477, text1, fontsize=15, color="black")
#     return plt.show()


def show_index():
    name = r"Dragon"
    return render_template("index.html", background_image=image_full_path, name=name)
