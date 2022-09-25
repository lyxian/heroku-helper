# heroku-helper

Features:

- webserver to serve requests
- send exceptions from other telebots to user
- encryption key store
  - authentication server
  - authentication app

Requires:

- telebot API

# Development

**preprod**

- server routes
  - error logging
- telebot functions
  - error logging
- test

# TO-DO

- dynamic url for heroku/local in test
- error dashboard
- check why '/' is not returning json
  - 200 = OK
  - 201 = Created
  - 204 = No Content
  - 400 = Bad Request
  - 401 = Unauthorized
  - 403 = Forbidden
  - 404 = Not Found
  - 405 = Method Not Allowed

##Packages (list required packages & run .scripts/python-pip.sh)
flask
pyyaml
gunicorn
pendulum
apscheduler
cryptography
PyTelegramBotAPI
pytest==7.1.2
##Packages
