# Getting Started
The Item Catalog project consists list of items within a variety of categories, as well as provide a user registration and authentication system.

## Setting up enviroment
### Downloads
1. Install virtualbox. [Download Virtualbox](https://www.virtualbox.org/)
2. Install Vagrant. [Download Vagrant](http://vagrantup.com)
3. Clone this repository.

### Starting enviroment
Go to cloned project folder and run the following command ``` vagrant up ``` and wait until it's done. Then run ```vagrant ssh``` You are now logged in our desired environment.
## Starting Project
After running ```vagrant ssh``` you are now in development enviroment. Now go to project folder using the command 

```cd /vagrent/application```

### Install

```pip install Flask-JSON```

### Add enviroment variable

```
export FLASK_APP=catalog
export FLASK_ENV=development
```

### Run server

```
flask run --host=0.0.0.0
```

#### Resources used along with udacity classes:
1. http://flask.pocoo.org/docs/1.0/tutorial
2. http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/