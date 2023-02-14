## Getting Started

an **.env** file is needed to pass along authorization config values. please email ebettenga@gmail.com to ask about contributing to this project

### Easy Mode

    1. docker compose up 
    2. docker compose exec -it crossed_server /bin/bash
    3. flask db upgrade

    this will get the app in a working order

### Development Mode

    1. create a venv on your machine
    2. pip3 install -r requirements.txt
    3. docker compose up (this will still create a server, but you don't need to use it anymore)
    4. flask db upgrade
    5. for easy development, I shut off the docker server and run flask app.py on my command line, since hot reload is not setup on this codebase.


## Docs

API [flask](https://flask.palletsprojects.com/en/2.2.x/)

Validation and Marshalling / DeMarshalling [marshmallow](https://marshmallow.readthedocs.io/en/stable/examples.html#quotes-api-flask-sqlalchemy)

ORM: [sql-sqlalchemy](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship.params.query_class)

Migrations [alembic migrations](https://kimlehtinen.com/flask-database-migrations-using-flask-migrate/)

WebSocket support [socketio](https://flask-socketio.readthedocs.io/en/latest/getting_started.html#rooms)


    basic migration sequences looks something like

    flask db migrate
    ** check on file and make any changes needed **
    flask db upgrade

    if rollbacks are needed:
    flask db downgrade -1, which rolls back 1 migration

**note:** Creating autogenerated migrations require the model to be imported somewhere in the app, which i'm currently doing [here](app.py) on line 2

## Folder Structure

Folder structure is a domain design, following this pattern

    resource/
        model
        view
        service


Model folder containing the Mapping schemas and the sql model itself

View is to organize resource routes and create response objects

Service layer is to perform actions on data and offload side effects


