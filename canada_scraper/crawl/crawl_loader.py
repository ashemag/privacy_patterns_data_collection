import urllib2 
from bs4 import BeautifulSoup
import csv 
import collections as ct

class Crawler:
	export_filename = 'opc_cases_scraped.csv'
	privacy_principles = ['4.1', '4.1.2', '4.1.3', '4.1.4', '4.1.4(a)', '4.1.4(b)','4.1.4(c)', '4.1.4(d)', '4.10', '4.10.2', 
		'4.10.3', '4.10.4', '4.2', '4.2.3',  '4.2.4',  '4.2.5',  '4.3',  '4.3.1',  '4.3.2',  '4.3.3', '4.3.4',  '4.3.5', 
		'4.3.6', '4.3.7', '4.3.7(d)', '4.3.8', '4.4', '4.4.1', '4.4.2', '4.5', '4.5.2', '4.5.3', '4.6', '4.6.1', '4.6.3', 
		'4.7', '4.7.1', '4.7.2', '4.7.3', '4.7.3(b)', '4.7.3(c)', '4.7.4', '4.7.5', '4.8', '4.8.1', '4.8.2', '4.8.2(d)', 
		'4.9', '4.9.1', '4.9.2', '4.9.3', '4.9.4', '4.9.5', '4.9.6', '5', '5.3', '8.3', '8.4', '8.5', '8.8']

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
	def _extract_last_updated(soup): 
		return soup.find_all('strong')[1].text

	@staticmethod
	def _extract_accountability(soup): 
		for header in soup.find_all('h4'):
			if header.text == 'Accountability':
				nextNode = header
				while True:  
					nextNode = nextNode.nextSibling 
					if nextNode is None: 
						break  
					if nextNode.name is not None:
						if nextNode.name == 'p': 
							return nextNode.text   
		return ''
		 
	def _extract_case_data(self, case_urls, case_numbers, data, case_principles, principle, verbose): 
		base = 'https://www.priv.gc.ca/'
		for i, url in enumerate(case_urls): 
			url = base + url 
			html_doc = urllib2.urlopen(url).read()
			soup = BeautifulSoup(html_doc, 'html.parser')
			if verbose: 
				print("On case " + str(i + 1))
			case_url = url 
			case_name = self._extract_case_name(soup)			
			case_number = case_numbers[i]
			case_principles[case_number].append(principle)
	
			last_updated = self._extract_last_updated(soup)
			enforcement_authority = 'OPC'
			location = 'Canada'
			
			data[case_number] = [case_name.encode('utf-8'), case_url.encode('utf-8'), case_number.encode('utf-8'), last_updated.encode('utf-8'), enforcement_authority, location]
	
	def _write(self, data): 
		with open(self.export_filename, 'w') as csvfile: 
			writer = csv.writer(csvfile)
			fieldnames = ['Case Name', 'Case URL', 'Case Number', 'Last Updated', 'Enforcement Authority', 'Location']
			writer.writerow(fieldnames)
			for key in data: 
				writer.writerow(data[key])
	
	@staticmethod
	def _extract_case_numbers(url): 
		case_numbers = []
		html_doc = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html_doc, 'html.parser')
		for node in soup.find_all('strong'): 
			if '#' in node.text: 
				case_number = node.text.split('#')[1].strip()
				case_numbers.append('#' + case_number)
		
		return case_numbers 

	@staticmethod
	def _get_case_total(url):
		html_doc = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html_doc, 'html.parser')
		for node in soup.find_all('p'): 
			if 'showing' in node.text.lower(): 
				arr = node.text.split('.')[0].split(' ')
				total = int(arr[len(arr) - 1])
				return total 
		print("SHOULD NOT BE REACHED")

	def _crawl_by_principle(self, data, case_principles, principle, verbose=False): 
		page_number = 1
		page_limit_reached = False 
		start_url="https://www.priv.gc.ca/en/opc-actions-and-decisions/investigations/investigations-into-businesses/"
		case_total = self._get_case_total(start_url + "?p[0]=" + principle + "&Page=" + str(page_number))
		case_count = 0 

		while True: 
			if verbose: 
				print("Page " + str(page_number))
			url = start_url + "?p[0]=" + principle 
			url += "&Page=" + str(page_number) #if page is repetitive, stop 
			
			page_number += 1
			case_urls = self._extract_case_urls(url, verbose)
			case_numbers = self._extract_case_numbers(url)
			self._extract_case_data(case_urls, case_numbers, data, case_principles, principle, verbose)
			case_count += len(case_numbers)
			print("Data length: " + str(len(data)))

			if case_count >= case_total:
				print("BREAKING") 
				break 
			

	@staticmethod
	def _process_dict(data, dictionary): 
		for key in dictionary: 
			entry = data[key]
			col = set(dictionary[key]) #remove duplicates
			entry.append(('; ').join(list(col)).strip())
			data[key] = entry

	def crawl(self, verbose=True):
		principles = ['4.1']
		data = {}
		case_principles = ct.defaultdict(list)
		total_no = len(self.privacy_principles)
		for i, principle in enumerate(self.privacy_principles): 
			if verbose: 
				print("Principle: " + str(i + 1) + " of " + str(total_no))
			self._crawl_by_principle(data, case_principles, principle) 
		
		self._process_dict(data, case_principles)
		self._write(data)

		#turn case principles into sets 


#for testing 
if __name__ == "__main__":
	pass 
