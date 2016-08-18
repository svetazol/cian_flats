import logging

from download import run_saving_all, info_iter
from flat import Flat

from cian_flats.cian_flats import timer
from settings import GROUP_NUMBER

logger = logging.getLogger(__name__)

run_saving_all()

from cian_flats.cian_flats.excel import ExcelWorkbook

excel = ExcelWorkbook('data_{group_number}_2016'.format(group_number=GROUP_NUMBER),
                      'group_{group_number}'.format(group_number=GROUP_NUMBER))


@timer
def parse_and_write():
    for info in info_iter():
        flat = Flat(*info)
        excel.write_flat(flat)


parse_and_write()

excel.save_workbook()
