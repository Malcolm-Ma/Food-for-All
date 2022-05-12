# Server-app
Written by team8 (APEX)

Driven by django(python) and mysql

# Pre-installed Software Requirements
MYSQL

Anaconda

node.js

# Environment Setup

## Install Conda Environment
### In Command Line with Anaconda
Note: replace "{systemtype}" with the name of your operating system, e.g. windows
```shell
cd server-app
conda env create -f environment_{systemtype}.yml
```

## Set MYSQL
### In MYSQL

```mysql
create database foodforall;
create user 'apex'@'%' identified by 'apex08';
grant all privileges on *.* to 'apex'@'%';
flush privileges;
```

### Then set your mysql ini with:

```
[client]
default-character-set=utf8mb4
[mysql]
default-character-set=utf8
[mysqld]
port = 3306
character-set-server=utf8
default-storage-engine=INNODB
```

## Initialise the database

```shell
cd {project path}/server-app
conda activate tsp
python manage.py makemigrations
python manage.py migrate
```

# Startup Environment
## In Command Line with Anaconda

```shell
cd {your mysql bin path}
net start mysql
```

# Server Start

```shell
cd {project path}/server-app
conda activate tsp
python manage.py runserver --noreload 0.0.0.0:8000
```

# Demo

After the initial start of the back-end service, the database is empty.
The back-end service therefore provides a demo data generation interface for testing and debugging.
Please make sure that 
```python
DEBUG = False
```
is changed to 
```python
DEBUG = True
``` 
in FoodForAll/settings.py.
Afterwards use your browser to access http://127.0.0.1:8000/init_database/
**The interface will empty the database and regenerate 50 simulated users and 100 simulated projects.**
Please note that the interface will call the api provided by paypal sandbox to request the product id when generating the fake projects, so the interface will run slowly, around 1 minute. **Please be patient. Please do not refresh the page**.
**Note that you should not call this interface repeatedly within 5 minutes**, otherwise paypal sandbox may temporarily disable the api call and cause the interface to report an error; if you accidentally trigger the threshold of paypal's disable call, don't worry, just wait for 5 minutes and call the interface again.
The interface returns json format, where user_list is a list of size 50*5, and the 5 columns in the list are the initialized user's: uid, mail, password, encrypted_password, user_type. **If you are testing through the front end, use the password column as the user password, if you are accessing the back end directly, use the encrypted_password column as the user password**, because when accessing the back end directly, the password transfer encryption process is not applied. user_list is also stored in the **{project path}/debug/ backend/init_database/init_database_user.csv** for easy viewing by testers.

# API Document

Open webpage http://127.0.0.1:8000/static/apidoc/index.html after startup the server.

# Learn More

To learn django, check out the [Django Documentation](https://docs.djangoproject.com/en/4.0/).

# Contact

If you have any questions about the back-end system, please contact tliang9@sheffield.ac.uk