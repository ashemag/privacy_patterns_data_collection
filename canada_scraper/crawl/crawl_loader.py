import urllib2 
from bs4 import BeautifulSoup

class Crawler:
	key1 = 'How the OPC Enforces PIPEDA'

	def extract_case_data(self, url):
		html_doc = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html_doc, 'html.parser')
		links = []
		links.text = []
		start_index, end_index = 0, 0
		for i, link in enumerate(soup.find_all('a')):
			print(link.string)
			if link.string != None and self.key1 in link.string:
				start_index = i 
			if i == start_index + 10: 
				end_index = i 
			links.append(link.get('href'))

		print(links[start_index:end_index])

			# link = link.get('href')
			# if 'opc-actions-and-decisions/investigations/investigations-into-businesses' in str(link): 
			# 	print(link)
			# 	links.add(link)

	def crawl(self): 
		start_url="https://www.priv.gc.ca/en/opc-actions-and-decisions/investigations/investigations-into-businesses/"
		privacy_principle = "4.1"
		start_url += "?p[0]=" + privacy_principle 
		page_number="1"
		start_url += "&Page=" + page_number #if page is repetitive, stop 
		print(start_url)
		self.extract_case_data(start_url)

#for testing 
if __name__ == "__main__":
	pass 
