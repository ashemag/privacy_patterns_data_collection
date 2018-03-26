import urllib2 
from bs4 import BeautifulSoup
import datetime 
from dateutil import parser

class Crawler():
	KEY_TAGS = ['data security', 'consumer privacy', 'privacy', 'security', 'privacy and security', 'privacy shield']

	'''
	Find all cases on the page
	'''
	@staticmethod
	def extract_case_urls(url): 
		html_doc = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html_doc, 'html.parser')

		links = set()
		for link in soup.find_all('a'):
			links.add(link.get('href'))

		key = 'https://www.ftc.gov/enforcement/cases-proceedings'
		processed_links = set()
		for link in links:
			if link == None: 
				continue 
			link = link.encode("utf-8") #convert unicode -> string 
			if key in link: 
				processed_links.add(link)
		return processed_links
	

	#helper method to extract tags 
	@staticmethod
	def extract_tags(soup): 
		divs = soup.find_all('div', class_ = 'field-name-field-tags-view')
		tags = [] 
		for div in divs: 
			for link in div.find_all('a'): 
				tag = link.contents[0].lower().strip()
				tags.append(tag) 
		return tags
	
	#helper method to extract text from html given key 
	@staticmethod
	def extract_text(soup, key): 
		text = soup.get_text().encode('utf-8')
		if key in text: 
			text = text.split(key)[1].strip().split('\n')[0].strip()
			return text 
		return 'N/A'

	#helper method to detect valid tags 
	def valid_tags(self, tags):
		for tag in tags: 
			if tag in self.KEY_TAGS: 
				return True 
		return False 

	'''
	Extracts all case data given a set of case urls 
	'''
	def extract_case_data(self, data, case_urls): 
		for i, case_url in enumerate(case_urls ):
			print("On case " + str(i + 1))
			html_doc = urllib2.urlopen(case_url).read()
			soup = BeautifulSoup(html_doc, 'html.parser')
			tags = self.extract_tags(soup)
			update_time = self.extract_text(soup, 'Last Updated:')
			case_number = self.extract_text(soup, 'FTC Matter/File Number:')
			if self.valid_tags(tags): 
				print("happens")
				title = soup.head.title.string
				processed_title = title.split("|")[0].strip()
				data[processed_title.encode('utf-8')] = [case_url, case_number, update_time,', '.join(tags).encode('utf-8')] 	
	#Driver 
	def crawl(self):
		start_url = 'https://www.ftc.gov/enforcement/cases-proceedings'
		data = {}
		case_urls = self.extract_case_urls(start_url)
		# extract cases from each case url 
		self.extract_case_data(data, case_urls)
		return data 
		