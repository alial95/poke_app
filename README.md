Hello and welcome to my pokedex app! I hope you enjoy using it.
Instructions for usage:
The data used in this program is stored a local MySql database, so please have MySql running locally 
before getting started.
You'll also need to set up a virtual environment to run the packages required for the app to run. 
To do so, run 'python -m venv {NAMEOFENV}', then for mac users run 'source {NAMEOFENV}/bin/activate' and for windows users
run '{NAMEOFENV}/Scripts/activate'. Then once you have your virtual environment up and running, run
'pip install requirements.txt' to install the required packages inside your local environment.
The password variable in the 'sql.py' script will have to be set to the password for your local mysql server. Mine is stored
in an environment variable then loaded using the os and dotenv libraries. Not the most important security step to make
but better safe than sorry!
So, if you have MySql configured on your machine and you are working with a bash shell, the final step to make is
to run 'chmod +x script.sh' and then run './script.sh'. This will create a pokedex database with two tables,
a pokemon table and an items table. These tables will then be populated with data from the PokeApi. If you aren't
in a bash shell, simply run the two python scripts 'load_pokemon.py' and 'load_items.py' back to back to populate
your local database instead. Okay! Now you are ready to go. Finally.... 