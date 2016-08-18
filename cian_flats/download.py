# Python 2.7
import io
import os
import logging
import json
import pickle
import thread
import time
from cian_flats.web import get_flat_html, get_flat_json, flats_id_chank, flat_get_all_id
from cian_flats.settings import DOWNLOADED_HTML_FILE, DOWNLOADED_JSON_FILE, DOWNLOADED_HTML_HOME, DOWNLOADED_JSON_HOME, \
    NUMBER_OF_THREADS, FILE_WITH_ERRORS_ID
from cian_flats.util import timer

logger = logging.getLogger(__name__)


class BaseDownLoad:
    def __init__(self):
        """
        all will be got from child class
        """
        self.file_path_template = None
        self.get_info = None
        self.extension = None
        self.save_to_file = None
        return

    def get_flat_info_from_local(self, flat_id):
        result_file = self.file_path_template.format(flat_id=flat_id)
        return self.pickle_load_from_file(result_file)

    def download_flat_info_from_web(self, flat_id):
        info = self.get_info(flat_id)
        if info:
            result_file = self.file_path_template.format(flat_id=flat_id)
            self.pickle_dump_to_file(result_file, info)
        else:
            logger.error('SOS no info about flat id = {id}'.format(id=flat_id))
            add_to_file(flat_id)

    def pickle_dump_to_file(self, filename, info):
        with open(filename, 'wb') as f:
            pickle.dump(info, f)

    def pickle_load_from_file(self, filename):
        with open(filename, 'rb') as f:
            info = pickle.load(f)
        return info


def add_to_file(text):
    with open(FILE_WITH_ERRORS_ID, 'a') as f:
        f.write(str(text) + '\n')


def read_from_file(filename):
    with open(filename, 'r') as f:
        f.read()


class HtmlDownLoad(BaseDownLoad):
    def __init__(self):
        self.file_path_template = DOWNLOADED_HTML_FILE
        self.get_info = get_flat_html

    def save_to_file(self, filename, text):
        with io.open(filename, 'w', encoding='utf8') as f:
            f.write(text)


class JsonDownLoad(BaseDownLoad):
    def __init__(self):
        self.file_path_template = DOWNLOADED_JSON_FILE
        self.get_info = get_flat_json

    def save_to_file(self, filename, json_):
        with io.open(filename, 'w', encoding='utf8') as f:
            f.write(unicode(json.dumps(json_, ensure_ascii=False)))


html_download = HtmlDownLoad()
json_download = JsonDownLoad()


@timer
def run_saving_all_backup():
    flats_id_iter = flats_id_chank()
    for flats_id in flats_id_iter:
        for flat_id in flats_id:
            html_download.download_flat_info_from_web(flat_id)
            json_download.download_flat_info_from_web(flat_id)


def download_flat_info_from_web(flats_id, i):
    logger.debug('Thread {i}, len={len_}'.format(i=i, len_=len(flats_id)))
    for flat_id in flats_id:
        html_download.download_flat_info_from_web(flat_id)
        json_download.download_flat_info_from_web(flat_id)

    exitmutex[i] = True


exitmutex = [False] * NUMBER_OF_THREADS


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


@timer
def run_saving_all():
    create_dir(DOWNLOADED_HTML_HOME)
    create_dir(DOWNLOADED_JSON_HOME)
    full_flat_ids = flat_get_all_id()
    logger.info('Total amount of ids = {amount}'.format(amount=len(full_flat_ids)))
    already_existing_ids = check_files()
    needed_flat_ids = list(set(full_flat_ids).difference(already_existing_ids))
    logger.info('Only new ids amount={amount}'.format(amount=len(needed_flat_ids)))
    flats_by_tread = [needed_flat_ids[i::NUMBER_OF_THREADS] for i in xrange(NUMBER_OF_THREADS)]
    for i in range(NUMBER_OF_THREADS):
        thread.start_new_thread(download_flat_info_from_web, (flats_by_tread[i], i))

    while False in exitmutex:
        time.sleep(3)


def clear_dir(dir_name):
    fileList = os.listdir(dir_name)
    for fileName in fileList:
        os.remove(dir_name + '/' + fileName)


def ids_from_dir(search_dir):
    ids = map(lambda filename: filename[:filename.rfind('.')], os.listdir(search_dir))
    ids.sort()
    return ids


def info_iter():
    flat_ids = ids_from_dir(DOWNLOADED_HTML_HOME)
    if flat_ids:
        for flat_id in flat_ids:
            html = html_download.get_flat_info_from_local(flat_id)
            json_ = json_download.get_flat_info_from_local(flat_id)
            yield (json_, html)


def check_files():
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
