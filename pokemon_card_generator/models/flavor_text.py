from pokemon_card_generator import utils
from pokemon_card_generator.data.scrap_data import get_lore
import openai
from os import path


def generate_flavor(pokémon_name, *args, **kwargs):
    """Baseline: uses openAI to generate text"""

    # locate the path to the api-file and load it
    three_dirs_up = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    api_file = path.join(three_dirs_up, "openai_api_key/openai.key")

    openai.api_key = utils.get_file_contents(api_file)

    # read from the scrapped wiki biology section and pick the first 50 characters
    lore = get_lore()
    prompt = lore[pokémon_name][1:50]

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
