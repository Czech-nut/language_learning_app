# Language Learning App

## Local Setup
### Dependencies
For dependency management we use `poetry`. 
More on the installation if you don't have it installed yet, can be found [here](https://python-poetry.org/docs/#installation).

After the installation you need to create a virtual environment from `backend` directory with  Python 3.10.7 and activate it. 
You can do that using any module you prefer, poetry also proposes their envs, but that's not obligatory.

After the environment is activated, you need to install dependencies using `poetry`: [here's how](https://python-poetry.org/docs/cli/#install).

### Database
We use PostgreSQL.
To point the application to it, you need to create `.env` file in the root directory where you set your local credentials. 

That's how the `.env` file should look like:
```
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_NAME = "postgres"

SECRET_KEY = ""
REFRESH_SECRET_KEY = ""
```

### Code style
With `poetry` we also install the following code style/linting tools:
- [black](https://black.readthedocs.io/en/stable/)
- [flake8](https://flake8.pycqa.org/en/latest/)
- [isort](https://pycqa.github.io/isort/)

You will need to run them from the root dir before commiting your code. No specific params are required.
```bash
black .
```

```bash
flake8
```

```bash
isort .
```
