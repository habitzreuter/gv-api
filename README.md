# gv API

## Install
gv requires Python 3.6 and pipenv

### Run development environment
```
pipenv install --dev
pipenv run gunicorn --reload "gv:get_app()"
```

### Run tests
To run unit tests, execute
```
pipenv install --dev
pipenv run coverage run -m pytest tests/ tests_integration/
pipenv run coverage report
```

### Run gunicorn
```
pipenv run gunicorn --reload "gv:get_app()"
```