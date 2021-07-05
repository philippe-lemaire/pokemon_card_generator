from pokemon_card_generator import utils
from pokemon_card_generator.data.scrap_data import get_lore
import openai
from os import path
from random import choice


def get_prompt(pokémon_name, cards_df):
    """returns a random beginning of prompt from a random flavor text in cards_df set to this pokémon"""
    # filter on cards with this name
    mask = cards_df.name == pokémon_name
    pokémon_df = cards_df[mask]

    # list the flavor texts

    flavor_texts = [text for text in pokémon_df.flavorText if isinstance(text, str)]

    # remove duplicates
    flavor_texts = list(set(flavor_texts))
    # make a random selection
    selected_flavor = choice(flavor_texts)
    # cut down the prompt take the 8 first words
    prompt_as_list = selected_flavor.split(" ")[:6]
    # slice it up and join it back
    prompt = " ".join(prompt_as_list)
    return prompt


def generate_flavor(pokémon_name, cards_df, *args, **kwargs):
    """Baseline: uses openAI to generate text"""

    # locate the path to the api-file and load it
    three_dirs_up = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    api_file = path.join(three_dirs_up, "openai_api_key/openai.key")

    openai.api_key = utils.get_file_contents(api_file)

    # read from the scrapped wiki biology section and pick the first 50 characters
    # lore = get_lore()
    prompt = get_prompt(pokémon_name, cards_df)

    # call the API
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=25)
    flavor_text = f"{prompt}{response['choices'][0]['text']}"

    # split the response after the first dot and return it with the dot included.
    sep = "."
    stripped = flavor_text.split(sep, 1)[0].strip()
    # remove some \n that would be present
    stripped = stripped.replace("\n", " ")
    # remove eventual double spaces
    stripped = stripped.replace("  ", " ")
    # all done
    return stripped + sep


if __name__ == "__main__":
    prompt = "Bulbasaur is feeling"

    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=25)
    print(f"{prompt}{response['choices'][0]['text']}")
