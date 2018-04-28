import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GSpreadSheet(object):
    def __init__(self):
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials \
                .from_json_keyfile_name('../Test Hashtag Bot-85bcf54c6a5e.json', scope)
            self.gc = gspread.authorize(credentials)
        except FileNotFoundError as e:
            print(e.reason)
            print('Not pushed the google spreadsheet json file because of security reason')

    def open(self, file='TestHashtagBot'):
        """
        This method would be used to open a provided spreadsheet,
        If spreadsheet isn't provided in the argument, default spreadsheet would be opened
        :param file:
        :return:
        """
        try:
            worksheet = self.gc.open(file)
            return worksheet
        except gspread.SpreadsheetNotFound as e:
            print(e.reason)

    def read(self, worksheet):
        return worksheet.get_all_records()

    def delete(self, worksheet):
        """
        This method can be used to delete the worksheet,
        since I am not using it so leaving it blank for future implementation
        :param worksheet:
        :return:
        """

    def is_empty(self, data):
        """
        This method checks whether the spreadsheet is empty or not
        :param data:
        :return:
        """
        count = 0
        for value in data:
            if value and value != ['']:
                count += 1
        return count == 0

    def write(self, worksheet=None, file=None, data_to_write=None):
        """
        This method would write data in spreadsheet,
        If spreadsheet is_empty only column headers would be written, else data would be appended to sheet
        :param worksheet:
        :param file:
        :param data_to_write:
        :return:
        """
        if not worksheet:
            try:
                worksheet = self.open(file)
            except gspread.SpreadsheetNotFound as e:
                print(e.reason)

        wks = worksheet.sheet1

        # Try to read data, if no data is present through message
        data = None
        try:
            data = self.read(wks)
        except IndexError:
            print("Spreadsheet is empty")
            # If the data is empty add only headings
            wks.append_row(['Profile Name', 'Followers Count'])

        # If data isn't empty append records
        wks.append_row(data_to_write)
        return wks
