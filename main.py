from GoogleConnector import GoogleSheetConnector




import os
from pathlib import Path


import pandas as pd
import pathlib
import configparser
import shutil
from datetime import datetime
import glob
import argparse
if __name__ == "__main__":
    # Create a GoogleConnector object
    config = configparser.ConfigParser()
    config.read('conf.ini')
   
    conf = config['DEFAULT']
    print (conf['ClientSecretfileName'])    
    title = ''
    path = './CSV'
    google_connector = GoogleSheetConnector(conf,'Bitte mir mitteilen ob du die Freigabe erhalten hast')
    files = []
    extension = 'csv'
    os.chdir(path)
    results = glob.glob('*.{}'.format(extension))
    
    for result in results:
      #  print(result.split('.')[0])
        mypath = os.path.join(path, result)
        
        title = result.split('.')[0]
        df = pd.read_csv (result, keep_default_na=False, na_values=[''])
        google_connector.create_sheet(title, len(df), len(df.columns))
        google_connector.update_data(df, title)



    # Get the list of all the files in the Google Drive
   # files = google_connector.get_files()

    # Print the list of files
   # for file in files:
   #     print(file)