from __future__ import print_function
import httplib2

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

	def get_range_encoding()
	
	def write(self, values_to_write=[['ok', 'why']], col_number = 2):
		"""
		Writes values to google sheet  
		"""
		credentials = self.get_credentials()
		http = credentials.authorize(httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
						'version=v4')
		service = discovery.build('sheets', 'v4', http=http,
								  discoveryServiceUrl=discoveryUrl)

		spreadsheetId = os.environ['spreadsheet_id']

		range_encoded = self.get_range_encoding(col_number) 
		
		body = {'values': values_to_write}
		# result = service.spreadsheets().values().get(
		# 	spreadsheetId=spreadsheetId, range='A1:B2').execute()
		# values = result.get('values', [])
		# print(values)
		result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, valueInputOption='USER_ENTERED', range="A3:B3", body=body).execute()
		print('{0} cells updated.'.format(result.get('updatedCells')));

#for testing 
if __name__ == "__main__":
	g = GoogleSheets()
	g.write()
