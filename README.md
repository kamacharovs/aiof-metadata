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
- [fastapi](https://github.com/tiangolo/fastapi)
- [pytest](https://docs.pytest.org/en/stable/)

## API

### Financial independence (FI)

Financial Independence is based on the FIRE movement. Financial Independence, Retire Early (FIRE) is a movement dedicated to a program of extreme savings and investment that allows proponents to retire far earlier than traditional budgets and retirement plans would allow. By dedicating up to 70% of income to savings, followers of the FIRE movement may eventually be able to quit their jobs and live solely off small withdrawals from their portfolios decades before the conventional retirement age of 65. More information can be found [here](https://www.investopedia.com/terms/f/financial-independence-retire-early-fire.asp)

API endpoinds available are

```text
/metadata/fi/time/to/fi
/metadata/fi/added/time
/metadata/fi/rule/of/72
/metadata/fi/ten/million/dream/<int:monthlyInvestment>
/metadata/fi/compound/interest
/metadata/fi/investment/fees/effect
```

### How to run it

```powershell
python .\setup.py develop
cd .\api
uvicorn api:app
```

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
