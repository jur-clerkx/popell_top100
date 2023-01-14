# PopEll Top100

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=popell-top100&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=popell-top100) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=popell-top100&metric=coverage)](https://sonarcloud.io/summary/new_code?id=popell-top100) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Built With

* [![Django][Django]][Django-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]

## Setting up a development environment

### Back end

1. Install the Python version specified in the file `PipFile`.
   You can use [pyenv](https://github.com/pyenv/pyenv) to manage the Python version for you.
2. Install [pip](https://pypi.org/project/pip/), if necessary.
   If you've used `pyenv` to install Python, `pip` has been installed as well.
3. Install [pipenv](https://pipenv.readthedocs.io/) by executing `pip install pipenv`.
   There's an [issue related to language and region settings](https://github.com/kennethreitz/pipenv/issues/538) that
   you might run into, but it's easy to resolve.
4. Run `pipenv install --ignore-pipfile --dev` to create a virtual environment with all dependencies installed.
   If you run into issues due to an existing virtual environment for this app, delete that environment by
   executing `pipenv --rm`.
5. Install the pre-commit hooks by executing `pre-commit install`. This makes sure `black` and `flake8` run before
   commits

Before executing any Python-related command, you need to activate the virtual environment that `pipenv` manages for this
app.
You can do so by executing `pipenv shell`.
Afterwards, your command prompt should indicate that you've activated the virtual environment.
It can be deactivated by executing `exit`.

## Running the development setup

By default, the project uses the development settings. This includes having the project in debug mode. However, some
things still have to be set to make sure the spotify integration works on your local machine:

- Set the `SPOTIFY_CLIENT_ID` in the environment variables to your spotify API client ID
- Set the `SPOTIFY_CLIENT_SECRET` in the environment variables to your spotify API client secret
- Set the `SPOTIPY_REDIRECT_URI` in the environment variables to a local URL for the spotify OAuth callback.
  E.g. `localhost:9999` would work (port must be available)

## Running the app in production

To deploy the app in production configuration, make sure the following settings are configured:

- Make sure the app uses the `popell_top100.prod_settings` settings file
- Set the `SPOTIFY_CLIENT_ID` in the environment variables to your spotify API client ID
- Set the `SPOTIFY_CLIENT_SECRET` in the environment variables to your spotify API client secret
- Set the `SPOTIPY_REDIRECT_URI` in the environment variables to a URL for the spotify OAuth callback that redirects to
  your server. This port has to be open to the server. E.g. `example.com:9999`.

### Database configuration

Production doesn't use SQLite but PostgresSQL. The following configurations are needed to setup the database connection:

- In the working directory, create the `.pg_service.conf` file with the following contents:
  ```properties
  [popell_top100]
  host=<db_host>
  user=<db_username>
  dbname=<db_name>
  port=<db_port>
  ```
- In the working directory, create the `.my_pgpass` file, containing the connection string to the db:
  ```text
  <db_host>:<db_port>:<db_name>:<db_user>:<db_password>
  ```

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[Django]: https://img.shields.io/badge/Django-0C4B33?style=for-the-badge&logo=django&logoColor=white

[Django-url]: https://www.djangoproject.com/

[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white

[Bootstrap-url]: https://getbootstrap.com