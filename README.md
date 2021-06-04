# Status

Early Development.


# tinytinylog
A tiny tiny app to log things.


# Development 

### Setup

Create a Python3 (v3.9+) environment: `python3 -m venv .venv`

Activate the environment: `source .venv/bin/activate`

Install requirements: `pip install -r requirements.txt`

### Environment

Rename the file `.env.example` to `.env`.
Update the values in `.env` files. Default values are for development!

### Run

Create a Django super user: `./manage.py createsuperuser`

Run the application: `./manage.py runserver`

### Style enforcement

Run `flake8`
Fix any issue that may come up.