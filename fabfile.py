from __future__ import with_statement
from fabric.api import local, prefix, run, cd, env
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from contextlib import contextmanager as _contextmanager


env.hosts = ["deploy@next.techism.de:2222"]

BASE_DIR = "/srv/www"
GIT_REPO_DIR = "techism.git"
TEST_DIR = "techism-test"
PROD_DIR = "techism-prod"
DB_FILENAME = "techism.sqlite"

def _git_push():
    with cd(BASE_DIR):
        if not exists(GIT_REPO_DIR):
            run("git init --bare %s" % GIT_REPO_DIR)
    local("git push --tags ssh://%s@%s:%s%s/%s master" % (env.user, env.host, env.port, BASE_DIR, GIT_REPO_DIR))

def _clean_checkout(target_dir):
    with cd(BASE_DIR):
        if exists(target_dir):
            with cd(target_dir):
                run("git reset --hard")
                run("git clean -d -f")
                run("git pull")
        else:
            run("git clone %s %s" % (GIT_REPO_DIR, target_dir))
        run("chmod 775 %s" % target_dir)

def _setup_venv(target_dir):
    with cd(BASE_DIR), cd(target_dir):
        if not exists("venv"):
            run("virtualenv --no-site-packages --setuptools venv")
        with _virtualenv():
            run("pip install --download-cache /srv/www/pip-download-cache -r dependencies.pip")

def _manage_test_db(target_dir):
    with cd(BASE_DIR), cd(target_dir):
        if exists(DB_FILENAME) and not confirm("Keep test DB?", default=True): 
            run("rm techism.sqlite")
        if not exists(DB_FILENAME) and exists("../%s/%s" % (PROD_DIR, DB_FILENAME)) and confirm("Copy prod DB?", default=True):
            run("sqlite3 ../%s/%s '.backup %s'" % (PROD_DIR, DB_FILENAME, DB_FILENAME))

def _migrate_db(target_dir):
    with cd(BASE_DIR), cd(target_dir):
        with _virtualenv():
            run("./manage.py syncdb")
            run("chmod 664 %s" % DB_FILENAME)

def _collect_static(target_dir):
    with cd(BASE_DIR), cd(target_dir):
        with _virtualenv():
            run("./manage.py collectstatic --noinput")

@_contextmanager
def _virtualenv():
    with prefix("source venv/bin/activate"):
        yield

def deploy_test():
    _git_push()
    _clean_checkout(TEST_DIR)
    _setup_venv(TEST_DIR)
    _manage_test_db(TEST_DIR)
    _migrate_db(TEST_DIR)
    _collect_static(TEST_DIR)
    run("sudo supervisorctl restart techism-test")
    
def deploy_prod():
    _git_push()
    _clean_checkout(PROD_DIR)
    _setup_venv(PROD_DIR)
    _migrate_db(PROD_DIR)
    _collect_static(PROD_DIR)
    run("sudo supervisorctl restart techism-prod")


