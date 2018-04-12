import urllib2 
from bs4 import BeautifulSoup

class Crawler:
	@staticmethod
	def _extract_case_urls(url, verbose):
		html_doc = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html_doc, 'html.parser')
		links = []
		links_text = []
		start_index, end_index = 0, 0
		key = 'How the OPC Enforces PIPEDA'

		for i, link in enumerate(soup.find_all('a')):
			if link.string != None and key in link.string:
				start_index = i + 1 
			
			links.append(link.get('href'))
			links_text.append(link.string)	

			if link.string == 'Previous': 
				end_index = i
				break 
			
			if link.string == '1': 
				end_index = i 
				break 
				
		if verbose: #sanity check 
			print(links[start_index:end_index])
			print(links_text[start_index:end_index])

		return links[start_index:end_index] 

	@staticmethod
	def _extract_case_name(soup): 
		case_title = soup.find_all('title')[0].text
		case_name = case_title.split(':')[1].strip()
		return case_name 
	
	@staticmethod
	def _extract_case_number(soup): 
		case_title = soup.find_all('title')[0].text
		case_number = case_title.split(':')[0]
		return case_number 

	@staticmethod
	def _extract_last_updated(soup): 
		return soup.find_all('strong')[1].text

	@staticmethod
	def _extract_accountability(soup): 
		for header in soup.find_all('h3'):
			if header.text == 'Accountability':
				nextNode = header
				while True:  
					nextNode = nextNode.nextSibling 
					if nextNode.name is not None:
						if nextNode.name == 'p': 
							return nextNode.text   
		return ''
		 
	def _extract_case_data(self, case_urls, data, verbose): 
		base = 'https://www.priv.gc.ca/'
		for i, url in enumerate(case_urls): 
			url = base + url 
			html_doc = urllib2.urlopen(url).read()
			soup = BeautifulSoup(html_doc, 'html.parser')
			if verbose: 
				print("On case " + str(i + 1))
			case_url = url 
			case_name = self._extract_case_name(soup)
			case_number = self._extract_case_number(soup)
			last_updated = self._extract_last_updated(soup)
			accountability = self._extract_accountability(soup)
			enforcement_authority = 'OPC'
			location = 'Canada'
			if case_number in data: 
				return True #for page break 
			data[case_number] = [case_url, case_name, last_updated, accountability, enforcement_authority, location]
		return False 

	def crawl(self, verbose=False): 
		data = {}
		page_number = 1
		page_limit_reached = False 
		start_url="https://www.priv.gc.ca/en/opc-actions-and-decisions/investigations/investigations-into-businesses/"

		while True: 
			if page_limit_reached: 
				break 
			if verbose: 
				print("Page " + str(page_number))
			privacy_principle = "4.1"
			url = start_url + "?p[0]=" + privacy_principle 
			url += "&Page=" + str(page_number) #if page is repetitive, stop 
			print(url)
			page_number += 1
			case_urls = self._extract_case_urls(url, verbose)
			page_limit_reached = self._extract_case_data(case_urls, data, verbose)
			print("Data length: " + str(len(data)))

#for testing 
if __name__ == "__main__":
	pass 
