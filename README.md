# FTC Scraper
1. Crawls FTC site for privacy-related case data 
2. Updates google spreadsheet with new cases that are not yet included in our Privacy Patterns Project database 
3. Sends an email notification to notify human experts that case catalog was updated and needs to be transferred 

## Prerequisites 

### Makefile 
Install awescli or command line AWS: 
	brew install awscli 

### Google Sheets class 
Install google sheets client: 
	pip install --upgrade google-api-python-client
	Instructions: https://developers.google.com/sheets/api/quickstart/python

Note: To run you will need access to the config file with sensitive information. Email ashe@cs.stanford.edu for this.
