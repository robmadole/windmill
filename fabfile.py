import os

from fabric.api import env, run, put, local, roles
from pkginfo import version

env.hosts     = ['localbase.webfactional.com']
env.roledefs  = {'eggserver': ['localbase.webfactional.com']}
env.user      = 'localbase'
env.name_left = 'windmill'

@roles('eggserver')
def deploy():
    """Deploys Github version of Windmill to our eggs directory on Web Faction"""
    local('rm -rf dist/*')
    local('python setup.py sdist')

    dist_files = os.listdir('dist')

    filename = dist_files[0]

    local_filename  = 'dist/%s' % filename
    remote_filename = '/home/localbase/webapps/eggs/%s' % filename

    put(local_filename, remote_filename)
