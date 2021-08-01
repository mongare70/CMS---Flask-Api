# CMS (Flask API)

> A project done in fulfillment of the pre-training challenge of the SkaeHub Developer Program

#1 Problem definition
The main objective of this API is to allow a user to create an account, delete an account,
login, and edit his/her profile when need be.

#2. Installation and setup

1. First clone this repository to your local machine using `https://github.com/mongare70/CMS---Flask-Api`

2. Checkout into the **master** branch using `git checkout master`

3. Create a **virtualenv** on your machine and install the dependencies via `pip install -r requirements.txt` and activate it.

4. cd into the project folder and run `python`

5. While in the python shell run `from app import db` and `db.create_all()` respectively to create database.

6. Run development server to serve the Flask application by running `flask run`

#3. Tests

To run tests ensure that you are within the _virtual environment_ and have the following installed:

1. _pytest_
2. _pytest-cov_

After ensuring the above run :

`pytest` or

`pytest --cov=test_models`

## Credits

1. [Hillary Mongare](https://github.com/mongare70)

2. The [SkaeHub](https://skaehub.com/) community.
