import os
import shutil

from src.utils.logging_config import app_log


def remove_file(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
            app_log.info('successfully removed file %s', path)
            return

        if os.path.isdir(path):
            shutil.rmtree(path)
            app_log.info('successfully removed dir %s', path)
            return

        app_log.error('teardown incomplete - error removing %s', path)

    except OSError as e:
        app_log.error('teardown incomplete - error removing %s', path)
        app_log.error('%s', e)

def create_parent_dir(path):
    parent_dir = os.path.dirname(path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
