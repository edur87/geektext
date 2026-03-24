# Quick Start for MacOS

## 1. Install the Essentials

###Download Brew on their [Brew website](https://brew.sh)

### Python

**brew install python**
*python3 --version*
*pip3 --version*

###Git
*git --version*

**if _missing_**
**brew install git**


## 2. Create a branch + Virtual environment

**Create a branch [here](https://github.com/edur87/geektext)
*Open branch with code editor of choice and run these code below * **VS Code (Reccomended)**

*python3 -m venv .venv*
*source .venv/bin/activate*

*python -m pip install --upgrade pip*

## 3. Install Django + Rest Framework

*pip install django djangorestframework*


## 4. Run project

*python manage.py migrate*

*python manage.py runserver*
