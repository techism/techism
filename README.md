##Setup

    $ sudo apt-get install python-pip python-virtualenv
    $ git clone git://github.com/techism/techism.git
    $ cd techism
    $ virtualenv --no-site-packages venv 
    $ source venv/bin/activate
    (venv)$ pip install -r dependencies.pip

##Development

Start local development server:

    (venv)$ python manage.py runserver

or

    (venv)$ gunicorn_django techism

Save dependencies:

    (venv)$ pip freeze > dependencies.pip

Run tests:

    (venv)$ ./manage.py test techism events ical rss twitter

Edit test data:

    $ cd test-utils
    $ vi fixture_template.json

Available Placeholders:
YESTERDAY
TOMORROW
NEXTWEEK

##Deployment

Create another virtualenv and install Fabric:

    $ virtualenv --no-site-packages venv-deploy
    $ source venv-deploy/bin/activate
    (venv-deploy)$ pip install Fabric

Deploy to staging environment:

    (venv-deploy)$ fab deploy_staging

Deploy to production environment:

    (venv-deploy)$ fab deploy_production

There needs to be an SSH key stored on the server.

SSH fingerprint of the server is: 50:09:98:00:60:19:f4:b8:c1:4f:af:35:91:0c:38:d5
