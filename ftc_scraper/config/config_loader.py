import os 
import json 

class ConfigLoader(): 

	CONFIG_FILE = 'config.json'

	def config(self): 
		""" Parse configuration """ 
		config_file = os.path.join(
				os.path.dirname(os.path.realpath(__file__)), 
				self.CONFIG_FILE)
		if not hasattr(self, '_parsed_config'): #won't read file if already loaded 
			self._parsed_config = self.load(config_file)
		return self._parsed_config

	def load(self, config_file): 
		""" Reads JSON file and assign it to instance variable """ 
		with open(config_file) as data_file: 
			self._parsed_config = json.load(data_file)
		return self._parsed_config