from pokemon_card_generator.data.pokemon_list import pokemon_list
from pokemon_card_generator.predict import create_card
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import requests
import random

app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config["SECRET_KEY"] = "C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb"

# Flask-Bootstrap requires this line
Bootstrap(app)

rarityDict = {"Common": 1, "Uncommon": 2, "Rare": 4, "Ultra Rare": 5}


class Form(FlaskForm):
    pokémon_name = SelectField(
        "Select a Pokémon", choices=pokemon_list, validators=[DataRequired()]
    )
    rarity = SelectField(
        "Select a rarity", choices=rarityDict.keys(), validators=[DataRequired()]
    )
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():

    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = Form()
    message = ""
    if form.validate_on_submit():
        random_set_size = random.randint(101, 200)
        random_card_number = random.randint(1, random_set_size)
        if random_card_number < 10:
            card_number = f"00{random_card_number}/{random_set_size}"
        elif random_card_number < 100:
            card_number = f"0{random_card_number}/{random_set_size}"
        else:
            card_number = f"{random_card_number}/{random_set_size}"

        pokémon_name = form.pokémon_name.data
        rarity = form.rarity.data
        rarity = rarityDict[rarity]

        card_data = create_card(pokémon_name=pokémon_name, rarity=rarity)
        return render_template(
            "card.html",
            form=form,
            message=message,
            card_data=card_data,
            card_number=card_number,
            rarity=rarity,
        )
    else:
        message = "Pikachus will power your request..."
    return render_template("index.html", form=form, message=message)
