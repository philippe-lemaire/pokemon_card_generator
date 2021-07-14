FROM python:3.8.6-buster

COPY pokemon_card_generator /pokemon_card_generator
COPY raw_data /raw_data
COPY requirements.txt /requirements.txt
COPY pokemontcg_api_key /pokemontcg_api_key
COPY openai_api_key /openai_api_key
COPY flask_app /flask_app
COPY setup.py /setup.py
COPY scripts /scripts
COPY tests /tests

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .

CMD cd flask_app/ && gunicorn wsgi:app -b 0.0.0.0:$PORT