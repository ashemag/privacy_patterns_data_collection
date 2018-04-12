import urllib2 
from bs4 import BeautifulSoup

class Crawler:
	key1 = 'How the OPC Enforces PIPEDA'



	def _extract_case_urls(self, url, verbose):
		html_doc = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html_doc, 'html.parser')
		links = []
		links_text = []
		start_index, end_index = 0, 0
		for i, link in enumerate(soup.find_all('a')):
			if link.string != None and self.key1 in link.string:
				start_index = i + 1 
			if i == start_index + 10: 
				end_index = i 
			links.append(link.get('href'))
			links_text.append(link.string)
		
		if verbose: 
			print(links[start_index:end_index])
			print(links_text[start_index:end_index]) sanity check 
		return links 

	def crawl(self, verbose=True): 
		start_url="https://www.priv.gc.ca/en/opc-actions-and-decisions/investigations/investigations-into-businesses/"
		privacy_principle = "4.1"
		start_url += "?p[0]=" + privacy_principle 
		page_number="1"
		start_url += "&Page=" + page_number #if page is repetitive, stop 
		links = self._extract_case_urls(start_url, verbose)

#for testing 
if __name__ == "__main__":
	pass 
