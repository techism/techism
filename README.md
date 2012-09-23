##Setup

    $ sudo apt-get install python-pip python-virtualenv
    $ git clone git://github.com/techism/techism.git
    $ cd techism
    $ virtualenv --no-site-packages venv 
    $ source venv/bin/activate
    (venv)$ pip install -r dependencies.pip

##Development

Entwicklungsserver starten:

    (venv)$ python manage.py runserver

Oder:

    (venv)$ gunicorn_django techism

Dependencies speichern:

    (venv)$ pip freeze > dependencies.pip

##Deployment

    $ git remote add prod git@www.techism.de:techism
    $ git push prod master

