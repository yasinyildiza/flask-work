set FLASK_APP=mywallet
set MYWALLET_SETTINGS=..\..\config.py
flask dropdb
flask initdb
flask createanonymoususer
flask populatedb
