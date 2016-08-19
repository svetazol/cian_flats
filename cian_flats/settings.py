import os

SALE_FLAT_URL_AJAX = 'http://www.cian.ru/ajax/mobile/sale/flat/'
SALE_FLAT_URL_HTML = 'http://www.cian.ru/sale/flat/'
FILTER_URL = 'http://www.cian.ru/ajax/mobile/offers_list/?deal_type=sale&district{district}&engine_version=2&offer_type=flat&region=1&room{room}=1'

DISTRICT_N_START = 112
DISTRICT_N_FINISH = 113

ROOMS = ['1']

GROUP_NUMBER = '00'

NUMBER_OF_THREADS = 20

# paths to solve results
DOWNLOADED_HOME = os.path.join(os.path.dirname(__file__), '../results')
DOWNLOADED_JSON_HOME = os.path.join(DOWNLOADED_HOME, 'json/')
DOWNLOADED_JSON_FILE = os.path.join(DOWNLOADED_JSON_HOME, '{flat_id}.json')
DOWNLOADED_HTML_HOME = os.path.join(DOWNLOADED_HOME, 'html/')
DOWNLOADED_HTML_FILE = os.path.join(DOWNLOADED_HTML_HOME, '{flat_id}.html')
FILE_WITH_ERRORS_ID = os.path.join(DOWNLOADED_HOME, 'errors.txt')

RESULT_EXCEL_HOME = DOWNLOADED_HOME

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(funcName)-30s %(levelname)-8s %(message)s')
