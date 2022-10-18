# CRUD REST API

## Summary

This repo contains a basic create-read-update-delete (CRUD) API with standard endpoints (POST, GET, PATCH, and DELETE).  The Python code leverages the Tornado web framework and interfaces with a SQLite database.  It passes many tests with static-analysis tools (`black`, `isort`, `pylint`, `mypy`, `bandit`, `pytest`, and `pipenv check`).  Run the app with `pipenv run python -m src.main` from the top-level directory within the repo.  You can then issue commands like `requests.post('http://localhost:888/api/widgets', params={'name': 'widget1', 'parts': '5'})` and get reasonable responses.

## Getting started

You'll need `git`, Python 3.9, and `pipenv`.  After cloning down the repo, navigate into the repo's top-level directory and use `pipenv install` to get all of the packages set up within a virtual environment.  Remember to use `pipenv run` or `pipenv shell` to work within the virtual environment; otherwise, you'll be using whatever Python packages you have installed otherwise.

## Checking the code

Here is a `pipenv shell` session illustrating the results of various static-analysis tools applied to the codebase.

### `black`
```
(crud_rest_api) 16:19 ~/crud_rest_api (main) black .
All done! ✨ 🍰 ✨
11 files left unchanged.
```

### `isort`
```
(crud_rest_api) 16:19 ~/crud_rest_api (main) isort .
Skipped 5 files
```

### `mypy`
```
(crud_rest_api) 16:19 ~/crud_rest_api (main) mypy .
Success: no issues found in 11 source files
```

### `pylint`
```
(crud_rest_api) 16:20 ~/crud_rest_api (main) pylint src/ tests/

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```

### `pytest`
```
(crud_rest_api) 16:20 ~/crud_rest_api (main) pytest
======================================================== test session starts ========================================================
platform linux -- Python 3.9.2, pytest-7.1.3, pluggy-1.0.0
rootdir: /home/patrick/crud_rest_api
collected 8 items

tests/test_db.py ........                                                                                                     [100%]

========================================================= 8 passed in 0.25s =========================================================
```

### `bandit`
```
(crud_rest_api) 16:28 ~/crud_rest_api (main) bandit -r -c pyproject.toml .
[main]  INFO    profile include tests: None
[main]  INFO    profile exclude tests: None
[main]  INFO    cli include tests: None
[main]  INFO    cli exclude tests: None
[main]  INFO    using config: pyproject.toml
[main]  INFO    running on Python 3.9.2
Run started:2022-10-18 20:30:24.300375

Test results:
        No issues identified.

Code scanned:
        Total lines of code: 400
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
Files skipped (0):
```

### `pipenv check`
```
16:45 ~/crud_rest_api (main) pipenv check
Checking PEP 508 requirements...
Passed!
Checking installed package safety...
All good!
```


