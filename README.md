# CTFmanager
Staging: http://ctfmanstaging.joepseuren.xyz
Uses Etherpad to create a powerfull tool to manage and play with a CTF team

Written in Django.

# Features

- User Stat Tracking
- Collaboration Solutions
- Event Planning
- Writeup support
- Scoreboard
- Groups

# Installation
You can load this project with Pycharm to run it, or follow the steps below to deploy the website localy or remote.
## Local
### Requirements
- python3
- pip3

### Steps
I assume you are in the project root, where manage.py is located
- Clone into any folder
- pip3 install -r requirements.txt
- python3 manage.py migrate
- python3 manage.py runserver

## Remote
### Requirements
- gunicorn
- nginx

### Steps
/Deploy_tools holds a fabfile that automaticly creates the necessary folders and virtualenv in your accounts home directory.
Example:fab deploy:host=your_username@subdomain.domain.org
There are also templates for a gunicorn start up script and a nginx template.
You have to replace 'SITE' with the websites domain name.

