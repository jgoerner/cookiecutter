# -*- coding: utf-8 -*-

"""
cookiecutter.utils
------------------

Helper functions used throughout Cookiecutter.
"""

from __future__ import unicode_literals
import contextlib
import errno
import logging
import os
import stat
import shutil

logger = logging.getLogger(__name__)


def force_delete(func, path, exc_info):
    """
    Error handler for `shutil.rmtree()` equivalent to `rm -rf`
    Usage: `shutil.rmtree(path, onerror=force_delete)`
    From stackoverflow.com/questions/1889597
    """

    os.chmod(path, stat.S_IWRITE)
    func(path)


def rmtree(path):
    """
    Removes a directory and all its contents. Like rm -rf on Unix.

    :param path: A directory path.
    """

    shutil.rmtree(path, onerror=force_delete)


def make_sure_path_exists(path):
    """
    Ensures that a directory exists.

    :param path: A directory path.
    """

    logger.debug('Making sure path exists: {}'.format(path))
    try:
        os.makedirs(path)
        logger.debug('Created directory at: {}'.format(path))
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


@contextlib.contextmanager
def work_in(dirname=None):
    """
    Context manager version of os.chdir. When exited, returns to the working
    directory prior to entering.
    """
    curdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)


def make_executable(script_path):
    """
    Makes `script_path` executable

    :param script_path: The file to change
    """
    status = os.stat(script_path)
    os.chmod(script_path, status.st_mode | stat.S_IEXEC)
    
    
def remove_backspaces(input_string):
    """
    Cleans the \x08 (a.k.a. backspaces) from the user input
    
    :param input_string: The string to be cleaned
    """
    final_string = ""
    cnt_ignore = 0
    for c in input_string.replace("\x08", "?")[::-1]:
        if c == "?":
            cnt_ignore += 1
            continue
        if cnt_ignore > 0:
            cnt_ignore -= 1
        else:
            final_string = c + final_string
    return final_string
