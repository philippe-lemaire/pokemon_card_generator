from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime
from pokemon_card_generator.predict import create_card


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/create_card")
def pred(pokémon_name, rarity):
    rarity = int(rarity)
    created_card = create_card(pokémon_name, rarity)
    return created_card


if __name__ == "__main__":

    pokémon_name = "Blastoise"
    rarity = "3"

    created_card = pred(pokémon_name, rarity)
    print(pred)
