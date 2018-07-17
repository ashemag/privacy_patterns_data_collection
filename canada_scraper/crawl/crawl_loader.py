import urllib2 
from bs4 import BeautifulSoup
import csv 
import collections as ct
from dateutil import parser
import datetime 

class Crawler:
	dispositions_index = [462, 463, 464, 465, 466, 467, 468, 469, 470, 471]
	dispositions = [
		'Declined to investigate', 
		'Discontinued', 
		'Early resolved', 
		'No jurisdiction', 
		'Not well-founded', 
		'Resolved', 
		'Settled', 
		'Well-founded', 
		'Well-founded and conditionally resolved', 
		'Well-founded and resolved', 
	]

	complaint_types = [
		'Access', 
		'Accountability', 
		'Accuracy', 
		'Appropriate Purposes', 
		'Challenging Compliance', 
		'Collection', 
		'Consent', 
		'Correction', 
		'Fee', 
		'Identifying Purposes', 
		'Incident', 
		'Openness', 
		'Retention and Disposal', 
		'Safeguards', 
		'Time Limit', 
		'Use and Disclosure', 
	]

	complaint_types_index = [446, 447, 458, 459, 454, 448, 449, 450, 456, 460, 363, 457, 451, 452, 455, 453]

	topics = [
		'Access to personal information', 
		'Advertising and marketing', 
		'Biometrics', 
		'Cloud computing', 
		'Consent', 
		"Driver's licences", 
		'Health/medical Information', 
		'Identity theft', 
		'Internet and online', 
		'Mobile devices and apps', 
		'OPC Privacy Priorities', 
		'Personal information transferred across borders', 
		'Privacy and kids', 
		'Privacy and society', 
		'Privacy at work', 
		'Privacy breaches', 
		'Privacy policies', 
		'Public safety and law enforcement', 
		'Social Insurance Number (SIN)', 
		'Social Networking', 
		'Spam', 
		'Surveillance and monitoring', 
	]

	topics_index = [25, 28, 29, 30, 33, 35, 39, 40, 41, 62, 354, 36, 64, 53, 63, 51, 617, 54, 56, 57, 58, 59]
	sectors = [
		'Aboriginal Public Administration',
		'Accommodations', 	
		'Computer Electronics Products',
		'Construction',
		'Consumer Goods Rental',
		'Financial Institutions',
		'Health', 
		'Insurance',
		'Marketing',
		'Mobile Applications',
		'Nuclear', 
		'Other', 
		'Professionals', 
		'Sales', 
		'Security',
		'Services', 
 		'Educational Support Services', 
		'Social Networking', 
		'Telecommunications', 
		'Transportation'
	]

	sector_index = [701, 392, 444, 642, 396, 397, 437, 404, 439, 443, 438, 441, 409, 424, 436, 430, 431, 440, 419, 414]
	
	def __init__(self, date_str="April 17, 2018"):
		today = datetime.date.today()
		week_ago = today - datetime.timedelta(days=7)
		self.stop_date = week_ago 
		# stop_date = parser.parse(date_str).date() #testing 
		# self.stop_date = stop_date
		self.export_filename = 'opc_cases_scraped.csv'
		self.privacy_principles = ['4.1', '4.1.2', '4.1.3', '4.1.4', '4.1.4(a)', '4.1.4(b)','4.1.4(c)', '4.1.4(d)', '4.10', '4.10.2', 
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
			
			if link.string == 'First': 
				end_index = i 
				break 

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
		# print(soup.find_all('title'))
		case_title = soup.find_all('title')[0].text
		case_name = case_title.split(':')[1].strip()
		return case_name 

	@staticmethod
	def _extract_last_updated(url, stop_date):
		dates = []
		html_doc = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html_doc, 'html.parser')
		for node in soup.find_all('strong'):
			if node.time is not None: 
				new_date = parser.parse(node.time.text).date() 

				if new_date <= stop_date: 
					return dates 
	
				dates.append(node.time.text)
		return dates
		 
	def _extract_case_data(self, case_urls, case_numbers, case_dates, data, verbose): 
		base = 'https://www.priv.gc.ca/'
		verbose=True
		for i, url in enumerate(case_urls): 
			url = base + url 
			html_doc = urllib2.urlopen(url).read()
			soup = BeautifulSoup(html_doc, 'html.parser')
			if verbose: 
				print("On case " + str(i + 1))
			case_url = url 
			# print(case_url)
			case_name = self._extract_case_name(soup)			
			case_number = case_numbers[i]
			last_updated = case_dates[i]
			arr = case_url.split('/')
			case_key = arr[len(arr) - 2]
			data[case_key] = {
				'case_name': case_name.encode('utf-8'), 
				'case_url': case_url.encode('utf-8'), 
				'case_number': case_number.encode('utf-8'), 
				'last_updated': last_updated.encode('utf-8')
			}
	
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

	def crawl_by_category(self, data, key, filter_data, indices, verbose=False): 
		# print "Exploring: " + key 
		page_urls = []
		start_url="https://www.priv.gc.ca/en/opc-actions-and-decisions/investigations/investigations-into-businesses/"
		
		for i, index in enumerate(indices):
			url = start_url + "?q[0]=" + str(index) + "&Page=1"
			case_numbers = self._extract_case_numbers(url)
			case_urls = self._extract_case_urls(url, verbose)

			# map from case urls to disposition type 
			for case_url in case_urls: 
				arr = case_url.split('/')
				case_key = arr[len(arr) - 2]	
				if case_key in data: 
					data[case_key][key].append(filter_data[i])
	
	def crawl_by_principle(self, data, verbose=False): 
		start_url="https://www.priv.gc.ca/en/opc-actions-and-decisions/investigations/investigations-into-businesses/"

		for principle in self.privacy_principles: 
			# print(principle)
			url = start_url + "?p[0]=" + str(principle) + "&Page=1"
			case_numbers = self._extract_case_numbers(url)
			case_urls = self._extract_case_urls(url, verbose)

			# map from case urls to disposition type 
			for case_url in case_urls: 
				arr = case_url.split('/')
				case_key = arr[len(arr) - 2]		
				if case_key in data:
					data[case_key]['principle'].append(principle)

	def crawl(self, verbose=False):
		page_number = 1
		start_url="https://www.priv.gc.ca/en/opc-actions-and-decisions/investigations/investigations-into-businesses/"
		page_url = start_url + "?Page="
		data = {}
		case_principles = ct.defaultdict(list)

		while True: 
			url = page_url 
			url += str(page_number) 
			print "On page: " + str(page_number)
			page_number += 1

			case_urls = self._extract_case_urls(url, verbose)
			case_numbers = self._extract_case_numbers(url)
			case_dates = self._extract_last_updated(url, self.stop_date)
			
			index = len(case_dates)
			print index
			case_urls = case_urls[:index]
			case_numbers = case_numbers[:index]
			case_dates = case_dates[:index]
			if index == 0: 
				break 

			self._extract_case_data(case_urls, case_numbers, case_dates, data, verbose)

		for key in data:
			data[key]['dispositions'] = []
			data[key]['complaint_types'] = []
			data[key]['topics'] = []
			data[key]['principle'] = []
			data[key]['sectors'] = []
		
		entries = []
		if len(data) > 0: 
			self.crawl_by_principle(data)
			self.crawl_by_category(data, 'dispositions', self.dispositions, self.dispositions_index)
			self.crawl_by_category(data, 'complaint_types', self.complaint_types, self.complaint_types_index)
			self.crawl_by_category(data, 'topics', self.topics, self.topics_index)
			self.crawl_by_category(data, 'sectors', self.sectors, self.sector_index)

			for key in data: 
				entries.append([
					data[key]['case_name'],
					data[key]['case_url'], 
					data[key]['case_number'], 
					data[key]['last_updated'],
					('; ').join(data[key]['dispositions']), 
					('; ').join(data[key]['complaint_types']), 
					('; ').join(data[key]['topics']), 
					('; ').join(data[key]['sectors']), 
					('; ').join(data[key]['principle']), 
				]) 

		return entries 

#for testing 
if __name__ == "__main__":
	pass


