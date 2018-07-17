import csv 

'''
Maps CSA principles to GAPP principles in final csv 
'''

filename = './opc_cases_final.csv'
mappings = './mapping_principles.csv'

def read_keys(data):
	entries = [] 
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			principles = row['Principle']
			arr = principles.split(';')
			entry = ''
			temp_arr = []
			for elem in arr: 
				elem = elem.strip()
				if elem in data:
					temp_arr.append(data[elem])
			if len(temp_arr) > 0: 
				entry = ('; ').join(temp_arr)
					
			entries.append(entry)

	return entries 

def read_mappings(): 
	data = {}
	with open(mappings) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			gapp = row['GAPP #']
			csa = row['CSA #']
			if csa == '' or csa == 'N/A': 
				continue 
			data[csa] = gapp
	return data

def _write(entries): 
	with open('opc_cases_final_principles.csv', 'w') as csvfile: 
		writer = csv.writer(csvfile)
		fieldnames = ['GAPP Principles']
		writer.writerow(fieldnames)
		for entry in entries: 
			writer.writerow([entry])

# one time script 
if __name__ == "__main__":
	data = read_mappings()
	entries = read_keys(data)	
	_write(entries)