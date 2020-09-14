# Overview

All in one finance data crunching backend

[![Build Status](https://gkamacharov.visualstudio.com/gkama-cicd/_apis/build/status/kamacharovs.aiof-metadata?branchName=master)](https://gkamacharov.visualstudio.com/gkama-cicd/_build/latest?definitionId=19&branchName=master)

## Documentation

Overall documentation

### Package management

- Install package: `python -m pip install <package-name>`
- Uninstall package: `python -m pip uninstall <package-name>`

### Libraries

- [pandas](https://pandas.pydata.org/docs/reference/index.html)
- [statistics](https://docs.python.org/3/library/statistics.html)
- [list of py finance libraries](https://github.com/wilsonfreitas/awesome-quant#python)
- [numpy-financial](https://numpy.org/numpy-financial/latest/)

## API

### How to run it

The application is setup as a Flask API. In order to start the application, you must `cd` into the correct directory `../api`. Once there, simply run the `flask run` command. Sometimes, you would have to setup the `FLASK_APP` environment variable. In order to do that in powershell, run `$env:FLASK_APP="api"`. The complete steps are:

```powershell
$env:FLASK_APP="api"
cd .\api\
flask run
```

## Tests

Unit tests and how to run them

### How to run unit tests

`python .\setup.py test`
