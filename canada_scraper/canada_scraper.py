from database.crawl_loader import Crawler 
from database.crawl_detail_loader import DetailCrawler 

'''
Task 1: Search one page 
'''
def lambda_handler(): 
	
	pass
	

def create_database(): 
	# collect all OPC cases by privacy principle
	# generate a spreadsheet with the data, should only be called once 
	# Crawler().crawl()
	DetailCrawler().crawl()
	

#for testing 
if __name__ == "__main__":
	create_database()