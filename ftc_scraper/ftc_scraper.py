#!/usr/bin/python
from __future__ import print_function
import os 
import json
import boto3 
import base64
import datetime 

from crawl.crawl_loader import Crawler
from google_sheets.google_sheets_loader import GoogleSheets
from _email.email_loader import Emailer

# Decrypt code should run once as variables stored outside of the function
# handler so that these are decrypted once per container
# ENCRYPTED_SPREADSHEED_ID = os.environ['SpreadsheetId']
# DECRYPTED_SPREADSHEED_ID= boto3.client('kms').decrypt(CiphertextBlob=base64.b64decode(ENCRYPTED_SPREADSHEED_ID))['Plaintext']
# os.environ['SpreadsheetId'] = DECRYPTED_SPREADSHEED_ID

def lambda_handler(json_input, context): #deployed by aws 
	data = Crawler().crawl() 
	data = dict_to_list(data) 

	today = datetime.date.today()
	week_ago = today - datetime.timedelta(days=7)
	msg = 'FTC Privacy Case results for %s to %s: ' % (week_ago.strftime("%B %d, %Y"), today.strftime("%B %d, %Y")) 
	
	if len(data) > 0: 
		updated_cell_number = GoogleSheets().write(values_to_write=data)
		update = "\n\n%d privacy related FTC cases found.\n"
	else: 
		update = "\n\nNo privacy related FTC cases found.\n"
	update += "Please see the following link for more details: https://docs.google.com/spreadsheets/d/1HnjM8yz9WIKdO16dOOt4GlgSnfhd4PrRvOVGxYP5GmQ/edit?usp=sharing"
	Emailer().send_email(content=msg + update)
	return build_json_doc("Success")

def build_json_doc(value): 
	doc = {"Result": value}
	return json.dumps(doc)

def dict_to_list(data): 
	_list = []
	for key in data: 
		entry = [key] + data[key]
		_list.append(entry)
	return _list 

#for testing 
if __name__ == "__main__":
	lambda_handler()
	exit() 
	data = Crawler().crawl() 
	data = dict_to_list(data) 

	today = datetime.date.today()
	week_ago = today - datetime.timedelta(days=7)
	msg = 'FTC Privacy Case results for %s to %s: ' % (week_ago.strftime("%B %d, %Y"), today.strftime("%B %d, %Y")) 
	
	if len(data) > 0: 
		updated_cell_number = GoogleSheets().write(values_to_write=data)
		update = "\n\n%d privacy related FTC cases found.\n"
	else: 
		update = "\n\nNo privacy related FTC cases found.\n"
	update += "Please see the following link for more details: https://docs.google.com/spreadsheets/d/1HnjM8yz9WIKdO16dOOt4GlgSnfhd4PrRvOVGxYP5GmQ/edit?usp=sharing"
	Emailer().send_email(content=msg + update)

