import glob
import os
from unittest import TestCase

import mock as mock
import shutil

from xlrd import open_workbook


class TestRunCians(TestCase):
    test_results_dir = os.path.join(os.path.dirname(__file__), 'results')
    flats_ids = [2057797, 23117310]
    json_dir = os.path.join(test_results_dir, 'json/')
    html_dir = os.path.join(test_results_dir, 'html/')

    @classmethod
    def setUpClass(cls):
        if os.path.exists(cls.test_results_dir):
            shutil.rmtree(cls.test_results_dir)

    @mock.patch('cian_flats.settings.DOWNLOADED_HOME', test_results_dir)
    @mock.patch('cian_flats.settings.DOWNLOADED_JSON_HOME', json_dir)
    @mock.patch('cian_flats.settings.DOWNLOADED_JSON_FILE', os.path.join(json_dir, '{flat_id}.json'))
    @mock.patch('cian_flats.settings.DOWNLOADED_HTML_HOME', html_dir)
    @mock.patch('cian_flats.settings.DOWNLOADED_HTML_FILE', os.path.join(html_dir, '{flat_id}.html'))
    @mock.patch('cian_flats.settings.FILE_WITH_ERRORS_ID', os.path.join(test_results_dir, 'error.txt'))
    @mock.patch('cian_flats.settings.DISTRICT_N_START', 112)
    @mock.patch('cian_flats.settings.DISTRICT_N_FINISH', 112)
    @mock.patch('cian_flats.web.get_needed_flat_ids', return_value=flats_ids)
    def test_download_from_web_to_files(self, get_needed_flat_ids_mock):
        from cian_flats.run import download_from_web_to_files
        download_from_web_to_files()
        json_ids = [int(os.path.basename(x).split('.')[0]) for x in glob.glob(self.json_dir + '*.json')]
        html_ids = [int(os.path.basename(x).split('.')[0]) for x in glob.glob(self.html_dir + '*.html')]
        json_ids.sort()
        html_ids.sort()
        self.assertListEqual(self.flats_ids, json_ids)
        self.assertListEqual(self.flats_ids, html_ids)

    @mock.patch('cian_flats.settings.RESULT_EXCEL_HOME', test_results_dir)
    def test_parse_and_save_to_excel(self):
        from cian_flats.run import parse_and_save_to_excel
        parse_and_save_to_excel()
        xlsx_files = [x for x in glob.glob(self.test_results_dir + '/*.xls')]
        self.assertEqual(len(xlsx_files), 1)
        xlsx_file = xlsx_files[0]
        wb = open_workbook(xlsx_file)
        sheet1 = wb.sheet_by_index(0)
        sheet2 = wb.sheet_by_index(1)
        # minus two head rows
        row_count = sheet1.nrows + sheet2.nrows - 2
        self.assertEqual(row_count, len(self.flats_ids))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_results_dir)
