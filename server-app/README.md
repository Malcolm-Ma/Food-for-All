# Server-app
Drived by django(python) and mysql

# Pre-installed Software Requirements
MYSQL

Anaconda

apidoc

# Environment Setup

## Install Conda Environment
### In Command Line with Anaconda
    cd server-app
    conda env create -f environment_{systemtype}.yml

## Set MYSQL
### In MYSQL
    create user 'apex'@'%' identified by 'apex08';
    grant all privileges on \*.\* to 'apex'@'%';
    flush privileges;

### Then set your mysql ini with:
    [client]
    default-character-set=utf8mb4
    [mysql]
    default-character-set=utf8
    [mysqld]
    port = 3306
    character-set-server=utf8
    default-storage-engine=INNODB

# Startup Environment
## In Command Line with Anaconda
    cd {your mysql bin path}
    net start mysql
    conda activate tsp

# Server Start
## Under the environment of the tsp
    cd {project path}/server-app
    python manage.py runserver 8000

# API Document
Visit http://127.0.0.1:8000/static/apidoc/index.html after startup the server.

# Learn More

To learn django, check out the [Django Documentation](https://docs.djangoproject.com/en/4.0/).