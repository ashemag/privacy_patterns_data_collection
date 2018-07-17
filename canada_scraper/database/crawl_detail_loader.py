import urllib2 
from bs4 import BeautifulSoup
import csv 
import collections as ct

class DetailCrawler:
	dispositions_data = {'006_150131': [], 'pipeda-2017-001': ['Well-founded and resolved'], 'pipeda-2017-002': ['Well-founded and resolved'], '005_140321': [], 'pipeda-2002-089': ['No jurisdiction'], 'pipeda-2002-087': ['Resolved'], '008_150818': [], '050418_01': [], 's2015-001_0909': ['Settled'], 's12_041116': ['Settled'], 's_040615_02': ['Settled'], 'pipeda-2014-014': ['Well-founded and conditionally resolved'], 'pipeda-2003-123': ['No jurisdiction'], '004_140919': [], 's17_051216': ['Settled'], 'er_03_170705': ['Early resolved'], 's19_060203': ['Settled'], 'pipeda-2001-026': ['Resolved'], 'pipeda-2003-195': [], 'pipeda-2003-197': [], 's_040624_02': ['Settled'], 'pipeda-2003-218': ['Not well-founded'], 's24_060721': ['Settled'], 's21_060724': ['Settled'], 's27_060516': ['Settled'], 's_041101': ['Settled'], 'swift_rep_070402': [], '010_160125': [], '013_160218': [], 'pipeda-2002-071': ['Well-founded'], 'er_121031': ['Early resolved'], 's13_050517': ['Settled'], 'pipeda-2003-114': ['Well-founded'], 'pipeda-2002-079': [], 's22_061002': ['Settled'], 'pipeda-2001-004': ['Not well-founded'], 'wn_011002': ['Not well-founded'], 'pipeda-2015-002': ['Discontinued', 'Well-founded'], 'pipeda-2015-001': ['Discontinued', 'Not well-founded', 'Well-founded', 'Well-founded and conditionally resolved', 'Well-founded and resolved'], 'nt_010620': [], 's_040706': ['Settled'], 'er_140224': ['Early resolved'], 's31_090225': ['Settled'], 's15_050624': ['Settled'], 'cf-dc_010420': [], 's_041026_02': ['Settled'], 'pipeda-2002-109': ['No jurisdiction'], 'pipeda-2002-106': ['Well-founded'], 'pipeda-2006-345': ['No jurisdiction'], '009_150710': [], 'pipeda-2001-001': ['Discontinued', 'Well-founded'], 'pipeda-2002-039': ['Not well-founded'], 'pipeda-2001-003': ['No jurisdiction'], 'swift_exec_070402': [], 'pipeda-2001-009': ['Not well-founded'], 's2016-001_0530': ['Settled'], 'pipeda-2003-178': ['Not well-founded'], '389_rep_080529': ['Well-founded'], 'pipeda-2012-004': ['Well-founded', 'Well-founded and resolved'], 'pipeda-2001-014': ['Not well-founded'], 's25_060127': ['Settled'], 'pipeda-2001-018': ['Not well-founded'], 'pipeda-2003-240': ['Not well-founded'], 'pipeda-2004-279': ['Well-founded'], 's14_050729': ['Settled'], '007_150723': [], 's30_071115': ['Settled'], 's20_060306': ['Settled'], 'er_040605': ['Early resolved'], 'pipeda-2003-164': ['No jurisdiction'], 'pipeda-2003-162': ['Resolved', 'Well-founded'], 'pipeda-2016-008': ['Well-founded and resolved'], 's18_060306': ['Settled'], 's_040227_02': ['Settled'], '001_170426': [], 's_041105': ['Settled'], 's_040615': ['Settled'], 's2014-001_0923': ['Settled'], 's16_051121': ['Settled'], 's29_070205': ['Settled'], 's2014-002_1001': ['Settled'], 'pipeda-2002-034': ['Not well-founded'], 'pipeda-2009-009': ['Well-founded'], 's23_060612': ['Settled'], 's26_060328': ['Settled'], '011_160219': [], '012_160224': [], 'pipeda-2013-001': ['Declined to investigate', 'Discontinued', 'Not well-founded', 'Well-founded', 'Well-founded and conditionally resolved', 'Well-founded and resolved'], 'pipeda-2013-002': ['Discontinued', 'Not well-founded', 'Well-founded and resolved'], 'pipeda-2013-003': ['Discontinued', 'Well-founded and resolved'], 's_040624': ['Settled'], 's2010-001_100106': ['Settled'], 's_041115': ['Settled'], 'cf-dc_010917': [], 'pipeda-2002-029': ['Resolved'], '003_061204': [], 's_040623': ['Settled'], 's28_061214': ['Settled'], '041221': [], 'pipeda-2008-388': ['Not well-founded', 'Well-founded and resolved'], 'pipeda-2002-098': ['No jurisdiction'], 'pipeda-2003-131': ['Not well-founded'], 'pipeda-2014-004': ['Discontinued', 'Not well-founded'], 'pipeda-2014-003': ['Discontinued', 'Well-founded and resolved'], 'pipeda-2014-001': ['Declined to investigate', 'Discontinued', 'Well-founded and conditionally resolved']}
	complaint_types_data = {'006_150131': ['Incident'], 'pipeda-2017-001': ['Consent'], 'pipeda-2017-002': ['Consent'], '005_140321': ['Incident'], 'pipeda-2002-089': ['Collection'], 'pipeda-2002-087': ['Access'], '008_150818': ['Incident'], '050418_01': ['Incident'], 's2015-001_0909': [], 's12_041116': ['Use and Disclosure'], 's_040615_02': [], 'pipeda-2014-014': ['Appropriate Purposes'], 'pipeda-2003-123': ['Collection', 'Use and Disclosure'], '004_140919': ['Incident'], 's17_051216': ['Collection'], 'er_03_170705': ['Consent'], 's19_060203': ['Collection'], 'pipeda-2001-026': ['Access'], 'pipeda-2003-195': [], 'pipeda-2003-197': [], 's_040624_02': [], 'pipeda-2003-218': ['Use and Disclosure'], 's24_060721': ['Accountability', 'Retention and Disposal'], 's21_060724': ['Use and Disclosure'], 's27_060516': ['Use and Disclosure'], 's_041101': [], 'swift_rep_070402': [], '010_160125': ['Incident'], '013_160218': ['Incident'], 'pipeda-2002-071': ['Collection', 'Use and Disclosure'], 'er_121031': ['Use and Disclosure'], 's13_050517': ['Collection'], 'pipeda-2003-114': ['Collection'], 'pipeda-2002-079': [], 's22_061002': ['Use and Disclosure'], 'pipeda-2001-004': ['Collection'], 'wn_011002': ['Use and Disclosure'], 'pipeda-2015-002': ['Appropriate Purposes', 'Consent', 'Use and Disclosure', 'Use and Disclosure'], 'pipeda-2015-001': ['Accountability', 'Collection', 'Collection', 'Consent', 'Retention and Disposal', 'Use and Disclosure'], 'nt_010620': [], 's_040706': [], 'er_140224': ['Use and Disclosure'], 's31_090225': [], 's15_050624': ['Use and Disclosure'], 'cf-dc_010420': ['Incident'], 's_041026_02': [], 'pipeda-2002-109': ['Use and Disclosure'], 'pipeda-2002-106': ['Collection'], 'pipeda-2006-345': ['Use and Disclosure'], '009_150710': ['Incident'], 'pipeda-2001-001': ['Collection', 'Collection'], 'pipeda-2002-039': ['Access'], 'pipeda-2001-003': ['Use and Disclosure'], 'swift_exec_070402': [], 'pipeda-2001-009': ['Use and Disclosure'], 's2016-001_0530': ['Access'], 'pipeda-2003-178': ['Use and Disclosure'], '389_rep_080529': ['Collection'], 'pipeda-2012-004': ['Access', 'Use and Disclosure'], 'pipeda-2001-014': ['Use and Disclosure'], 's25_060127': ['Use and Disclosure'], 'pipeda-2001-018': ['Access'], 'pipeda-2003-240': ['Access', 'Use and Disclosure'], 'pipeda-2004-279': ['Consent'], 's14_050729': ['Use and Disclosure'], '007_150723': ['Incident'], 's30_071115': ['Access'], 's20_060306': ['Use and Disclosure'], 'er_040605': ['Use and Disclosure'], 'pipeda-2003-164': ['Use and Disclosure'], 'pipeda-2003-162': ['Collection'], 'pipeda-2016-008': ['Access'], 's18_060306': ['Access'], 's_040227_02': [], '001_170426': ['Incident'], 's_041105': [], 's_040615': [], 's2014-001_0923': [], 's16_051121': ['Collection', 'Use and Disclosure'], 's29_070205': ['Safeguards'], 's2014-002_1001': [], 'pipeda-2002-034': ['Use and Disclosure'], 'pipeda-2009-009': ['Collection'], 's23_060612': ['Use and Disclosure'], 's26_060328': ['Use and Disclosure'], '011_160219': ['Incident'], '012_160224': [], 'pipeda-2013-001': ['Access', 'Consent', 'Retention and Disposal', 'Safeguards', 'Use and Disclosure'], 'pipeda-2013-002': ['Access', 'Collection', 'Identifying Purposes'], 'pipeda-2013-003': ['Access', 'Consent', 'Openness', 'Safeguards', 'Use and Disclosure'], 's_040624': [], 's2010-001_100106': [], 's_041115': [], 'cf-dc_010917': ['Incident'], 'pipeda-2002-029': ['Access'], '003_061204': ['Incident'], 's_040623': [], 's28_061214': ['Collection'], '041221': ['Incident'], 'pipeda-2008-388': ['Access', 'Accountability', 'Consent', 'Openness', 'Retention and Disposal'], 'pipeda-2002-098': ['Collection'], 'pipeda-2003-131': ['Collection'], 'pipeda-2014-004': ['Access', 'Use and Disclosure'], 'pipeda-2014-003': ['Access', 'Safeguards'], 'pipeda-2014-001': ['Appropriate Purposes', 'Use and Disclosure', 'Use and Disclosure']}

	topics_data = {'006_150131': ['Privacy breaches'], 'pipeda-2017-001': [], 'pipeda-2017-002': [], '005_140321': [], 'pipeda-2002-089': ['Consent'], 'pipeda-2002-087': ['Access to personal information', 'Privacy at work'], '008_150818': ['Internet and online', 'Privacy breaches'], '050418_01': [], 's2015-001_0909': ['Privacy at work', 'Surveillance and monitoring'], 's12_041116': [], 's_040615_02': [], 'pipeda-2014-014': [], 'pipeda-2003-123': ['Consent'], '004_140919': ['Privacy breaches'], 's17_051216': [], 'er_03_170705': [], 's19_060203': ['Social Insurance Number (SIN)'], 'pipeda-2001-026': ['Access to personal information'], 'pipeda-2003-195': ['Access to personal information'], 'pipeda-2003-197': [], 's_040624_02': [], 'pipeda-2003-218': ['Consent', 'Privacy at work', 'Privacy breaches'], 's24_060721': [], 's21_060724': [], 's27_060516': [], 's_041101': [], 'swift_rep_070402': [], '010_160125': ['Consent', 'Internet and online', 'Privacy breaches', 'Social Networking'], '013_160218': ['Privacy breaches'], 'pipeda-2002-071': ['Consent', 'Internet and online'], 'er_121031': [], 's13_050517': [], 'pipeda-2003-114': ['Consent', 'Privacy at work', 'Surveillance and monitoring'], 'pipeda-2002-079': [], 's22_061002': [], 'pipeda-2001-004': ['Consent'], 'wn_011002': ['Personal information transferred across borders'], 'pipeda-2015-002': ['Consent', 'Internet and online', 'OPC Privacy Priorities'], 'pipeda-2015-001': ['Advertising and marketing', 'Mobile devices and apps', 'Surveillance and monitoring'], 'nt_010620': [], 's_040706': [], 'er_140224': ['Privacy breaches'], 's31_090225': ['Internet and online', 'Social Networking'], 's15_050624': [], 'cf-dc_010420': [], 's_041026_02': [], 'pipeda-2002-109': ['Consent'], 'pipeda-2002-106': ['Consent', 'Privacy at work'], 'pipeda-2006-345': ['Consent'], '009_150710': ['Privacy breaches'], 'pipeda-2001-001': ['Consent', 'Consent', 'Surveillance and monitoring'], 'pipeda-2002-039': ['Access to personal information'], 'pipeda-2001-003': ['Personal information transferred across borders'], 'swift_exec_070402': [], 'pipeda-2001-009': [], 's2016-001_0530': ['Access to personal information'], 'pipeda-2003-178': [], '389_rep_080529': ['Biometrics', 'Personal information transferred across borders'], 'pipeda-2012-004': ['Privacy breaches'], 'pipeda-2001-014': ['Consent', 'Personal information transferred across borders'], 's25_060127': [], 'pipeda-2001-018': ['Access to personal information'], 'pipeda-2003-240': ['Access to personal information'], 'pipeda-2004-279': ['Privacy at work', 'Surveillance and monitoring'], 's14_050729': [], '007_150723': ['Privacy breaches'], 's30_071115': [], 's20_060306': [], 'er_040605': [], 'pipeda-2003-164': ['Consent'], 'pipeda-2003-162': ['Consent', 'Internet and online'], 'pipeda-2016-008': ['Access to personal information', 'Consent', 'Public safety and law enforcement', 'Surveillance and monitoring'], 's18_060306': [], 's_040227_02': [], '001_170426': ['Privacy breaches'], 's_041105': [], 's_040615': [], 's2014-001_0923': ['Consent', 'Internet and online'], 's16_051121': [], 's29_070205': [], 's2014-002_1001': ['Cloud computing', 'Consent', 'Internet and online'], 'pipeda-2002-034': ['Privacy breaches'], 'pipeda-2009-009': ['Consent', 'Internet and online', 'Personal information transferred across borders'], 's23_060612': [], 's26_060328': [], '011_160219': ['Privacy breaches'], '012_160224': ['Identity theft', 'Privacy breaches'], 'pipeda-2013-001': ['Health/medical Information', 'Mobile devices and apps'], 'pipeda-2013-002': ['Access to personal information'], 'pipeda-2013-003': ['Access to personal information'], 's_040624': [], 's2010-001_100106': [], 's_041115': [], 'cf-dc_010917': [], 'pipeda-2002-029': ['Access to personal information'], '003_061204': [], 's_040623': [], 's28_061214': [], '041221': [], 'pipeda-2008-388': ['Consent'], 'pipeda-2002-098': ["Driver's licences", 'Social Insurance Number (SIN)'], 'pipeda-2003-131': ['Surveillance and monitoring'], 'pipeda-2014-004': ['Privacy breaches'], 'pipeda-2014-003': ['Access to personal information', 'Privacy breaches'], 'pipeda-2014-001': ['Privacy at work']}

	sector_data = {'006_150131': [], 'pipeda-2017-001': ['Services'], 'pipeda-2017-002': ['Services'], '005_140321': [], 'pipeda-2002-089': ['Transportation'], 'pipeda-2002-087': ['Transportation'], '008_150818': [], '050418_01': [], 's2015-001_0909': [], 's12_041116': [], 's_040615_02': [], 'pipeda-2014-014': ['Transportation'], 'pipeda-2003-123': ['Telecommunications'], '004_140919': [], 's17_051216': [], 'er_03_170705': ['Financial Institutions'], 's19_060203': ['Accommodations'], 'pipeda-2001-026': ['Financial Institutions'], 'pipeda-2003-195': [], 'pipeda-2003-197': [], 's_040624_02': [], 'pipeda-2003-218': ['Financial Institutions'], 's24_060721': ['Accommodations'], 's21_060724': ['Transportation'], 's27_060516': ['Professionals'], 's_041101': [], 'swift_rep_070402': [], '010_160125': ['Telecommunications'], '013_160218': ['Financial Institutions'], 'pipeda-2002-071': ['Transportation'], 'er_121031': ['Telecommunications'], 's13_050517': [], 'pipeda-2003-114': ['Transportation'], 'pipeda-2002-079': [], 's22_061002': ['Other'], 'pipeda-2001-004': ['Other'], 'wn_011002': ['Health'], 'pipeda-2015-002': ['Services', 'Services'], 'pipeda-2015-001': ['Sales', 'Telecommunications'], 'nt_010620': [], 's_040706': [], 'er_140224': ['Services'], 's31_090225': [], 's15_050624': [], 'cf-dc_010420': ['Transportation'], 's_041026_02': [], 'pipeda-2002-109': ['Financial Institutions'], 'pipeda-2002-106': ['Transportation'], 'pipeda-2006-345': ['Other'], '009_150710': [], 'pipeda-2001-001': ['Financial Institutions', 'Security'], 'pipeda-2002-039': ['Financial Institutions'], 'pipeda-2001-003': ['Financial Institutions'], 'swift_exec_070402': [], 'pipeda-2001-009': ['Financial Institutions'], 's2016-001_0530': ['Services'], 'pipeda-2003-178': ['Telecommunications'], '389_rep_080529': ['Services', 'Educational Support Services'], 'pipeda-2012-004': ['Telecommunications'], 'pipeda-2001-014': ['Health'], 's25_060127': ['Other'], 'pipeda-2001-018': ['Financial Institutions'], 'pipeda-2003-240': ['Financial Institutions'], 'pipeda-2004-279': ['Other'], 's14_050729': [], '007_150723': [], 's30_071115': ['Professionals'], 's20_060306': ['Accommodations'], 'er_040605': [], 'pipeda-2003-164': ['Other'], 'pipeda-2003-162': ['Transportation'], 'pipeda-2016-008': ['Telecommunications'], 's18_060306': ['Financial Institutions'], 's_040227_02': [], '001_170426': ['Financial Institutions', 'Sales', 'Transportation'], 's_041105': [], 's_040615': [], 's2014-001_0923': [], 's16_051121': [], 's29_070205': ['Sales'], 's2014-002_1001': [], 'pipeda-2002-034': ['Financial Institutions'], 'pipeda-2009-009': ['Sales'], 's23_060612': ['Accommodations'], 's26_060328': ['Sales'], '011_160219': ['Financial Institutions'], '012_160224': ['Financial Institutions'], 'pipeda-2013-001': ['Accommodations', 'Sales', 'Services'], 'pipeda-2013-002': ['Financial Institutions', 'Financial Institutions'], 'pipeda-2013-003': ['Financial Institutions', 'Services'], 's_040624': [], 's2010-001_100106': [], 's_041115': [], 'cf-dc_010917': ['Telecommunications'], 'pipeda-2002-029': ['Financial Institutions'], '003_061204': [], 's_040623': [], 's28_061214': ['Other'], '041221': [], 'pipeda-2008-388': ['Sales'], 'pipeda-2002-098': ['Security'], 'pipeda-2003-131': ['Telecommunications'], 'pipeda-2014-004': ['Sales', 'Telecommunications'], 'pipeda-2014-003': ['Health', 'Insurance', 'Transportation'], 'pipeda-2014-001': ['Financial Institutions', 'Marketing', 'Transportation']}

	db = 'additional_opc_cases.csv'
	export_filename = 'additional_opc_cases_scraped_details.csv'
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
	
	def read_keys(self, dict_arr): 
		data = {}
		with open(self.db) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				url = row['Case URL']
				arr = url.split('/')
				key = arr[len(arr) - 2]				
				if dict_arr: 
					data[key]= []
				else: 
					data[key] = ''
		return data

	@staticmethod
	def _get_case_total(url):
		html_doc = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html_doc, 'html.parser')
		for node in soup.find_all('p'): 
			if 'showing' in node.text.lower(): 
				arr = node.text.split('.')[0].split(' ')
				total = int(arr[len(arr) - 1])
				return total 
		# sanity check: print("SHOULD NOT BE REACHED")
	
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
	def _extract_case_numbers(url): 
		case_numbers = []
		html_doc = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html_doc, 'html.parser')
		for node in soup.find_all('strong'): 
			if '#' in node.text: 
				case_number = node.text.split('#')[1].strip()
				case_numbers.append('#' + case_number)
		
		return case_numbers 

	def crawl_by_category(self, data, filter_data, indices, dict_arr=True, verbose=False): 
		page_urls = []
		start_url="https://www.priv.gc.ca/en/opc-actions-and-decisions/investigations/investigations-into-businesses/"

		for i, index in enumerate(indices):
			page_number = 1
			page_url = start_url + "?q[0]=" + str(index) + "&Page="
			case_total = self._get_case_total(page_url + str(page_number))
			case_count = 0 
			print "On category: " + filter_data[i]
			print "On index: " + str(indices[i])
			while True: 
				url = page_url + str(page_number) #if page is repetitive, stop 
				case_numbers = self._extract_case_numbers(url)
				case_count += len(case_numbers)
				case_urls = self._extract_case_urls(url, verbose)

				# map from case urls to disposition type 
				for case_url in case_urls: 
					arr = case_url.split('/')
					key = arr[len(arr) - 2]	
					if key in data: 
						if dict_arr: 
							data[key].append(filter_data[i])
						else: 
							data[key] = filter_data[i] 
				
				print "On page: " + str(page_number)
				if case_count >= case_total:
					break 

				page_number += 1
		print(data) 

	def _write(self): 
		data = {}
		with open(self.db) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				case_url, case_name, case_number = row['Case URL'], row['Case Name'], row['Case Number']
				last_updated = row['Last Updated']
				arr = case_url.split('/')
				key = arr[len(arr) - 2]	
				complaints = ('; ').join(self.complaint_types_data[key])
				sectors = ('; ').join(self.sector_data[key])
				topics = ('; ').join(self.topics_data[key])
				dispositions =('; ').join(self.dispositions_data[key])
				if topics == '': 
					topics = 'N/A'
				if sectors == '': 
					sectors = 'N/A'
				if complaints == '': 
					complaints = 'N/A'
				if dispositions == '': 
					dispositions = 'N/A'
				data[case_url] = [case_name, case_url, case_number, last_updated, 
					sectors, complaints, topics, dispositions]

		with open(self.export_filename, 'w') as csvfile: 
			writer = csv.writer(csvfile)
			fieldnames = ['Case Name', 'Case URL', 'Case Number', 'Last Updated', 'Sectors', 'Complaint Types', 'Topics', 'Dispositions']
			writer.writerow(fieldnames)
			for key in data: 
				writer.writerow(data[key])

	'''
	Read in URLS from spreadsheet created by crawler 
	Scrape cases by topic, complaint types, disposition, and sectors 
	Map each case to URL from spreadsheet, populate spreadsheet with findings 
	'''
	def crawl(self, verbose=False):
		data = self.read_keys(True) 
		# dispositions_data = self.crawl_by_category(data, self.dispositions, self.dispositions_index) 
		# print(dispositions_data)
		# self.crawl_by_category(data, self.complaint_types, self.complaint_types_index) 
		# print(len(self.dispositions) + len(self.complaint_types) + len(self.topics) + len(self.sectors))
		# self.crawl_by_category(data, self.topics, self.topics_index) 
		# print data
		# exit() 
		# self.crawl_by_category(data, self.sectors, self.sector_index) 
		# print data
		# exit() 
		self._write()

#for testing 
if __name__ == "__main__":
	DetailCrawler().crawl()
