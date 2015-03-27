import fabric.api as fab
from os import path

PYREPO_DIR = "/var/www/gefoo.org/pyrepo/"
PACKAGE_NAME = 'ubeity'

fab.env.roledefs = {
    'pyrepo': ['gefoo.org'],
    'prod': ['chef.lchome.net'],
    'staging': ['mixer.lchome.net']
}


@fab.task
def develop():
    """
    Setup dev environment
    """
    dev_pkgs = [
        'alembic',
        'ipython',
        'pytest',
        'pytest-xdist',
        'pytest-cov',
        'tox',
        'restview'
    ]

    if not path.exists("env"):
        fab.local("virtualenv env")
    fab.local("./env/bin/python setup.py develop")

    for dev_pkg in dev_pkgs:
        fab.local("./env/bin/pip install {}".format(dev_pkg))


@fab.roles('pyrepo')
@fab.task
def publish():
    fab.local("python setup.py sdist")
    tar_filename = fab.local("python setup.py --fullname", capture=True)
    fab.put("dist/{local_name}.tar.gz".format(local_name=tar_filename),
            PYREPO_DIR)


@fab.task
def doc():
    from os.path import abspath
    opts = {'builddir': '_build',
            'sphinx': abspath('env/bin/sphinx-build')}
    cmd = ('{sphinx} -b html '
           '-d {builddir}/doctrees . {builddir}/html')
    with fab.lcd('doc'):
        fab.local(cmd.format(**opts))


@fab.task
def bootstrap():
    pass


@fab.task
def test(coverage=False):
    """
    Start py.test and start unittesting
    """
    if coverage:
        fab.local("env/bin/py.test -f --color yes --cov ubiety/ ubiety")
    else:
        fab.local("env/bin/py.test -f --color yes ubiety")
