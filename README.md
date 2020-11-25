
# PeerRecSys

## Peer Recomendation System that pairs a user with a with another to form a study session

The system pairs a user with a deficiency in a certain skill with another user that is competent in that skill

## Setting up the flask server

1. Make sure you have python3 and pip3 installed

2. Clone this project folder

3. Create a venv inside the project folder

4. install dependencies in the requirements.txt file using pip

5. run using python flaskblog.py

## Follow these commands after cloning project folder (WINDOWS ONLY)

1. Install python3 from https://www.python.org/downloads/windows/

2. Add python and pip3 to path https://datatofish.com/add-python-to-windows-path/

3. pip3 comes with python3 installation

4. open cmd and go to project folder and run the following commands

5. python -m venv env

6. env\Scripts\activate.bat

7. pip install -r requirements.txt

8. add the following to windows environmental variables (same way as in step 2)
 - variable name: SECRET_KEY ,  value: 6367bd0b7d25c57d19b2f68a79897059 (or generate your own)
 - variable name: SQLALCHEMY_DATABASE_URI , value: sqlite:///site.db?check_same_thread=False
 
9. create the database https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/ ( import app from peer_rec_sys and do app.app_context().push before create_all() )

8. enter command python run.py

9. to deactivate venv type deactivate on cmd


