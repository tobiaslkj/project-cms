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
source python-env/bin/activate
(venv) cd app
(venv) pip install -r requirements.txt
```
if pip install fails, use:
```
(venv) pip install --upgrade -r requirements.txt
```

### Run database installer~~
Firstly, please ensure that your a database is created in your mysql server. Then ensure that the ```.env``` file is setup correctly in your app with the correct parameters.
```
# .env file
# Database config
DATABASE_NAME=your database name
DATABASE_HOST=your database host
DATABASE_USERNAME=your database username
DATABASE_PASSWORD=your database password
```
Then proceed to run the command in your terminal with the correct python command. This command can also be run to create additional tables from models that you have pull from the code repository.
```
python3 create_db.py
```

If needed, you can run the command to drop all tables.
```
python3 drop_db.py
```

### Starting the application
Depending on your preferences, there are many ways to start the app. But do rember to **RENAME .env.example to .env AND SET THE VARIABLES INSIDE ACCORDING TO YOUR CONFIGURATION**. These configurations will auto be loaded to the environment by flask.

Ensure you are in your virtual environment

Starting the app:
```
flask run
```


### Workflow

#### Before commiting your changes
If you have installed any modules during your development, you will have to share this information with your fellow developers. And this is what the ```requirements.txt``` file in your root directory is for. If you did not install any dependecies, you can skip this step.

Ensure that you are in your virtual environment or you can push your system python dependecies to your fellow developers. Change directory to the project root and run the command.
```
(venv) pip freeze > requirements.txt
```

This command will consolidate all the dependencies required in your project into the requirements.txt file and you can commit your changes now!


#### Commiting your changes to github
Once you are done with your work module, you can easily push to the repository at github after you commit.
```
git add *
git commit -m "Your messages here"
git push
```


### Addtional resource that may help 
Some additional resource to help you all. Please feel free to add on.

https://realpython.com/instance-class-and-static-methods-demystified/
https://stackoverflow.com/questions/39983695/what-is-truthy-and-falsy-in-python-how-is-it-different-from-true-and-false
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world