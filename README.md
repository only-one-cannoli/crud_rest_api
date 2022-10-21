# CRUD REST API

## Summary

This repo contains a basic create-read-update-delete (CRUD) API with standard endpoints (POST, GET, PATCH, and DELETE).  The Python code leverages the Tornado web framework and interfaces with a SQLite database.  It passes many tests with static-analysis tools (`black`, `isort`, `pylint`, `mypy`, `bandit`, `pytest`, and `pipenv check`).  After starting the app by issuing `pipenv run python -m src.main` from within the repo's top-level directory, commands like `requests.post('http://localhost:888/api/widgets', params={'name': 'widget1', 'parts': '5'})` yield reasonable responses.

## Getting started

You'll need `git`, Python 3.9, and `pipenv`.  After cloning down the repo, navigate into the repo's top-level directory and use `pipenv install` and `pipenv install -d` to get all of the packages set up within a virtual environment.  Remember to use `pipenv run` or `pipenv shell` to work within the virtual environment; otherwise, you'll be using whatever Python packages you have installed outside of the environment.

## Interactive session

Remember to run `pipenv run python -m src.main` and to keep the session open while attempting these commands.

```
19:48 ~/crud_rest_api (main) pipenv run ipython
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
Type 'copyright', 'credits' or 'license' for more information
IPython 8.5.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import requests

In [2]: url = 'http://localhost:8888/api/widgets/'
```

First, we run `requests.post()` in a loop to populate the database with some widgets.  We print the JSON content of the response each time; it contains the information that's being pushed to the database.

```
In [3]: for i in range(3):
   ...:     print(requests.post(url, params={'name':f'widget{i}', 'parts':str(i)}).json())
   ...: 
{'widgets': [{'uuid': '84f933c2-e43c-4eae-a14e-f322006c2beb', 'name': 'widget0', 'parts': '0', 'created': '2022-10-18T23:49:36.466473+00:00', 'updated': '2022-10-18T23:49:36.466473+00:00'}]}
{'widgets': [{'uuid': 'd91ebc64-9a06-4285-8ad4-31d310dfa41e', 'name': 'widget1', 'parts': '1', 'created': '2022-10-18T23:49:36.551389+00:00', 'updated': '2022-10-18T23:49:36.551389+00:00'}]}
{'widgets': [{'uuid': '985186fe-6372-43d5-8f5e-611208292fb0', 'name': 'widget2', 'parts': '2', 'created': '2022-10-18T23:49:36.575893+00:00', 'updated': '2022-10-18T23:49:36.575893+00:00'}]}
```

`requests.get()` with no `params` argument shows the full contents of the database, showing that all three widgets are in the database.

```
In [4]: requests.get(url).json()
Out[4]: 
{'widgets': [{'uuid': '84f933c2-e43c-4eae-a14e-f322006c2beb',
   'name': 'widget0',
   'parts': '0',
   'created': '2022-10-18T23:49:36.466473+00:00',
   'updated': '2022-10-18T23:49:36.466473+00:00'},
  {'uuid': 'd91ebc64-9a06-4285-8ad4-31d310dfa41e',
   'name': 'widget1',
   'parts': '1',
   'created': '2022-10-18T23:49:36.551389+00:00',
   'updated': '2022-10-18T23:49:36.551389+00:00'},
  {'uuid': '985186fe-6372-43d5-8f5e-611208292fb0',
   'name': 'widget2',
   'parts': '2',
   'created': '2022-10-18T23:49:36.575893+00:00',
   'updated': '2022-10-18T23:49:36.575893+00:00'}]}
```

Specifying either `name` or `uuid` through the `params` argument in a `requests.get()` call yields the expected results.

```
In [5]: requests.get(url, params={'name': 'widget1'}).json()
Out[5]: 
{'widgets': [{'uuid': 'd91ebc64-9a06-4285-8ad4-31d310dfa41e',
   'name': 'widget1',
   'parts': '1',
   'created': '2022-10-18T23:49:36.551389+00:00',
   'updated': '2022-10-18T23:49:36.551389+00:00'}]}

In [6]: requests.get(url, params={'uuid': '84f933c2-e43c-4eae-a14e-f322006c2beb'}).json()
Out[6]: 
{'widgets': [{'uuid': '84f933c2-e43c-4eae-a14e-f322006c2beb',
   'name': 'widget0',
   'parts': '0',
   'created': '2022-10-18T23:49:36.466473+00:00',
   'updated': '2022-10-18T23:49:36.466473+00:00'}]}
```

Specifying a nonexistent `uuid` has a different behavior for `requests.get()` compared to (e.g.) `requests.patch()`; `requests.get()` produces an empty result, whereas `requests.patch()` actually produces a custom error.

```
In [8]: requests.get(url, params={'uuid': 'not-a-real-uuid'}).json()
Out[8]: {'widgets': []}

In [12]: requests.patch(url, params={'uuid': 'not-a-real-uuid'}).text
Out[12]: '<html><title>500: No match for uuid in database!</title><body>500: No match for uuid in database!</body></html>'
```

Patching with a `uuid` that exists within the database produces the expected result.

```
In [14]: requests.patch(url, params={'uuid': '84f933c2-e43c-4eae-a14e-f322006c2beb', 'name': 'another widget'}).json()
Out[14]: 
{'widgets': [{'uuid': '84f933c2-e43c-4eae-a14e-f322006c2beb',
   'name': 'another widget',
   'parts': '0',
   'created': '2022-10-18T23:49:36.466473+00:00',
   'updated': '2022-10-18T23:49:36.466473+00:00'}]}

In [15]: requests.get(url, params={'uuid': '84f933c2-e43c-4eae-a14e-f322006c2beb'}).json()
Out[15]: 
{'widgets': [{'uuid': '84f933c2-e43c-4eae-a14e-f322006c2beb',
   'name': 'another widget',
   'parts': '0',
   'created': '2022-10-18T23:49:36.466473+00:00',
   'updated': '2022-10-21T02:16:09.687233+00:00'}]}
```

Deleting also works well.

```
In [16]: requests.delete(url, params={"uuid": 'd91ebc64-9a06-4285-8ad4-31d310dfa41e'})
Out[16]: <Response [200]>
```

The final state of the database reflects both the patch and delete operations.

```
In [18]: requests.get(url).json()
Out[18]: 
{'widgets': [{'uuid': '84f933c2-e43c-4eae-a14e-f322006c2beb',
   'name': 'another widget',
   'parts': '0',
   'created': '2022-10-18T23:49:36.466473+00:00',
   'updated': '2022-10-18T23:49:36.466473+00:00'},
  {'uuid': '985186fe-6372-43d5-8f5e-611208292fb0',
   'name': 'widget2',
   'parts': '2',
   'created': '2022-10-18T23:49:36.575893+00:00',
   'updated': '2022-10-18T23:49:36.575893+00:00'}]}
```

## TODO

* Add pagination to the `get` endpoint.  For this toy example, viewing the entire database is fine; however, restricting the view to some fraction of the overall database would clearly be necessary if the database grows to any appreciable size.
* Add additional filters to the `get` endpoint to allow searching by number of parts and the created and updated datetimes.  Rather than exact matching, filters that permit greater-than, less-than, and within-a-given-range searches would clearly be useful.
* Similarly, add case-insensitive searching and partial matches on widget names.
* Add proper tests to the app itself.  The existing tests cover only the direct interfaces with the database.
