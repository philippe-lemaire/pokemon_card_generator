from pokemon_card_generator import utils
import openai
from os import path

three_dirs_up = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

api_file = path.join(three_dirs_up, "openai_api_key/openai.key")

# Load your API key from an environment variable or secret management service
openai.api_key = utils.get_file_contents(api_file)


if __name__ == "__main__":
    prompt = "Bulbasaur is feeling"

    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=25)
    print(f"{prompt}{response['choices'][0]['text']}")
