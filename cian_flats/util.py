import os
import time
import logging

logger = logging.getLogger(__name__)


def timer(f):
    f.full_time = 0

    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        func_name = f.__name__
        result_time = time.time() - t
        f.full_time += result_time
        logger.debug('Time func %s: %f' % (func_name, result_time))
        return res

    return tmp


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def clear_dir(dir_name):
    fileList = os.listdir(dir_name)
    for fileName in fileList:
        os.remove(dir_name + '/' + fileName)
