import os
import sys
import json
import urllib
import tempfile
import shutil
from subprocess import Popen

VENV_URL = "https://pypi.python.org/pypi/virtualenv/json"
KNOWN_BINS = ['/usr/local/bin', '/opt/local/bin',
              os.path.join(os.environ['HOME'], '.bin'),
              os.path.join(os.environ['HOME'], '.local', 'bin')]

def find_user_paths():
    rv = []
    for item in os.environ['PATH'].split(':'):
        if os.access(item, os.W_OK) \
           and item not in rv \
           and '/sbin' not in item:
            rv.append(item)
    return rv

def bin_sort_key(path):
    try:
        return KNOWN_BINS.index(path)
    except ValueError:
        return float('inf')

def find_locations(paths):
    paths.sort(key=bin_sort_key)
    for path in paths:
        if path.startswith(os.environ['HOME']):
            return path, os.path.join(os.environ['HOME'],
                '.local', 'lib', 'lektor')
        elif path.endswith('/bin'):
            return path, os.path.join(
                os.path.dirname(path), 'lib', 'lektor')q


def wipe_installation(lib_dir, symlink_path):
    if os.path.lexists(symlink_path):
        os.remove(symlink_path)
    if os.path.exists(lib_dir):
        shutil.rmtree(lib_dir, ignore_errors=True)

def check_installation(lib_dir, bin_dir):
    symlink_path = os.path.join(bin_dir, 'lektor')
    if os.path.exists(lib_dir) or os.path.lexists(symlink_path):
        print '   Lektor seems to be installed already. Exiting.'

def fail(message):
    print 'Error: %s' % message
    sys.exit(1)

def install(virtualenv_url, lib_dir, bin_dir):
    t = tempfile.mkdtemp()
    Popen('curl -sf "%s" | tar -xzf - --strip-components=1' %
          virtualenv_url, shell=True, cwd=t).wait()

    try:
        os.makedirs(lib_dir)
    except OSError:
        pass
    Popen([sys.executable, './virtualenv.py', lib_dir], cwd=t).wait()
    Popen([os.path.join(lib_dir, 'bin', 'pip'),
       'install', '--upgrade', 'Lektor']).wait()
    os.symlink(os.path.join(lib_dir, 'bin', 'lektor'),
               os.path.join(bin_dir, 'lektor'))

def main():
    print
    print 'Welcome to Lektor'
    print
    print 'This script will install Lektor on your computer.'
    print

    paths = find_user_paths()
    if not paths:
        fail('None of the items in $PATH are writable. Run with '
             'sudo or add a $PATH item that you have access to.')

    bin_dir, lib_dir = find_locations(paths)
    if bin_dir is None or lib_dir is None:
        fail('Could not determine installation location for Lektor.')

    check_installation(lib_dir, bin_dir)

    print 'Installing at:'
    print '  bin: %s' % bin_dir
    print '  app: %s' % lib_dir
    print

    for url in json.load(urllib.urlopen(VENV_URL))['urls']:
        if url['python_version'] == 'source':
            virtualenv = url['url']
            break
    else:
        fail('Could not find virtualenv')

    install(virtualenv, lib_dir, bin_dir)

    print
    print 'All done!'

main()