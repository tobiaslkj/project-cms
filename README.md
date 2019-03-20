# Project CMS
---
This repository contains the source code for Project CMS backend. The python version used is 3.7.2

## Setup the project 

### Clone this repo
Make a directory and change to the directory that you want your project to be stored. This directory will contain the virtual env folder as well.
```
mkdir codes
cd codes
git clone https://github.com/tobiaslim/project-cms.git ./app
```

### Setup python virtual env

As you are coding this project, you should use at least python 3.7.2. Thus we will use the built in venv python module to create the virutal env ```python-env``` or any name you desire.

Assuming your python command is python3:
```
python3 -m venv python-env
```


### Install package dependencies
After you have done setting up the virtual environment, activate it and install the required dependecies
For macOS:
```
source app/python-env/bin/activate
pip install app/requirements.txt
```

### Run database installer
```
cd app
python3 create_db.py
```

