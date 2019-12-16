# Goalz

A simple full-stack web app that allows a user to sign in to view, create, and edit personal goals

## Tech Stack

Back-end: Python, Flask, PostgreSQL, SQLAlchemy
Front-end: Javascript, jQuery, Bootstrap

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.


### Installing

A step by step series of examples that tell you how to get a development env running

Create a virtual environment in same directory

```
$ virtualenv env
```

Activate virtual environment

```
$ source env/bin/activate
```

Install requirements

```
$ pip3 install -r requirements.txt
```

Create database

```
$ psql goals
```

Run model.py interactively

```
$ python3 -i model.py
```

Create the database

```
$ db.create_all()
```

Use the program by running server.py and navingating to localhost:5000 on your browsser

```
$ python3 server.py
```

## Tests

I did not have enough time to write tests for this program. If I did, I would have ensured test coverage of Flask routes. 