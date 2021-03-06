#!/usr/bin/python
from __future__ import print_function
import os 
import json
import base64
import datetime 

from crawl.crawl_loader import Crawler
from google_sheets.google_sheets_loader import GoogleSheets
from _email.email_loader import Emailer

def lambda_handler(json_input, context): #deployed by aws 
	data = Crawler().crawl() 
	data = _dict_to_list(data) 

	today = datetime.date.today()
	week_ago = today - datetime.timedelta(days=7)
	msg = 'FTC Privacy Case results for %s to %s: ' % (week_ago.strftime("%B %d, %Y"), today.strftime("%B %d, %Y")) 
	
	if len(data) > 0: 
		updated_cell_number = GoogleSheets().write(values=data)
		update = "\n\n%d privacy related FTC case(s) found.\n" % (len(data))
	else: 
		update = "\n\nNo privacy related FTC cases found.\n"
	update += "Please see the following link for more details: https://docs.google.com/spreadsheets/d/1HnjM8yz9WIKdO16dOOt4GlgSnfhd4PrRvOVGxYP5GmQ/edit?usp=sharing"

	Emailer().send_email('ashe.magalhaes@gmail.com', content=msg + update)
	Emailer().send_email('tkosa@stanford.edu', content=msg + update)
	Emailer().send_email('yishg@stanford.edu', content=msg + update)
	return _build_json_doc("Success")

def _build_json_doc(value): 
	doc = {"Result": value}
	return json.dumps(doc)

# helper function for transforming data from crawler 
def _dict_to_list(data): 
	_list = []
	for key in data: 
		entry = [key] + data[key]
		_list.append(entry)
	return _list 

#for testing 
if __name__ == "__main__":
	lambda_handler('input', 'context')
	exit() 
