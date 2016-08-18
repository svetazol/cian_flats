import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(funcName)-30s %(levelname)-8s %(message)s')

SALE_FLAT_URL_AJAX = 'http://www.cian.ru/ajax/mobile/sale/flat/'
SALE_FLAT_URL_HTML = 'http://www.cian.ru/sale/flat/'
FILTER_URL = 'http://www.cian.ru/ajax/mobile/offers_list/?deal_type=sale&district{district}&engine_version=2&offer_type=flat&region=1&room{room}=1'

DISTRICT_N_START = 112
DISTRICT_N_FINISH = 114
DISTRICTS = []
for i in range(0, DISTRICT_N_FINISH - DISTRICT_N_START + 1):
    DISTRICTS.append('[{i}]={n}'.format(i=i, n=i + DISTRICT_N_START))

ROOMS = ['1']
GROUP_NUMBER = '00'
DOWNLOADED_HOME = 'D:/PythonPrograms/cian_result/'
DOWNLOADED_JSON_HOME = DOWNLOADED_HOME + 'json/'
DOWNLOADED_JSON_FILE = DOWNLOADED_JSON_HOME + '{flat_id}.json'
DOWNLOADED_HTML_HOME = DOWNLOADED_HOME + 'html/'
DOWNLOADED_HTML_FILE = DOWNLOADED_HTML_HOME + '{flat_id}.html'
RESULT_EXCEL_HOME = DOWNLOADED_HOME
FILE_WITH_ERRORS_ID = DOWNLOADED_HOME + 'errors.txt'
NUMBER_OF_THREADS = 20
