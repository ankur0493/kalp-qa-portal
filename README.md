Kalprvruksh Q&A Portal
======================

A minimalistic Q&A application with following features:

- [x] REST API to allow consumers to retrieve Questions with Answers as JSON. The response includes Answers inside their Question as well as include the id and name of the Question and Answer users.
- [x] Private Questions are not returned by default in the API response.
- [x] Every API request requires a valid Tenant API key to be included
- [x] API request counts are tracked per Tenant
- [x] An HTML dashboard page as the root URL that shows the total number of Users, Questions, and Answers in the system, as well as Tenant API request counts for all Tenants
- [ ] Tests for all code
- [ ] Questions can be filtered on query terms by adding a query parameter to the API Request
- [x] API requests are throttled on a per-Tenant basis. After the first 100 requests per day, only 1 request per 10 seconds is allowed

Installation
============
- Preferred way is to install it inside a virtualenvironment
- Make sure you have Python 2.7 installed on your machine
- Install pip and virtualenvironment if not already installed
  ```
  sudo apt-get update
  sudo apt-get install python-pip
  sudo pip install virtualenv
  ```
- Create a directory to store your virtual enironments (if does not already exist):
  ```
  mkdir ~/env/
  ```
- Create a virtualenv for the project:

  ```
  virtualenv --python=/usr/bin/python2.7 ~/env/qaportal
  ```
- Activate the virtual environment:

  ```
  source ~/env/qaportal/bin/activate
  ```
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py loaddata fixtures/*
- python manage.py runserver
