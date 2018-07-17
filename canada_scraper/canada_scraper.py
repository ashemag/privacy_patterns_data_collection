from crawl.crawl_loader import Crawler
from google_sheets.google_sheets_loader import GoogleSheets
from _email.email_loader import Emailer

import time 
import datetime 
import json 

def lambda_handler(json_input, context): #deployed by aws 
	data = Crawler().crawl() 
	today = datetime.date.today()
	week_ago = today - datetime.timedelta(days=7)
	msg = 'OPC case results for %s to %s: ' % (week_ago.strftime("%B %d, %Y"), today.strftime("%B %d, %Y")) 
	
	if len(data) > 0: 
		updated_cell_number = GoogleSheets().write(values=data)
		update = "\n\n%d privacy related OPC case(s) found.\n" % (len(data))
	else: 
		update = "\n\nNo privacy related OPC cases found.\n"
	
	update += "Please see the following link for more details: https://docs.google.com/spreadsheets/d/1HnjM8yz9WIKdO16dOOt4GlgSnfhd4PrRvOVGxYP5GmQ/edit?usp=sharing"
	Emailer().send_email('ashe.magalhaes@gmail.com', content=msg + update)
	Emailer().send_email('tkosa@stanford.edu', content=msg + update)
	Emailer().send_email('yishg@stanford.edu', content=msg + update)
	return _build_json_doc("Success")

def _build_json_doc(value): 
	doc = {"Result": value}
	return json.dumps(doc)

#for testing 
if __name__ == "__main__":
	lambda_handler('input', 'context')