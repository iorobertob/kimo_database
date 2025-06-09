

# TODO before release
- delete old scripts
- delete secret, add to an ignored folder
- see about the static serving of files
- replace upload options for thumbs, etc., with links to those resources. Where to host them then?
- migrate to postgres?



# Cleaup model table
```
bash# 1. Clean up existing data
python manage.py shell
>>> from scripts.cleanup_and_reset_films import cleanup_and_reset_films
>>> cleanup_and_reset_films()
```

# Import film data
Navigate to the /scripts/ app and run
```
python import_films.py
```

1. Install Required System Packages
bash# Update package list
sudo apt update
```
# Install MySQL development packages and pkg-config
sudo apt install pkg-config python3-dev default-libmysqlclient-dev build-essential
If you're using MariaDB instead of MySQL:
bashsudo apt install pkg-config python3-dev libmariadb-dev build-essential
2. Install Python Dependencies
bash# Now install the Python packages
pip install python-decouple gunicorn

# Try installing mysqlclient separately first
pip install mysqlclient

# Then install the rest of your requirements
pip install -r req.txt
```