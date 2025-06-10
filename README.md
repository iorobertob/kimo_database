# KIMO Database
## v 1.0.1

## TODO 
- Add a superuser 
Replace upload options for thumbs, etc., with links to those resources. Where to host them then?
- Migrate to postgres?

## Deploy
This asumes deployment in Linux. Tested in Ubuntu using mariaDB and Nginx

### Create Database and user
```
mysql -u root

mysql> create database DATABASE_NAME;

mysql> create user 'USER_NAME'@'localhost' identified by 'PASSWORD';

mysql> grant all privileges on DATABASE_NAME.* TO 'USER_NAME'@'localhost';

mysql> flush privileges;

mysql> exit;
```

### Create a Python virtual environment and activate it
```
python3 -m venv /path/to/virtual/environment
source /path/to/virtual/environment/bin/activate
```

### Clone and prepare Django application
Clone this repository to the server

```
# Navigate to the Django project directory
cd /path/to/cloned/repository
```
### Install Required System Packages

Install MySQL development packages and pkg-config
```
# Update package list
sudo apt update

sudo apt install pkg-config python3-dev default-libmysqlclient-dev build-essential
```
OR If using MariaDB instead of MySQL:
```
bashsudo apt install pkg-config python3-dev libmariadb-dev build-essential

```

Install Python Dependencies
```
# Now install the Python packages
pip install python-decouple gunicorn

# Try installing mysqlclient separately first
pip install mysqlclient

# Then install the rest of your requirements
pip install -r requirements.txt
```

### Collect Static Files
```
# Create static directory
sudo mkdir -p /var/www/misc.lmta.lt/web7/web/kimo/static/

# Collect static files
python manage.py collectstatic --noinput
```

### Create Environment File
```
# Create .env file in your Django project root
nano /path/to/kimo_1/.env
```
Add this to the file:
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here
DB_HOST=localhost
DB_PORT=3306
DB_NAME=some_db_name
DB_USER=some_user_name
DB_PASSWORD=some_password
STATIC_ROOT=/absolute/path/to/kimo/static/
```

### Update Django Settings
Open ```settings.py``` Make sure that the ALLOWED HOSTS point to the domain where this is deployed:
```
ALLOWED_HOSTS = ['misc.lmta.lt', 'localhost']
```

### Database setup/migration
```
# Run migrations
python manage.py migrate
```

### Install and configure Gunicorn
```
# Install Gunicorn
pip install gunicorn

# Test Gunicorn (replace 'kimo_1' with your project name)
gunicorn kimo_1.wsgi:application --bind 0.0.0.0:8001
```

### Create Gunicorn service
```
# Create systemd service file
sudo nano /etc/systemd/system/kimo.service
```

Add this to that file:
```
[Unit]
Description=Gunicorn instance to serve kimo_1
After=network.target

[Service]
User=YOUR-USER
Group=www-data
WorkingDirectory=/path/to/kimo_1
Environment="PATH=/path/to/virtual/environment/bin"
ExecStart=/path/to/virtual/environment/bin/gunicorn --workers 3 --bind unix:kimo.sock -m 007 kimo_1.wsgi:application
Restart=on-always

[Install]
WantedBy=multi-user.target
```

### Start Gunicorn Service
```
# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl start kimo
sudo systemctl enable kimo
sudo systemctl status kimo
```

### Setup/update Nginx Configuration
For this deployment, the Django app lives in a server with an already running site, as a /route from that domain. So we add the location configuration to the nginx file:

```
# Edit existing site configuration
sudo nano /etc/nginx/sites-available/misc.lmta.lt
```

Add this location block inside the existing server block:
```
        # Django app location
        location  /kimo/ {
            proxy_pass http://unix:/var/www/kimo_database/kimo.sock;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Remove /kimo prefix when passing to Django
            rewrite ^/kimo/(.*)$ /$1 break;

            proxy_redirect off;
        }

        # Static files for Django
        location /kimo/static/ {
            alias /var/www/misc.lmta.lt/kimo/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
```

### Test and reload Nginx
```
# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```


### (optional) Verify files ownerships and permissions
```
# Your Django project files should be owned by YOURUSER
sudo chown -R YOURUSER:www-data /var/www/kimo_database/

# Make sure YOURUSER can read/write, www-data can read
sudo chmod -R 755 /var/www/kimo_database/

# Static files directory should be accessible by nginx
sudo chown -R YOURUSER:www-data /var/www/misc.lmta.lt/kimo/
sudo chmod -R 755 /var/www/misc.lmta.lt/web7/web/kimo/

# .env file should be readable by the service user
sudo chown YOURUSER:www-data /var/www/kimo_database/.env
sudo chmod 640 /var/www/kimo_database/.env
```


### (optional) Cleaup model table if there is previous data in it.
```
# 1. Clean up existing data
python manage.py shell
>>> from scripts.cleanup_and_reset_films import cleanup_and_reset_films
>>> cleanup_and_reset_films()
```

### (optional) Import film data from given csv file
Navigate to the /scripts/ app and run
```
python import_films.py
```

## Changelog
### v1.0 - 20250610 - First deployment. Implemented only listing all films with no filtering and a limited range of API endpoints.

### v1.0.1 - 20250610 - Added global search.
