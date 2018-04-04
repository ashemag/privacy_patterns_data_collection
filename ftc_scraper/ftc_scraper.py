#!/usr/bin/python
from __future__ import print_function
import os 
import json
import boto3 
import base64

from crawl.crawl_loader import Crawler
from google_sheets.google_sheets_loader import GoogleSheets

''' 
Dates should never be more than a week old when this is triggered weekly. 
First run will have different implementation 
'''
# def fetch_stop_date(week_ago): 
# 	#first run implementation 

# 	#triggered implementation 
# 	test_str = 'March 23, 2018'
# 	today = datetime.date.today()
# 	week_ago = today - datetime.timedelta(days=7)
# 	date = parser.parse(test_str).date() 

# def is_stop_date(date, stop_date): 
# 	if date <= stop_date: 
# 		return True 
# 	return False

'''
Iter1: 
-Crawl through case dates
-Add to google spreadsheet 
-Email point people that sheet has been added to 
-People manually add what is in our sheet to the database 
'''

# Decrypt code should run once as variables stored outside of the function
# handler so that these are decrypted once per container
# ENCRYPTED = os.environ['Example']
# DECRYPTED = boto3.client('kms').decrypt(CiphertextBlob=base64.b64decode(ENCRYPTED))['Plaintext']
# TEST = False 
def lambda_handler(event, context): #deployed by aws 
	# data = crawler.crawl() 
	# if len(data) > 0: 
	# 	#send emails 
	# 	#add to google sheet 
	# 	return build_json_doc("%d cases added " % (len(data)))
	# if TEST: 

	print(ENCRYPTED)
	print(DECRYPTED)
	return build_json_doc(DECRYPTED)

def build_json_doc(value): 
	doc = {"result": value}
	return json.dumps(doc)

#for testing 
if __name__ == "__main__":

	# TEST = True 
	data = Crawler().crawl() 
	


	# lambda_handler('event', 'context')
