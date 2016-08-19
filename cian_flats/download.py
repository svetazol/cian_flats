# Python 2.7
import sys
import logging
import os
import pickle
import thread
import time

from cian_flats.settings import DOWNLOADED_HTML_FILE, DOWNLOADED_JSON_FILE, DOWNLOADED_HTML_HOME, DOWNLOADED_JSON_HOME, \
    NUMBER_OF_THREADS, FILE_WITH_ERRORS_ID
from cian_flats.util import timer, clear_dir
from cian_flats.web import get_flat_html, get_flat_json

logger = logging.getLogger(__name__)


class BaseDownLoad:
    """
    Download html and json web pages to files. Need both because not all needed info can be find from json(
    """

    def __init__(self, file_path_template, get_info_func):
        # """
        # all will be got from child class
        # """
        self.file_path_template = file_path_template
        self.get_info_func = get_info_func
        return

    def get_flat_info_from_local(self, flat_id):
        result_file = self.file_path_template.format(flat_id=flat_id)
        return self.pickle_load_from_file(result_file)

    def download_flat_info_from_web(self, flat_id):
        info = self.get_info_func(flat_id)
        if info:
            result_file = self.file_path_template.format(flat_id=flat_id)
            self.pickle_dump_to_file(result_file, info)
        else:
            logger.error('SOS no info about flat id = {id}'.format(id=flat_id))
            add_to_error_file(flat_id)

    def pickle_dump_to_file(self, filename, info):
        with open(filename, 'wb') as f:
            pickle.dump(info, f)

    def pickle_load_from_file(self, filename):
        with open(filename, 'rb') as f:
            info = pickle.load(f)
        return info


def add_to_error_file(text):
    with open(FILE_WITH_ERRORS_ID, 'a') as f:
        f.write(str(text) + '\n')


def read_from_file(filename):
    with open(filename, 'r') as f:
        f.read()


# class HtmlDownLoad(BaseDownLoad):
#     def __init__(self):
#         self.file_path_template = DOWNLOADED_HTML_FILE
#         self.get_info_func = get_flat_html
#
#     def save_to_file(self, filename, text):
#         with io.open(filename, 'w', encoding='utf8') as f:
#             f.write(text)
#
#
# class JsonDownLoad(BaseDownLoad):
#     def __init__(self):
#         self.file_path_template = DOWNLOADED_JSON_FILE
#         self.get_info_func = get_flat_json
#
#     def save_to_file(self, filename, json_):
#         with io.open(filename, 'w', encoding='utf8') as f:
#             f.write(unicode(json.dumps(json_, ensure_ascii=False)))


html_download = BaseDownLoad(DOWNLOADED_HTML_FILE, get_flat_html)
json_download = BaseDownLoad(DOWNLOADED_JSON_FILE, get_flat_json)


def download_flat_info_from_web(flats_id, i):
    """
    :param flats_id: flat id for which need to download info to files
    :param i: number of thread (to set free)
    """
    logger.debug('Thread {i}, len={len_}'.format(i=i, len_=len(flats_id)))
    for flat_id in flats_id:
        html_download.download_flat_info_from_web(flat_id)
        json_download.download_flat_info_from_web(flat_id)

    exitmutex[i] = True


exitmutex = [False] * NUMBER_OF_THREADS


@timer
def download_from_web_by_ids_to_files(flat_ids):
    """
    :param flat_ids: flats id for which need to download info to files
    """
    logger.info('Total amount of ids = {amount}'.format(amount=len(flat_ids)))
    already_existing_ids = check_files()
    needed_flat_ids = list(set(flat_ids).difference(already_existing_ids))
    logger.info('Only new ids amount={amount}'.format(amount=len(needed_flat_ids)))
    flats_by_tread = [needed_flat_ids[i::NUMBER_OF_THREADS] for i in xrange(NUMBER_OF_THREADS)]
    for i in range(NUMBER_OF_THREADS):
        thread.start_new_thread(download_flat_info_from_web, (flats_by_tread[i], i))

    while False in exitmutex:
        time.sleep(3)


def ids_from_dir(search_dir):
    """
    :param search_dir: folder with files which name = id number (flat id)
    :return: flats ids
    """
    if not (os.path.exists(search_dir)):
        logger.error("No such directory {dir}".format(dir=search_dir))
        sys.exit(2)
    else:
        ids = map(lambda filename: filename[:filename.rfind('.')], os.listdir(search_dir))
        ids.sort()
        return ids


def downloaded_file_data_generator():
    """
    :yield: html and json deserialized data
    """
    json_ids = set(ids_from_dir(DOWNLOADED_HTML_HOME))
    html_ids = set(ids_from_dir(DOWNLOADED_JSON_HOME))
    flat_ids = json_ids.intersection(html_ids)
    if flat_ids:
        for flat_id in flat_ids:
            html = html_download.get_flat_info_from_local(flat_id)
            json_ = json_download.get_flat_info_from_local(flat_id)
            yield (json_, html)


def check_files():
    """
    :return: intersection of flat ids from two dirs (html/json)
    """
    json_ids = set(ids_from_dir(DOWNLOADED_HTML_HOME))
    html_ids = set(ids_from_dir(DOWNLOADED_JSON_HOME))
    json_and_html_ids = json_ids.intersection(html_ids)
    intersection = len(json_and_html_ids)
    logger.info('Existing intersection: {intersection}  len json={json_ids}  len html={html_ids}'.format(
        intersection=intersection, json_ids=len(json_ids), html_ids=len(html_ids)))
    return set([int(json_and_html_id) for json_and_html_id in json_and_html_ids])


if __name__ == '__main__':
    check_files()
    clear_dir(DOWNLOADED_HTML_HOME)
    clear_dir(DOWNLOADED_JSON_HOME)
