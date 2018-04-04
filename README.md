# FTC Scraper
1. Crawls FTC site for privacy-related case data 
2. Updates google spreadsheet with new cases that are not yet included in our Privacy Patterns Project database 
3. Sends an email notification to notify human experts that case catalog was updated and needs to be transferred 

## Prerequisites 

### Makefile 
Install awscli or command line AWS: 
	pip install awscli 

Create virtual environment `venv_temp'

### Google Sheets class 
Install google sheets client: 
	pip install --upgrade google-api-python-client
	Instructions: https://developers.google.com/sheets/api/quickstart/python
