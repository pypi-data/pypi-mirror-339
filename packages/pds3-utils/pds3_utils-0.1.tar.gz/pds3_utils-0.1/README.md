# pds3_utils
A module of utilities to work with PDS3 data, built on top of pvl.


## Dependencies

The following dependencies must be met:
- python 3
- pandas
- pyyaml
- pvl

## Installation

### pip

```pip install pds3_utils```

should do the job, although creating a dedicated environment is recommended (see below).

### conda

First, clone this repository. If you are using conda, the dependencies can be installed in a new environment using the provided environment file:

```conda env create -f environment.yml```

The newly created environment can be activated with:

```conda activate pds3_utils```

Otherwise, please make sure the dependencies are installed with your system package manager, or a tool like `pip`. Use of a conda environment or virtualenv is recommended!

The package can then be installed with:

```python setup.py install```


## Usage

### index_products(directory='.', pattern='*.lbl', recursive=True):

This function loads the labels of products with `pattern` in `directory` (recursively if requested) and retrieves key hard-coded meta-data and loads them into a pandas dataframe:

- PRODUCT_ID
- INSTRUMENT_ID
- DATA_SET_ID
- MISSION_ID
- START_TIME
- STOP_TIME

###  Database (class) 

The Database class is used to create one or more tables (pandas DataFrames) from PDS3 meta-data according to a configuration file. This can be retrieved, saved to/loaded from disk and used in later analysis.

This class is instantiated with:
```python
files=None, directory='.', config_file=default_config, recursive=True
```
where files, directory and recursive are as above. `config_file` gives the filepath to a YAML formatted file which defines which additional meta-data are retrieved.

The configuration file has a format like:

```yaml
INSTRUMENT_ID:
  table_name:
    prod_id: "TEST_RAW"
    keywords:
      altitude:
        path: 'ALTITUDE'
      pixel_x:
        path: 'IMAGE_POI/IMAGE_POI_PIXEL'
        index: 0
      pixel_y:
        path: 'IMAGE_POI/IMAGE_POI_PIXEL'
        index: 1
```
In this case when using this configuration, any PDS3 products in `directory` with file pattern `files` will be checked for INSTRUMENT_ID. For those that match, each `table_name` entry will be used to defined a unique table built from products with PRODUCT_ID containing `prod_id`. Keywords then specify fields to be scraped from the labels.

For simple key/pair entries, it is only necessary to specify the keyword (e.g. `altitude` above) which will be used as the field name in the database, and the path (e.g. `ALTITUDE`). If the keyword has an attached unit, this wil be ignored and the value used. For keywords that have lists, the `index` parameter can be used to select which one is mapped into the corresponding field.

Putting this together with a few examples:

```
SC_TARGET_POSITION_VECTOR        = (-23.936 <km>, -43.917 <km>, -31.456 <km>)
```

to retrieve the 3 components, one would specify something like:

```yaml
      sc_position_x:
        path: 'SC_TARGET_POSITION_VECTOR'
        index: 0
      sc_position_x:
        path: 'SC_TARGET_POSITION_VECTOR'
        index: 1
      sc_position_x:
        path: 'SC_TARGET_POSITION_VECTOR'
        index: 2
```

In the case of groups, the input file should use a slash to describe the path, for example:

```

GROUP                            = SCIENCE_ACTIVITY
ROSETTA:MISSION_PHASE            = ("LTP001", "MTP006", "STP015")
ROSETTA:RATIONALE_DESC           = "NUCLEUS"
ROSETTA:OPERATIONAL_ACTIVITY     = "TAG_NUCLEUS_SHAPE"
ROSETTA:ACTIVITY_NAME            = "STP015_SHAP4S_002"
END_GROUP                        = SCIENCE_ACTIVITY
```

to get the mission phase here, one would use:

```yaml
      ltp:
        path: 'SCIENCE_ACTIVITY/ROSETTA:ROSETTA:MISSION_PHASE'
        index: 0
      mtp:
        path: 'SCIENCE_ACTIVITY/ROSETTA:ROSETTA:MISSION_PHASE'
        index: 1
      stp:
        path: 'SCIENCE_ACTIVITY/ROSETTA:ROSETTA:MISSION_PHASE'
        index: 2
```


## Example

The Jupyter notebook included with this repository shows an example of how to use the code. To view the notebook, click [here](https://nbviewer.jupyter.org/github/msbentley/pds3_utils/blob/master/pds3_utils_example.ipynb).
