import json
import requests
from time import strftime as timestamp
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os 

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Privacy Patterns Project'

class GoogleSheets():
	#Setup access to Google sheets
	scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
	dir_path = os.path.dirname(os.path.realpath(__file__))
	credentials = ServiceAccountCredentials.from_json_keyfile_name(dir_path + '/creds.json', scopes=scopes)
	
	def write(self, values=[]):
		"""
		Writes values to google sheet  
		"""
		credentials = self.credentials
		gc = gspread.authorize(credentials)
		sheet = gc.open('New FTC Cases, To Add to DB').worksheet("Sheet1")
		for value in values: 
			sheet.append_row(value)
		
		return len(values) 
