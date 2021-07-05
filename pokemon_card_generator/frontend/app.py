from flask import Flask, render_template, request
import requests
import os
from pokemon_card_generator.data.pokemon_list import pokemon_list

app = Flask("Pokemon Card Generator")
app.debug = True


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html", pokemon_list=pokemon_list, ability_text="ability text test OK"
    )


# @app.route("/result", methods=["POST"])
# def result():
#     result = request.form
#     pokemon_selected = result["pokemon_selected"]
#     rarity = result["rarity"]
#     return render_template(
#         "result.html", pokemon_selected=pokemon_selected, rarity=rarity
#     )


@app.route("/result1", methods=["POST"])
def result1():
    pokemon_selected = request.form["pokemon_selected"]
    rarity = request.form["rarity"]
    return render_template(
        "result1.html", pokemon_selected=pokemon_selected, rarity=rarity


# address of the api prediction
url = "https://api.pokemontcg.io/v2/cards/swsh4-57"
url2 = "https://api.pokemontcg.io/v2/cards/xy6-75"
url_api = "https://pokecardgenerator-tybpdn52ha-ew.a.run.app/create_card?pok%C3%A9mon_name=Pikachu&rarity=2"
api = "https://pokecardgenerator-tybpdn52ha-ew.a.run.app/create_card"

# get prediction
# params = dict(pokémon_name=pokemon_selected, rarity=rarity_selected)
# response = requests.get(url_api, params=params)
response = requests.get(url2)
prediction = response.json()

# input from prediction
pokemon_type = prediction["data"]["types"][0].lower()
pokemon_name = prediction["data"]["name"]
hp = prediction["data"]["hp"]
nationalPokedexNumbers = prediction["data"]["nationalPokedexNumbers"][0]

# category
if prediction["data"].get("category"):
    pokemon_category = prediction["data"]["category"]
else:
    pokemon_category = "Pokémon"

# height
if prediction["data"].get("height"):
    pokemon_height = prediction["data"]["height"]
else:
    pokemon_height = "5'"

# weight
if prediction["data"].get("weight"):
    pokemon_weight = prediction["data"]["weight"]
else:
    pokemon_weight = "12.4 lbs"

# ability
if prediction["data"].get("abilities"):
    ability_name = prediction["data"]["abilities"][0]["name"]
    ability_text = prediction["data"]["abilities"][0]["text"]

# attacks
if len(prediction["data"]["attacks"]) > 0:
    pokemon_attack1_cost = prediction["data"]["attacks"][0]["cost"]
    pokemon_attack1_name = prediction["data"]["attacks"][0]["name"]
    pokemon_attack1_damage = prediction["data"]["attacks"][0]["damage"]
    pokemon_attack1_text = prediction["data"]["attacks"][0]["text"]
if len(prediction["data"]["attacks"]) > 1:
    pokemon_attack2_cost = prediction["data"]["attacks"][1]["cost"]
    pokemon_attack2_name = prediction["data"]["attacks"][1]["name"]
    pokemon_attack2_damage = prediction["data"]["attacks"][1]["damage"]
    pokemon_attack2_text = prediction["data"]["attacks"][1]["text"]

# weakness
if prediction["data"].get("weaknesses"):
    pokemon_weakness_type = prediction["data"]["weaknesses"][0]["type"]
    pokemon_weakness_value = prediction["data"]["weaknesses"][0]["value"]

# resistance
if prediction["data"].get("resistances"):
    pokemon_resistance_type = prediction["data"]["resistances"][0]["type"]
    pokemon_resistance_value = prediction["data"]["resistances"][0]["value"]

# retreat
if prediction["data"].get("retreatCost"):
    pokemon_retreat_cost = prediction["data"]["retreatCost"][0]

# flavor text
if prediction["data"].get("flavorText"):
    pokemon_flavor_text = prediction["data"]["flavorText"]

# define paths
main_path = "pokemon_card_generator/frontend/static/images/"
set_path = main_path + "cleaned_cards"
ability_img_path = main_path + "card_icons/ability.png"
image_full_path = os.path.join(set_path, pokemon_type + ".png")

if __name__ == "__main__":
    app.run()
