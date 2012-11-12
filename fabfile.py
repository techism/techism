from fabric.api import local, prefix, run, cd, env
from fabric.utils import abort
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from contextlib import contextmanager as _contextmanager


env.hosts = ["deploy@next.techism.de:2222"]

BASE_DIR = "/srv/www"
GIT_REPO_DIR = "techism.git"
TEST_DIR = "techism-test"
PROD_DIR = "techism-prod"
PROD_BLUE_DIR = "techism-prod-blue"
PROD_GREEN_DIR = "techism-prod-green"
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

def _copy_prod_db(target_dir):
    with cd(BASE_DIR), cd(target_dir):
        if exists("../%s/%s" % (PROD_DIR, DB_FILENAME)):
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

def _create_prod_symlink(next_prod_dir):
    with cd(BASE_DIR):
        if exists(PROD_DIR):
            run("rm %s" % PROD_DIR)
        run("ln -s %s %s" % (next_prod_dir, PROD_DIR))

def _get_next_prod_dir():
    with cd(BASE_DIR):
        if exists(PROD_DIR):
            # aborts is PROD_DIR is not a link
            current_prod_dir = run("readlink %s" % PROD_DIR)
            if current_prod_dir == PROD_BLUE_DIR:
                return PROD_GREEN_DIR
            elif current_prod_dir == PROD_GREEN_DIR:
                return PROD_BLUE_DIR
            else:
                abort("Unknown current prod directory: %s" % current_prod_dir)
        elif exists(PROD_BLUE_DIR) or exists(PROD_GREEN_DIR):
            abort("Neither %s nor %s must exist." % (PROD_BLUE_DIR, PROD_GREEN_DIR))
        else:
            return PROD_BLUE_DIR

@_contextmanager
def _virtualenv():
    with prefix("source venv/bin/activate"):
        yield

def deploy_test():
    _git_push()
    run("sudo supervisorctl stop techism-test")
    _clean_checkout(TEST_DIR)
    _setup_venv(TEST_DIR)
    _manage_test_db(TEST_DIR)
    _migrate_db(TEST_DIR)
    _collect_static(TEST_DIR)
    run("sudo supervisorctl start techism-test")
    
def deploy_prod():
    _git_push()
    next_prod_dir = _get_next_prod_dir()
    _clean_checkout(next_prod_dir)
    _setup_venv(next_prod_dir)
    _copy_prod_db(next_prod_dir)
    _migrate_db(next_prod_dir)
    _collect_static(next_prod_dir)
    run("sudo supervisorctl stop techism-prod")
    _create_prod_symlink(next_prod_dir)
    run("sudo supervisorctl start techism-prod")

