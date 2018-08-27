# flask-boilerplate

Because the quickest thing to stop side projects is writing boilerplate code

## Pre-requsites

* python3
* virtualenv (if using python3.7+)
* sqlite3

## Setup

1. Setup virtual environment: `python3 -m venv env`
1. Load virtual environment: `. env/bin/activate`
1. Update pip: `pip3 install -U pip`
1. Install packages: `pip3 install -r requirements.txt`
1. Make script executable `chmod +x main.py`
1. Initialize database: `./main.py db init`
1. Perform database migrations: `./main.py db migrate`
1. Apply migrations to database: `./main.py db upgrade`
1. Start the server: `./main.py`

## License

This project is licensed under the [Revised BSD License](LICENSE).