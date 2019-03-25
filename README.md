# Mesonet DB
The `mesonet_db` library provides python utilities supporting the Montana Mesonet database. [Read the docs here.](https://mt-climate-office.github.io/mesonet_db/)

## Installation
The `mesonet_db` library is not yet available on PyPI. Until then, install directly from Github using `pip`:

```bash
pip install git+https://github.com/mt-climate-office/mesonet_db
```

## Usage

### Loading the library
After installation, load the `mesonet_db` library with a standard import call to the `utils` module:

```python
import mesonet_db.utils
```

## Development
This project has been set up using PyScaffold 3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.

First, clone this project and change into the project directory:

``` bash
git clone https://github.com/mt-climate-office/mesonet_db
cd mesonet_db
```

Then, to install the library and its dependencies into your current python environment, run:

```bash
python setup.py develop
```

### Testing
This project uses [pytest](https://docs.pytest.org/en/latest/) for testing and coverage analysis.
To test, from the project directory run:

```bash
python setup.py test
```


<!--
### Documentation
This project uses [`pdoc`](https://github.com/mitmproxy/pdoc) to auto-generate documentation from docstrings in the code. Documentation was generated using this command in the terminal:
```bash
pdoc --html --html-dir docs --overwrite ./src/zentra/api.py
mv -i docs/api.m.html docs/index.html
```
-->
