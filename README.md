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

    (venv)$ ./manage.py test techism events ical rss

##Deployment

Create another virtualenv and install Fabric:

    $ virtualenv --no-site-packages venv-deploy
    $ pip install Fabric
    $ source venv-deploy/bin/activate
    (venv-deploy)$ pip install Fabric

Deploy to test environment:

    (venv-deploy)$ fab deploy_test

Deploy to production environment:

    (venv-deploy)$ fab deploy_prod
