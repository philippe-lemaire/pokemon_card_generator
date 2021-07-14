FROM python:3.8.6-buster

COPY api /api
COPY pokemon_card_generator /pokemon_card_generator
COPY raw_data /raw_data
COPY requirements.txt /requirements.txt
COPY pokemontcg_api_key /pokemontcg_api_key
COPY openai_api_key /openai_api_key
COPY flask_app /flask_app


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
CMD cd flask_app/
CMD gunicorn wsgi:app --host 0.0.0.0 --port $PORT