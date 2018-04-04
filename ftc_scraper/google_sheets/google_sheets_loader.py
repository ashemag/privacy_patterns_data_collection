from __future__ import print_function
import httplib2
import os 

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Privacy Patterns Project'

class GoogleSheets():
	@staticmethod
	def get_credentials():
		"""Gets valid user credentials from storage.

		If nothing has been stored, or if the stored credentials are invalid,
		the OAuth2 flow is completed to obtain the new credentials.

		Returns:
			Credentials, the obtained credential.
		"""
		try:
			import argparse
			flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
		except ImportError:
			flags = None

		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir,
									   'sheets.googleapis.com-python-quickstart.json')

		store = Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
			flow.user_agent = APPLICATION_NAME
			if flags:
				credentials = tools.run_flow(flow, store, flags)
			else: # Needed only for compatibility with Python 2.6
				credentials = tools.run(flow, store)
			print('Storing credentials to ' + credential_path)
		return credentials

	# Gets range encoding for adding values to sheet
	def get_range_encoding(self, service, spreadsheetId, col_number, row_number):
		col_letter = chr(ord('A') + col_number - 1)
		existing_row_number = self.fetch_existing_row_number(service, spreadsheetId, col_letter) + 1
		range_encoding = 'A' + str(existing_row_number) + ':'
		row_number += existing_row_number
		range_encoding = range_encoding + str(col_letter) + str(row_number) 
		return range_encoding

	# Fetches existing numbe of rows in sheet 
	@staticmethod 
	def fetch_existing_row_number(service, spreadsheetId, col_letter): 
		max_rows = '10000000'
		result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='A1:' + col_letter + max_rows).execute()
		return len(result.get('values', []))

	def write(self, values_to_write=[['ok', 'why'], ['will this work', 'maybe?']]):
		"""
		Writes values to google sheet  
		"""
		credentials = self.get_credentials()
		http = credentials.authorize(httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
						'version=v4')
		service = discovery.build('sheets', 'v4', http=http,
								  discoveryServiceUrl=discoveryUrl)

		spreadsheetId = os.environ['SpreadsheetId']

		range_encoding = self.get_range_encoding(service, spreadsheetId, len(values_to_write[0]), len(values_to_write)) 
		body = {'values': values_to_write}
		result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, valueInputOption='USER_ENTERED', range=range_encoding, body=body).execute()
		updated_cell_number = result.get('updatedCells')
		return updated_cell_number 

#for testing 
if __name__ == "__main__":
	os.environ['SpreadsheetId'] = '1HnjM8yz9WIKdO16dOOt4GlgSnfhd4PrRvOVGxYP5GmQ'

	g = GoogleSheets()
	g.write(values_to_write={'Prime Sites, Inc. (Explore Talent)': ['https://www.ftc.gov/enforcement/cases-proceedings/162-3218/prime-sites-inc-explore-talent', '162 3218', 'February 12, 2018', "consumer protection, advertising and marketing, advertising and marketing basics, privacy and security, children's privacy"], 'Sears Holdings Management Corporation, a corporation, in the Matter of': ['https://www.ftc.gov/enforcement/cases-proceedings/082-3099-c-4264/sears-holdings-management-corporation-corporation', '082 3099', 'February 28, 2018', 'consumer protection, advertising and marketing, online advertising and marketing, privacy and security, consumer privacy'], 'PayPal, Inc., In the Matter of': ['https://www.ftc.gov/enforcement/cases-proceedings/162-3102/paypal-inc-matter', '162 3102', 'March 5, 2018', 'consumer protection, credit and finance, payments and billing, privacy and security, consumer privacy, data security, gramm-leach-bliley act, tech']}
)
