from fabric.api import local, prefix, run, cd, env
from fabric.context_managers import shell_env
from fabric.utils import abort
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from contextlib import contextmanager as _contextmanager
import datetime


env.hosts = ["techism@next.techism.de:2222"]

BASE_DIR = "/srv/www"
GIT_REPO_DIR = "techism.git"
PIP_DOWNLOAD_CACHE_DIR = "pip-download-cache"
STAGING_DIR = "techism-staging"
STAGING_LOG_DIR = "techism-staging-log"
STAGING_BLUE_DIR = "techism-staging-blue"
STAGING_GREEN_DIR = "techism-staging-green"
STAGING_SETTINGS = "techism.settings.staging"
STAGING_WSGI = "techism/settings/staging_wsgi.py"
STAGING_DB_NAME = "techisms"
PRODUCTION_DIR = "techism-production"
PRODUCTION_LOG_DIR = "techism-production-log"
PRODUCTION_BLUE_DIR = "techism-production-blue"
PRODUCTION_GREEN_DIR = "techism-production-green"
PRODUCTION_SETTINGS = "techism.settings.production"
PRODUCTION_WSGI = "techism/settings/production_wsgi.py"
PRODUCTION_DB_NAME = "techismp"
PRODUCTION_DB_BACKUP_DIR = "/backup/production-db"

def __git_push():
    with cd(BASE_DIR):
        if not exists(GIT_REPO_DIR):
            run("git init --bare %s" % GIT_REPO_DIR)
    local("git push --tags ssh://%s@%s:%s%s/%s master" % (env.user, env.host, env.port, BASE_DIR, GIT_REPO_DIR))

def __clean_checkout(target_dir):
    with cd(BASE_DIR):
        if exists(target_dir):
            with cd(target_dir):
                run("git reset --hard")
                run("git clean -d -f")
                run("git pull")
        else:
            run("git clone %s %s" % (GIT_REPO_DIR, target_dir))
        run("chmod 775 %s" % target_dir)

def __setup_venv(target_dir):
    with cd(BASE_DIR):
        if not exists(PIP_DOWNLOAD_CACHE_DIR):
            run("mkdir %s" % PIP_DOWNLOAD_CACHE_DIR)
        with cd(target_dir):
            if not exists("venv"):
                run("virtualenv --system-site-packages venv")
            with __virtualenv():
                run("pip install --download-cache %s/%s -r dependencies.pip" % (BASE_DIR, PIP_DOWNLOAD_CACHE_DIR))

def __create_log_dir(log_dir):
    with cd(BASE_DIR):
        if not exists(log_dir):
            run("mkdir %s" % log_dir)

def __manage_staging_db():
    if confirm("Drop staging DB?", default=False): 
        run("dropdb %s" % STAGING_DB_NAME)
        run("createdb -E UTF8 -T template0 %s" % STAGING_DB_NAME)
        if confirm("Copy production DB?", default=True):
            run("pg_dump %s | psql %s" % (PRODUCTION_DB_NAME, STAGING_DB_NAME))

def __backup_db(db_name):
    with cd(PRODUCTION_DB_BACKUP_DIR):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')
        backup_file_name = now + ".pg_dump"
        run("pg_dump %s > %s" % (db_name, backup_file_name))

def __migrate_db(target_dir, django_settings_module):
    with cd(BASE_DIR), cd(target_dir):
        with __virtualenv(), shell_env(DJANGO_SETTINGS_MODULE=django_settings_module):
            run("./manage.py syncdb")
            run("./manage.py migrate")

def __run_tests(target_dir, django_settings_module):
    with cd(BASE_DIR), cd(target_dir):
        with __virtualenv(), shell_env(DJANGO_SETTINGS_MODULE=django_settings_module):
            run("./manage.py test techism events ical rss twitter organizations")

def __collect_static(target_dir):
    with cd(BASE_DIR), cd(target_dir):
        with __virtualenv():
            run("./manage.py collectstatic -v 0 --noinput")

def __create_active_symlink(next_active_dir, active_dir):
    with cd(BASE_DIR):
        if exists(active_dir):
            run("rm %s" % active_dir)
        run("ln -s %s %s" % (next_active_dir, active_dir))

def __get_next_active_dir(active_dir, blue_dir, green_dir):
    with cd(BASE_DIR):
        if exists(active_dir):
            # aborts is active dir is not a link
            current_active_dir = run("readlink %s" % active_dir)
            if current_active_dir == blue_dir:
                return green_dir
            elif current_active_dir == green_dir:
                return blue_dir
            else:
                abort("Unknown current active directory: %s" % current_active_dir)
        elif exists(blue_dir) or exists(green_dir):
            abort("Neither %s nor %s must exist." % (blue_dir, green_dir))
        else:
            return blue_dir

def __touch_wsgi(target_dir, wsgi_path):
    with cd(BASE_DIR), cd(target_dir):
        run("touch %s" % wsgi_path)

def __install_crontab(target_dir):
    with cd(BASE_DIR), cd(target_dir):
        run("crontab < conf/crontab")

@_contextmanager
def __virtualenv():
    with prefix("source venv/bin/activate"):
        yield

def deploy_staging():
    __git_push()
    next_staging_dir = __get_next_active_dir(STAGING_DIR, STAGING_BLUE_DIR, STAGING_GREEN_DIR)
    __clean_checkout(next_staging_dir)
    __setup_venv(next_staging_dir)
    __create_log_dir(STAGING_LOG_DIR)
    __run_tests(next_staging_dir, STAGING_SETTINGS)
    __manage_staging_db()
    __migrate_db(next_staging_dir, STAGING_SETTINGS)
    __collect_static(next_staging_dir)
    __install_crontab(next_staging_dir)
    __create_active_symlink(next_staging_dir, STAGING_DIR)
    __touch_wsgi(next_staging_dir, STAGING_WSGI)
    
def deploy_production():
    __git_push()
    next_prod_dir = __get_next_active_dir(PRODUCTION_DIR, PRODUCTION_BLUE_DIR, PRODUCTION_GREEN_DIR)
    __clean_checkout(next_prod_dir)
    __setup_venv(next_prod_dir)
    __create_log_dir(STAGING_LOG_DIR)
    __backup_db(PRODUCTION_DB_NAME)
    __migrate_db(next_prod_dir, PRODUCTION_SETTINGS)
    __collect_static(next_prod_dir)
    __install_crontab(next_prod_dir)
    __create_active_symlink(next_prod_dir, PRODUCTION_DIR)
    __touch_wsgi(next_prod_dir, PRODUCTION_WSGI)

