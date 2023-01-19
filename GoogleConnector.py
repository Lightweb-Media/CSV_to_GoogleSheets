from __future__ import print_function
import string
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import configparser
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import argparse
import math


class GoogleSheetConnector:
    def __init__(self, conf, title):
        self.scope = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                    ]
    
        # Authentifizierung Google Sheets gegenüber
        authentifizierung = ServiceAccountCredentials.from_json_keyfile_name(
            conf['ClientSecretfileName'], self.scope)
        self.client = gspread.authorize(authentifizierung)
        self.document  = self.client.create(title)
        self.document.share('projekt.3ele@gmail.com', perm_type='user', role='writer')
      #  self.document.share('info@lightweb-media.de', perm_type='user', role='writer')
        
    def create_sheet(self, title,row, col):
        self.document.add_worksheet(title, row, col)
    
    def remove_keywords_sheet(self):
        worksheets = self.document.worksheets()
        del worksheets[0]
        reqs = [{"deleteSheet": {"sheetId": s.id}} for s in worksheets]
        if len(reqs) > 0:
            self.document.batch_update({"requests": reqs})


    def update_data(self,dataframe, title):
        worksheet = self.document.worksheet(title)
        worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())

    def update_updatetime(self):
        worksheet = self.document.worksheet('Keywords')
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        worksheet.update('B1', dt_string)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    conf = config['DEFAULT']
    GoogleSheetConnector(conf)
