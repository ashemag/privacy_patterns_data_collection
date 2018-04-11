from crawl.crawl_loader import Crawler 

'''
Task 1: Search one page 
'''
def lambda_handler(): 
	Crawler().crawl()

#for testing 
if __name__ == "__main__":
	lambda_handler()