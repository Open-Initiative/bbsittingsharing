from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm

env.hosts = ['bbsittingsharing@ssh.alwaysdata.com']

def deploy():
    with cd('bbsittingsharing'):
        run("git pull origin master")
        run("git merge master")
#        run("./manage.py syncdb")
        run("./manage.py compilemessages")
        run("./manage.py collectstatic")
