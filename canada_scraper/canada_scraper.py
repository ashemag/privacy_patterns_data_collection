from crawl.crawl_loader import Crawler 

def lambda_handler(): 
	start_url="https://www.priv.gc.ca/en/opc-actions-and-decisions/investigations/investigations-into-businesses/"
	privacy_principle = "4.1"
	start_url += "?p[0]=" + privacy_principle 
	start_url += "Page=" + page_number #if page is repetitive, stop 
	Crawler().crawl()

#for testing 
if __name__ == "__main__":
	lambda_handler()