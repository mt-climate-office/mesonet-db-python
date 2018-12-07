# zentra
Meter Zentra Cloud API Interface for Montana Mesonet Stations

## Setting up project
Dependency and environment management is provided by [Conda](https://conda.io/docs/) and is described in the [environment.yml] file. To build the environment, install conda and simply run this from your console:

``` bash
conda env create -f environment.yml -p envs/mesonet_db
```

To activate the environment, run:

```bash
source activate envs/mesonet_db
```

To deactivate:
```bash
source deactivate
```

