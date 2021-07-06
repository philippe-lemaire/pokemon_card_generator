from pokemon_card_generator.data.pokemon_list import pokemon_list
from os import path, listdir
from random import choice


def get_illustration(pokémon_name, cards_df, *args, **kwargs):
    """Dummy baseline, selects a random image from raw_data."""
    # get the pokemon national pokédex number
    mask = cards_df.name == pokémon_name
    pokémon_df = cards_df[mask]

    try:
        pokémon_num = pokémon_df.nationalPokedexNumbers.to_list()[0][0]
    except:
        pokémon_num = pokémon_df.nationalPokedexNumbers.to_list()[-1][0]
    pokémon_num = str(pokémon_num)

    # set the path to the images

    three_dirs_up = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

    cropped_imgs_path = path.join(three_dirs_up, "raw_data/img/per_pokemon")
    this_pok_img_path = path.join(cropped_imgs_path, pokémon_num)

    # select a random image
    this_pok_imgs = listdir(this_pok_img_path)
    selected_img = choice(this_pok_imgs)
    # return the selection with its relative path
    final_path = path.join("raw_data/img/per_pokemon", pokémon_num, selected_img)
    return final_path
