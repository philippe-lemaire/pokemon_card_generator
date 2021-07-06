# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

# ----------------------------------
#    LOCAL COMMANDS
# ----------------------------------

check_code:
	@flake8 scripts/* pokemon_card_generator/*.py

black:
	@black scripts/* pokemon_card_generator/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr pokemon_card_generator-*.dist-info
	@rm -fr pokemon_card_generator.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
#PYPI_USERNAME=<AUTHOR>
#build:
#	@python setup.py sdist bdist_wheel
#
#pypi_test:
#	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)
#
#pypi:
#	@twine upload dist/* -u $(PYPI_USERNAME)

start_api:
	@uvicorn api.fast:app --reload


### GOOGLE Cloud stuff

# project id
PROJECT_ID=pokemon-card-generator-wagon
REGION=europe-west1

enable_registry:
	gcloud services enable containerregistry.googleapis.com --project=${PROJECT_ID}

set_project:
	-@gcloud config set project ${PROJECT_ID}

### Docker stuff
SERVICE = pokecardgenerator

DOCKER_IMAGE_NAME = pokemon_card_docker_image
docker_build_image:
	docker build -t eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME} .

docker_run_locally:
	docker run -e PORT=8000 -p 8000:8000 eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME}

docker_deploy:
	docker push eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME}

docker_run_at_google:
	gcloud run deploy ${SERVICE} --image eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME} --allow-unauthenticated --platform managed --region ${REGION}
