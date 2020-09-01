# Overview

All in one finance data crunching backend

## Documentation

Overall documentation

### Package management

- Install package: `python -m pip install <package-name>`
- Uninstall package: `python -m pip uninstall <package-name>`

## API

### How to run it

The application is setup as a Flask API. In order to start the application, you must `cd` into the correct directory `../api`. Once there, simply run the `flask run` command. Sometimes, you would have to setup the `FLASK_APP` environment variable. In order to do that in powershell, run `$env:FLASK_APP="api"`

## Tests

Unit tests and how to run them

### How to run unit tests

`python .\setup.py test`
