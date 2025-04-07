# Description
This project includes a *very* small client to access data form 
the WebDataCollector-API. It is meant to provide a simple means 
of accessing the data in Json or as Panda-DataFrames.

More information about is availaible on its project homepage.

# Internal Notes for the Development Environment

## Initialize

	wdc-rest-api-python> poetry install

## Use cases

* Update dependencies: `poetry update`
	 
* Execute Python file: `poetry run python3 src/main.py`
	
* Running tests 
(https://pytest-with-eric.com/getting-started/poetry-run-pytest/)
	
	```
	poetry run pytest 
	poetry run pytest tests/test_module.py::testFunction
	poetry run pytest -s (with output from stdout and stderr)
	```
	
## Publish to PyPI
(https://python-poetry.org/docs/repositories/#publishable-repositories)
	
1. Config token (once)
	
	`poetry config pypi-token.pypi <my-token>`

2. Publish

	`poetry publish --build`
