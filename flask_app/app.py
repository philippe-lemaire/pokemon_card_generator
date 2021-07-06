from pokemon_card_generator.data.pokemon_list import pokemon_list
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config["SECRET_KEY"] = "C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb"

# Flask-Bootstrap requires this line
Bootstrap(app)


class Form(FlaskForm):
    pokémon_name = SelectField(
        "Select a Pokémon", choices=pokemon_list, validators=[DataRequired()]
    )
    rarity = SelectField(
        "Select a rarity", choices=range(1, 6), validators=[DataRequired()]
    )
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():

    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = Form()
    message = ""
    if form.validate_on_submit():
        pokémon_name = form.pokémon_name.data
        rarity = form.rarity.data
        base_api_url = "https://pokecardgenerator-tybpdn52ha-ew.a.run.app/create_card"
        params = {"pokémon_name": pokémon_name, "rarity": rarity}
        card_data = requests.get(url=base_api_url, params=params).json()
        return render_template(
            "card.html", form=form, message=message, card_data=card_data
        )
    else:
        message = "Please select a Pokémon and a rarity level."
    return render_template("index.html", form=form, message=message)
