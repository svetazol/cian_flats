from xlwt import Workbook
from cian_flats.settings import RESULT_EXCEL_HOME


class ExcelWorkbook:
    def __init__(self, workbook_name, sheet_name):
        self.workbook_name = workbook_name
        self.workbook = Workbook()
        self.sheet = self.workbook.add_sheet(sheet_name)
        self.sheet_trash = self.workbook.add_sheet('trash')
        self.columns = ['num',
                        'Group',
                        'N',
                        'Rooms',
                        'Price',
                        'Totsp',
                        'Livesp',
                        'Kitsp',
                        'Dist',
                        'Metrdist',
                        'Walk',
                        'Brick',
                        'Tel',
                        'Bal',
                        'Floor',
                        'New',
                        'Floors',
                        'NFloors',
                        'floor1',
                        'floor2',
                        'area']
        self.next_row = 0
        self.next_row_trash = 0
        self.write_header()

    def write_header(self):
        cell = 0
        for column in self.columns:
            self.sheet.write(self.next_row, cell, column)
            self.sheet_trash.write(self.next_row, cell, column)
            cell += 1

        self.next_row += 1
        self.next_row_trash += 1

    def write_flat(self, flat):
        cell = 0
        value_list = [getattr(flat, column.lower(), None) for column in self.columns]
        if None not in value_list[1:]:
            for value in value_list:
                self.sheet.write(self.next_row, cell, value)
                cell += 1

            self.next_row += 1
        else:
            for value in value_list:
                self.sheet_trash.write(self.next_row_trash, cell, value)
                cell += 1

            self.next_row_trash += 1
        return

    def save_workbook(self):
        self.workbook.save('{dir}/{filename}.xls'.format(filename=self.workbook_name, dir=RESULT_EXCEL_HOME))
