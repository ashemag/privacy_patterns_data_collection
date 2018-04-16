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
	def _extract_case_urls(url): 
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
	def _extract_tags(soup): 
		divs = soup.find_all('div', class_ = 'field-name-field-tags-view')
		tags = [] 
		for div in divs: 
			for link in div.find_all('a'): 
				tag = link.contents[0].lower().strip()
				tags.append(tag) 
		return tags
	
	#helper method to extract text from html given key 
	@staticmethod
	def _extract_text(soup, key): 
		text = soup.get_text().encode('utf-8')
		if key in text: 
			text = text.split(key)[1].strip().split('\n')[0].strip()
			return text 
		return 'N/A'

	#helper method to detect valid tags 
	def _valid_tags(self, tags):
		for tag in tags: 
			if tag in self.KEY_TAGS: 
				return True 
		return False 

	'''
	Extracts all case data given a set of case urls 
	'''
	def _extract_case_data(self, data, case_urls, verbose): 
		stop_page_reached = False 
		for i, case_url in enumerate(case_urls):
			if verbose: 
				print("On case " + str(i + 1))
			html_doc = urllib2.urlopen(case_url).read()
			soup = BeautifulSoup(html_doc, 'html.parser')
			tags = self._extract_tags(soup)
			update_time = self._extract_text(soup, 'Last Updated:')
			case_number = self._extract_text(soup, 'FTC Matter/File Number:')
			if self._valid_tags(tags): 
				if self._is_stop_time(test_date_str = update_time): 
					stop_page_reached = True  
				else: 
					title = soup.head.title.string
					processed_title = title.split("|")[0].strip()
					data[processed_title.encode('utf-8')] = [case_url, case_number, update_time,', '.join(tags).encode('utf-8')] 	
		return stop_page_reached

	#HELPER: get next page url in sequence 
	@staticmethod 
	def _get_next_url(url, page_count): 
		if "?" not in url: 
			url = "https://www.ftc.gov/enforcement/cases-proceedings?page=1"
		else: 
			url = "https://www.ftc.gov/enforcement/cases-proceedings?page=" + str(page_count) 
		return url 

	#HELPER: evaluate if test date string is before stop date string 
	@staticmethod
	def _is_stop_time(stop_date_str = 'November 29, 2017', test_date_str ="March 23, 2018", LAMBDA = True): 
		if LAMBDA: 
			today = datetime.date.today()
			week_ago = today - datetime.timedelta(days=7)
			stop_date = week_ago 
		else: 
			stop_date = parser.parse(stop_date_str).date() 
		
		test_date = parser.parse(test_date_str).date() 
		return test_date <= stop_date 

	#Driver 
	def crawl(self, verbose=False):
		url = 'https://www.ftc.gov/enforcement/cases-proceedings'
		page_count = 0 
		data = {}
		stop_page_reached = False 

		while (stop_page_reached == False): 
			case_urls = self._extract_case_urls(url)
			# extract cases from each case url 
			stop_page_reached = self._extract_case_data(data, case_urls, verbose)
			page_count += 1
			if verbose: 
				print "Completed page " + str(page_count)
			url = self._get_next_url(url, page_count)

		return data 

#for testing 
if __name__ == "__main__":
	pass





		