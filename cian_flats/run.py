import logging

from cian_flats import util, download, web
from cian_flats.flat import Flat
from cian_flats.util import timer
from cian_flats.settings import GROUP_NUMBER, RESULT_EXCEL_HOME, DOWNLOADED_HTML_HOME, DOWNLOADED_JSON_HOME, \
    DOWNLOADED_HOME

logger = logging.getLogger(__name__)


def download_from_web_to_files():
    """
    create needed folders and save serialized data to files from web site
    """
    util.create_dir(DOWNLOADED_HOME)
    util.create_dir(DOWNLOADED_HTML_HOME)
    util.create_dir(DOWNLOADED_JSON_HOME)
    flat_ids = web.flat_get_all_id()
    download.download_from_web_by_ids_to_files(flat_ids)
    logger.info("Info from cian.ru downloaded to dir {dir_name}".format(dir_name=DOWNLOADED_HOME))


def parse_and_save_to_excel():
    """
    unpack existing serialized files, parse them, save info to excel
    """
    from cian_flats.excel import ExcelWorkbook

    excel = ExcelWorkbook('data_{group_number}_2016'.format(group_number=GROUP_NUMBER),
                          'group_{group_number}'.format(group_number=GROUP_NUMBER))

    @timer
    def parse_and_write():
        for info in download.downloaded_file_data_generator():
            flat = Flat(*info)
            excel.write_flat(flat)

    parse_and_write()
    excel.save_workbook()
    logger.info("Info from cian.ru saved to file {file_name}".format(file_name=RESULT_EXCEL_HOME))
