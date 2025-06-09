

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