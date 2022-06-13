#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Script to control simple_order server.
'''
from pathlib import Path
import argparse
import datetime
import os
import pwd
import subprocess
import sys


USER = 'simple-order'
DATA_DIR = Path(f'/home/{USER}/so-data')
TMP_DIR = DATA_DIR / 'temp'
DUMPS_DIR = DATA_DIR / 'dbdumps'
STATIC_DIR = DATA_DIR / 'static'
PYTHON_DIR = Path('/opt/simple-order')
USWGI_INI = PYTHON_DIR / 'simple_order/scripts/uwsgi.ini'
MAX_DUMPS = 10


def _exec(*args):
    print('>>> %s' % ' '.join(args))
    shell = len(args) == 1
    p = subprocess.run(args, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr, shell=shell)
    sys.stdout.flush()
    sys.stderr.flush()
    return p.returncode


def run():
    print('---- Simple order control ----')
    # parse args
    parser = argparse.ArgumentParser(description=__doc__.strip())
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'dump', 'update', 'shell', 'createsuperuser'], help='Action to run.')
    args = parser.parse_args()
    # Check user
    user = pwd.getpwuid(os.getuid()).pw_name
    if user != USER:
        print(f'Switching user to {USER}.')
        sys.stdout.flush()
        os.execl('/usr/sbin/runuser', 'runuser', '-u', USER, '--', *sys.argv)
        sys.exit(1)
    # Write initial info in log
    now = datetime.datetime.now()
    print(f'Started on {now.strftime("%Y-%m-%d %H:%M:%S")} by user {user}.')
    # Check current dir
    os.chdir(PYTHON_DIR)
    sys.path.pop(0)
    sys.path.append(str(PYTHON_DIR))
    # Run action
    if args.action in ('dump', 'update'):
        dump()
    if args.action == 'update':
        update()
    if args.action in ('start', 'restart', 'stop', 'update'):
        stop()
    if args.action in ('start', 'restart', 'update'):
        start()
    if args.action == 'shell':
        shell()
    if args.action == 'createsuperuser':
        createsuperuser()
    sys.exit(0)


def dump():
    print('---- Dumping database ----')
    from simple_order import settings
    dump_cmd = None
    if hasattr(settings, 'DATABASES') and settings.DATABASES.get('default'):
        dbs = settings.DATABASES.get('default')
        now = datetime.datetime.now()
        if 'sqlite' in dbs.get('ENGINE'):
            db_path = dbs.get('NAME')
            if db_path and Path(db_path).exists():
                dump_path = DUMPS_DIR / f'{now.strftime("%Y-%m-%d_%H-%M-%S")}.db'
                dump_cmd = f'cp "{db_path}" "{dump_path}"'
        else:
            print('Error: The database engine is not handled.', file=sys.stderr)
            sys.exit(1)
    if dump_cmd:
        DUMPS_DIR.mkdir(parents=True, exist_ok=True)
        os.chmod(DUMPS_DIR, 0o700)
        rc = _exec(dump_cmd)
        if rc != 0:
            sys.exit(rc)
        # Remove old dumps
        print('Searching for old database dump to remove...')
        dumps = list()
        for path in DUMPS_DIR.iterdir():
            if path.name.endswith('.sql') or path.name.endswith('.db'):
                dumps.append((path.stat().st_mtime, path))
        if dumps:
            dumps.sort()
            while len(dumps) >= MAX_DUMPS:
                path = dumps.pop(0)[1]
                print('Removing old database dump "%s".' % path)
                path.unlink()
    else:
        print('No database configured, dump command ignored.')


def shell():
    print('---- Starting shell ----')
    os.execl('/usr/bin/python3', 'python3', str(PYTHON_DIR / 'simple_order/manage.py'), 'shell')


def createsuperuser():
    print('---- Starting createsuperuser ----')
    os.execl('/usr/bin/python3', 'python3', str(PYTHON_DIR / 'simple_order/manage.py'), 'createsuperuser')


def update():
    print('---- Updating server ----')
    cmds = [
        ('find', '.', '-name', '*.pyc', '-type', 'f', '-delete'),
        ('find', '.', '-name', '__pycache__', '-type', 'd', '-delete'),
        ('git', 'fetch', '--recurse-submodules', '--all'),
        ('git', 'reset', '--hard', 'origin/main'),
        ('git', 'pull', '--recurse-submodules'),
        ('python3', str(PYTHON_DIR / 'simple_order/manage.py'), 'migrate', '--no-input'),
    ]
    for cmd in cmds:
        rc = _exec(*cmd)
        if rc != 0:
            sys.exit(rc)


def stop():
    print('---- Stopping server ----')
    rc = _exec('pkill', '-U', USER, '-9', '-f', '--', 'uwsgi --ini %s' % USWGI_INI)
    print('pkill return code: %s' % rc)


def start():
    print('---- Starting server ----')
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    if not (STATIC_DIR / 'admin').exists():
        print('Creating admin static link')
        import django
        _exec('ln', '-sfn', str(Path(django.__path__[0]) / 'contrib/admin/static/admin'), str(STATIC_DIR / 'admin'))
    if not (STATIC_DIR / 'simple_order').exists():
        print('Creating simple_order static link')
        _exec('ln', '-sfn', str(PYTHON_DIR / 'simple_order/static/simple_order'), str(STATIC_DIR / 'simple_order'))
    if 'UWSGI_ORIGINAL_PROC_NAME' in os.environ:
        del os.environ['UWSGI_ORIGINAL_PROC_NAME']
    if 'UWSGI_RELOADS' in os.environ:
        del os.environ['UWSGI_RELOADS']
    os.execl('/usr/bin/uwsgi', 'uwsgi', '--ini', '%s' % USWGI_INI)


if __name__ == '__main__':
    run()
