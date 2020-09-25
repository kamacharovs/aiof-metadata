# Overview

All in one finance data crunching backend

[![Build Status](https://gkamacharov.visualstudio.com/gkama-cicd/_apis/build/status/kamacharovs.aiof-metadata?branchName=master)](https://gkamacharov.visualstudio.com/gkama-cicd/_build/latest?definitionId=19&branchName=master)

## Documentation

Overall documentation

### Package management

- Install package: `python -m pip install <package-name>`
- Uninstall package: `python -m pip uninstall <package-name>`

### Libraries

- [fastapi](https://github.com/tiangolo/fastapi)
- [uvicorn](https://github.com/encode/uvicorn)
- [pandas](https://pandas.pydata.org/docs/reference/index.html)
- [statistics](https://docs.python.org/3/library/statistics.html)
- [numpy-financial](https://numpy.org/numpy-financial/latest/)
- [pytest](https://docs.pytest.org/en/stable/)
- [list of py finance libraries](https://github.com/wilsonfreitas/awesome-quant#python)

#### FastAPI

Helpful `FastAPI` documentation

- [Settings and Environment Variables](https://fastapi.tiangolo.com/advanced/settings/)
- [Dependencies - First Steps](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Concurrency and async / await](https://fastapi.tiangolo.com/async/)

#### Python

Helpful `python` documentation

- [Dependency injection and inversion of control in Python](http://python-dependency-injector.ets-labs.org/introduction/di_in_python.html)

## API

### Financial independence (FI)

Financial Independence is based on the FIRE movement. Financial Independence, Retire Early (FIRE) is a movement dedicated to a program of extreme savings and investment that allows proponents to retire far earlier than traditional budgets and retirement plans would allow. By dedicating up to 70% of income to savings, followers of the FIRE movement may eventually be able to quit their jobs and live solely off small withdrawals from their portfolios decades before the conventional retirement age of 65. More information can be found [here](https://www.investopedia.com/terms/f/financial-independence-retire-early-fire.asp)

API endpoinds available are

```text
/api/fi/time
/api/fi/added/time
/api/fi/compound/interest
/api/fi/rule/of/72
/api/fi/ten/million/dream/{monthlyInvestment}
/api/fi/investment/fees/effect
```

## How to run it

In order to run the API locally, you would first need to run the `.\setup.py` script, if it hasn't been setup locally before. Afterwards, you need to change the directory to the `.\api` one and run it via `uvicorn`

```powershell
python .\setup.py develop
cd .\api
uvicorn api:app
```

### Docker

```powershell
docker build -t aiof-metadata .
docker run -p 8080:80 aiof-metadata
```

Or run the container detached

```poershell
docker run -d -p 8080:80 aiof-metadata
```

Optional command to clean up `<none>` images

```powershell
docker rmi $(docker images -f “dangling=true” -q)
```

## Tests

Unit tests are used to test units of code. Below you can see how to run them

### How to run unit tests

```powershell
cd .\tests\
pytest
```
