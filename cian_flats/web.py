import json
import logging
import urllib2
import sys
from cian_flats.util import timer
from settings import SALE_FLAT_URL_AJAX, SALE_FLAT_URL_HTML, DISTRICT_N_FINISH, DISTRICT_N_START, ROOMS, FILTER_URL

logger = logging.getLogger(__name__)


def get_needed_flat_ids(filter_url, min_page_num=1, max_page_num=100):
    """
    :param filter_url:
    :param min_page_num:
    :param max_page_num:
    :return:
    """
    needed_ids = set([])
    failed_attempts = 0
    for i in range(min_page_num, max_page_num + 1):
        filter_url_page = filter_url + '&p=' + str(i)
        try:
            page_info = json.load(urllib2.urlopen(filter_url_page))
            failed_attempts = 0
        except urllib2.URLError:
            if failed_attempts < 3:
                failed_attempts += 1
                i -= 1
                continue
            else:
                logger.critical("Can not load {filter_url_page}".format(filter_url_page=filter_url_page))
                sys.exit(2)

        offers = page_info['offers']
        if not offers:
            break
        needed_ids.update(set([offer['id'] for offer in offers]))
    return needed_ids


def get_flat_html(flat_id):
    html = None
    try:
        html = urllib2.urlopen(SALE_FLAT_URL_HTML + str(flat_id)).read().decode('utf-8')
    except urllib2.URLError:
        logger.error('URLError ' + SALE_FLAT_URL_HTML + str(flat_id))

    return html


def get_flat_json(flat_id):
    json_ = None
    try:
        sale_flat_url = SALE_FLAT_URL_AJAX + str(flat_id)
        json_ = json.load(urllib2.urlopen(sale_flat_url))
    except urllib2.URLError:
        logger.error('URLError ' + SALE_FLAT_URL_AJAX + str(flat_id))

    return json_


def flats_id_chank():
    DISTRICTS = []
    for i in range(0, DISTRICT_N_FINISH - DISTRICT_N_START + 1):
        DISTRICTS.append('[{i}]={n}'.format(i=i, n=i + DISTRICT_N_START))
    for district in DISTRICTS:
        for room in ROOMS:
            needed_flat_ids = get_needed_flat_ids(FILTER_URL.format(district=district, room=room))
            amount = len(needed_flat_ids)
            logger.info(
                '{district} {rooms} amount={amount} min={minim} max={maxim}'.format(district=district, rooms=room,
                                                                                    amount=str(amount),
                                                                                    maxim=max(needed_flat_ids or []),
                                                                                    minim=min(needed_flat_ids or [])))
            yield needed_flat_ids


@timer
def flat_get_all_id():
    full_flat_ids = []
    for flats_id in flats_id_chank():
        if flats_id:
            full_flat_ids += flats_id

    return full_flat_ids
