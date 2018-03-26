#!/usr/bin/python

from __future__ import print_function
import json
from config.config_loader import ConfigLoader 
from crawl.crawl_loader import Crawler 

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
def lambda_handler(event, context): #deployed by aws 
	data = crawler.crawl() 
	if len(data) > 0: 
		#send emails 
		#add to google sheet 
		return build_json_doc("%d cases added " % (len(data)))
	return build_json_doc("No cases added.")

def build_json_doc(value): 
	doc = {"result": value}
	return json.dumps(doc)

#for testing 
if __name__ == "__main__":
	lambda_handler('event', 'context')
