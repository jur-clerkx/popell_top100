# PopEll Top100
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)



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
  There's an [issue related to language and region settings](https://github.com/kennethreitz/pipenv/issues/538) that you might run into, but it's easy to resolve.
4. Run `pipenv install --ignore-pipfile --dev` to create a virtual environment with all dependencies installed.
  If you run into issues due to an existing virtual environment for this app, delete that environment by executing `pipenv --rm`.
5. Install the pre-commit hooks by executing `pre-commit install`. This makes sure `black` and `flake8` run before commits

Before executing any Python-related command, you need to activate the virtual environment that `pipenv` manages for this app.
You can do so by executing `pipenv shell`.
Afterwards, your command prompt should indicate that you've activated the virtual environment.
It can be deactivated by executing `exit`.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Django]: https://img.shields.io/badge/Django-0C4B33?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com