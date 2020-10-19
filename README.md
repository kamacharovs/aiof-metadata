# Overview

All in one finance data crunching backend

[![Build Status](https://gkamacharov.visualstudio.com/gkama-cicd/_apis/build/status/kamacharovs.aiof-metadata?branchName=master)](https://gkamacharov.visualstudio.com/gkama-cicd/_build/latest?definitionId=19&branchName=master)

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
/api/fi/savings/rate
```

### Asset

Asset functionality and analysis

API endpoints available are

```text
/api/asset/breakdown
```

## How to run it

In order to run the API locally, you would first need to run the `python .\setup.py develop` script, if it hasn't been setup locally before. Afterwards, start the API via `uvicorn`

```powershell
python .\setup.py develop
uvicorn api.main:app
```

### Docker

Build it

```powershell
docker build -t aiof-metadata .
```

Run it

```poershell
docker run -it --rm -p 8000:80 aiof-metadata
```

Make API calls to

```text
http://localhost:8080/
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

## Documentation

Overall documentation

### Package management

- Install package: `python -m pip install <package-name>`
- Uninstall package: `python -m pip uninstall <package-name>`

### Libraries

- [fastapi](https://github.com/tiangolo/fastapi)
- [uvicorn](https://github.com/encode/uvicorn)
- [pandas](https://pandas.pydata.org/docs/reference/index.html)
- [pandas-datareader](https://pydata.github.io/pandas-datareader/stable/index.html)
- [statistics](https://docs.python.org/3/library/statistics.html)
- [numpy-financial](https://numpy.org/numpy-financial/latest/)
- [pytest](https://docs.pytest.org/en/stable/)
- [list of py finance libraries](https://github.com/wilsonfreitas/awesome-quant#python)

#### FastAPI

Helpful `FastAPI` documentation

- [Settings and Environment Variables](https://fastapi.tiangolo.com/advanced/settings/)
- [Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Dependencies - First Steps](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Concurrency and async / await](https://fastapi.tiangolo.com/async/)
- [Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/)
- [tiangolo/uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)

#### Pydantic

Helpful `pydantic` documentation

- [Typing Iterables](https://pydantic-docs.helpmanual.io/usage/types/#typing-iterables)

#### Pandas

Helpful `pandas` documentation

- [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html)

#### Python

Helpful `python` documentation

- [Dependency injection and inversion of control in Python](http://python-dependency-injector.ets-labs.org/introduction/di_in_python.html)
- [Lambda, Map, and Filter in Python](https://medium.com/better-programming/lambda-map-and-filter-in-python-4935f248593)
- [numpydoc docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html#numpydoc-docstring-guide)
