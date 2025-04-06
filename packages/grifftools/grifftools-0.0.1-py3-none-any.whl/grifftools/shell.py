import os
import shutil
import subprocess
from os import chdir as cd
from os import listdir as ls
from os.path import basename, dirname, exists
from os.path import expanduser as home
from os.path import isdir, isfile, islink, join
from pathlib import Path
from re import search as grep
from re import sub as sed
from shutil import move as mv
from time import sleep


def sh(cmd, live=False):
    if live:
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            for line in iter(p.stdout.readline, b''):
                print(line.decode('utf-8'), end='')
            p.stdout.close()
            p.wait()
    else:
        return subprocess.run(cmd, shell=True, check=True, capture_output=True).stdout.decode('utf-8')


def rm(*targets, **kwargs):
    for target in targets:
        if os.path.isdir(target):
            os.rmdir(target, **kwargs)
        else:
            os.remove(target, **kwargs)


def cp(src, dst, **kwargs):
    if os.path.isdir(src):
        shutil.copytree(
            src,
            os.path.join(dst, os.path.basename(src)) if os.path.exists(dst) else dst,
            **kwargs,
        )
    else:
        shutil.copy(src, dst, **kwargs)
    return dst


def cat(*srcs):
    for src in srcs:
        with open(src, 'r') as f:
            yield from f.read().splitlines()


def mkdir(*dirs, exist_ok=True, **kwargs):
    for dir_ in dirs:
        os.makedirs(dir_, exist_ok=exist_ok, **kwargs)


def touch(*targets):
    for target in targets:
        open(target, 'a').close()


def filename(src):
    return os.path.splitext(os.path.basename(src))[0]


def extname(src):
    return os.path.splitext(os.path.basename(src))[1]


def find(src='.', name='*', type=None, exec=str):
    if not os.path.isdir(src):
        raise ValueError(f"source {src} is not a valid directory")
    paths = Path(src).rglob(name)
    if type == 'f':
        paths = filter(lambda path: path.is_file(), paths)
    elif type == 'd':
        paths = filter(lambda path: path.is_dir(), paths)
    elif type == 'l':
        paths = filter(lambda path: path.is_symlink(), paths)
    yield from map(exec, paths)
