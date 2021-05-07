# Why
This tool allows to work collect and visualize easily scripts runned with Hydra. With it you can sort runs and experiment per tag, hyperparameters, group, etc.
You can also export and visualize them by different ways using streamlit and plotly. 
Here a working example http://138.131.217.125:8501/

# Installation 
For adding CSEM_ExperimentTracker as a submodules in a repo for the first time just run:
`git submodule add git@gitlab.csem.local:611/csem_experimenttracker.git`
Then add and commit the two files 

```
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   .gitmodules
        new file:   csem_experimenttracker
```

When cloning the repo with a submodule remember to add `--recurse-submodules --remote-submodules` to the git clone command. Otherwise submodules will not be used.


Then install the repo as:
`pip install -e csem_experimenttracker/`

# Getting started
## Collect your results
Let's assume you have run an experiment "my_experiment" of 3 runs (see below for the terminology) on 2021-01-26 at 17:07:39. And that, for each run you are saving a npy file and a log file. 

```
my_experiment/
└── 2021-01-26
    └── 17-07-39
        ├── 0
        │   ├── .hydra
        │   │   ├── config.yaml
        │   │   ├── hydra.yaml
        │   │   └── overrides.yaml
        │   ├── lstm_finetuning.log
        │   └── metric.npy
        ├── 1
        │   ├── .hydra
        │   │   ├── config.yaml
        │   │   ├── hydra.yaml
        │   │   └── overrides.yaml
        │   ├── lstm_finetuning.log
        │   └── metric.npy
        ├── 2
        │   ├── .hydra
        │   │   ├── config.yaml
        │   │   ├── hydra.yaml
        │   │   └── overrides.yaml
        │   ├── lstm_finetuning.log
        │   └── metric.npy
        └── multirun.yaml
```

The following code snippets will return a pd.DataFrame containing the parameters for each and the path to your results (i.e. the npy files).

```python
from csem_exptrack import process
loader = process.file_loader.FileLoader(query_string="*.npy")
df = loader.load_folder("my_experiment")
```

if you want to return also the path to your log files you can pass a list instead of a string as parameter to query_string 

```python
from csem_exptrack import process
loader = process.file_loader.FileLoader(query_string=["*.npy","*.log"])
df = loader.load_folder("my_experiment")
```

The returned pd.DataFrame contains the paths of your results relative to the folder where you run your code the parameters, from .hydra/config, of each run.
The pd.DataFrame has hierchical structure, both for columns and rows.
Columns:
- Level 0: **Date**: the path to the results (npy file)
- Level 1: **Run**: the name of the parameter you used in your .hydra/config file
Rows:
- Level 0: **Group**: See below "formatting the hydra file"
- Level 1: **parameters**: See below "formatting the hydra file"




This module offers a series of utility functions and templates for creating your own GUI.
You should be some what familiar with Streamlit. If you aren't, just spend 20 minutes looking at https://docs.streamlit.io/en/stable/getting_started.html

CSEM_ExperimentTracker is module tha comprises of two main sub-modules (plus a bunch of utilities .py files)
- GUI. Here will find modules about implementing graphical widget, plots and GUI utilities.

- Process. Here you will modules processing hydra like structure.  base_loader.py is the abstract class that needs to be implemented depeding for your specific type of experiment. You can find this already for lightning.

Start by looking at loading_data.py in examples. This allows you to collect programmatically the path of any file that matches a string (query_string).
The returned pandas dataframe contains all but rows from the Hydra file. The last row is the path of the desired file. You can access it with df.loc["path"]
# Terminology (Based on WandB):

- **Project**: A collection of one or more experiments. (Each _Project_ has one or more days sub-folders, and then one or more time sub-folders) 
- **Experiment**: A collection of one or more runs. Each experiment contains one or more runs subfolders 
- **Run**: A training of a learning algorithm plus its performance evaluation 

# Important
If you want to use the parallel coordinate plots all yours hyperparameters should be indented and included in hyperparameters. Example:
```
hyperparameters:
  lm_bs: 128 
  lm_last_layer_epochs: 7
  lm_all_layers_epochs: 6
```

Adding a key called random_seed will allow you to average plots.

Metrics should be added to the resulting pandas dataframe creating new rows with levels ("metrics",NameOfYourMetric)

# Structure of the resulting pandas dataframe 
The base loader returns an hierchical pandas dataframe. This contains all parameters, plus paths to import files. The name of this pandas dataframe is param_df
In addition to this, each plotting function requires another pandas dataframe, called df_parallel_coordinate

# To Do 
1) Allow multiple query strings at the same time
2) Add better documentation for plots
