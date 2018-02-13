from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db import models
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from display_data_app.forms import DataTypeForm, LocationForm, IndustryForm
from display_data_app.models import DataEntry, UserModel
import csv 
import json 
import ast 

def populate_database(): 
	#get data from privacy_principles doc 
	filename = 'display_data_app/privacy_principles.csv'
	data = {}
	with open(filename) as csvfile: 
		reader = csv.DictReader(csvfile)
		for i, row in enumerate(reader): 
			principle_id, subprinciple, note  = row['GAPP #'], row['GAPP Subprinciple'], row['GAPP Note']
			pos_rec, data_type = row['"Positive" Recommendation'], row['Actions with Data (from User Questionnaire)']
			data[principle_id] = [subprinciple, note, pos_rec, data_type]
	processed_data = []
	filename2 = 'display_data_app/ftc_cases.csv'
	with open(filename2) as csvfile: 
		reader = csv.DictReader(csvfile)
		for i, row in enumerate(reader): 
			principle_id, case_name = row['Privacy Principle - Primary'], row['Case Name']

			case_url, company_type_key, location, last_updated = row['Case URL'], row['Company Type Key'], row['Location'], row['Last Updated']
			principles_id = [x.strip() for x in principle_id.split(';')]
			if principles_id == ['']: 
				continue 
			if 'N/A' in principles_id[0]: 
				continue 
			count_happens, count_doesnt = 0, 0
			
			notes = []
			subprinciples = []
			pos_recs = []
			data_types = []
			for principle_id in principles_id: 	
				if principle_id in data: 		
					subprinciple, note, pos_rec, data_type = data[principle_id]
					notes.append(note)
					subprinciples.append(subprinciple)
					pos_recs.append(pos_rec)
					data_types.append(data_type)

			data_type_temp = set() 
			for data_type in data_types: 
				if "," in data_type: 
					data_type_list = data_type.split(',')
					for data_type_entry in data_type_list: 
						data_type_temp.add(data_type)
				else: 
					data_type_temp.add(data_type)


			data_entry = [case_name, case_url, last_updated, location, company_type_key, ('\n\n').join(subprinciples), ('\n\n').join(notes), ('\n\n').join(pos_recs), list(data_type_temp)]
			processed_data.append(data_entry)
	
	DataEntry.objects.all().delete() 

	#add data to model 
	for i, entry in enumerate(processed_data): 
		new_entry = DataEntry(case_name = entry[0], case_url = entry[1], last_updated=entry[2], location=entry[3], company_type_key=entry[4], subprinciple=entry[5], note=entry[6], pos_rec = entry[7], data_type=entry[8])
		new_entry.id = i + 1 
		new_entry.save() 
	print("completed data adding")
	exit() 

def index(request): 
	#populate_database()
	return render(request, 'index.html')

def is_valid(data_entry, data_types, locations, industries): 
	if data_entry.location in locations and data_entry.company_type_key in industries: 
		data_entry_data_types = ast.literal_eval(data_entry.data_type)
		for data_type in data_entry_data_types: 
			if data_type in data_types: 
				return True # return if they share at least one data type 
		return True 
	else: 
		return False 

class DataVisView(TemplateView):
	template_name = "data_vis.html"

	def data_types(self): 
		user = UserModel.objects.get(id=1)	
		return ast.literal_eval(user.data_type)

	def locations(self): 
		user = UserModel.objects.get(id=1)	
		return ast.literal_eval(user.location)

	def industries(self): 
		user = UserModel.objects.get(id=1)	
		return ast.literal_eval(user.industries)

	def data(self): 
		print(DataEntry.objects.all())
		print("in data vis POST view")
		user = UserModel.objects.get(id=1)	
		data_type_list = ast.literal_eval(user.data_type)
		locations_list = ast.literal_eval(user.location)
		industries_list = ast.literal_eval(user.industries)

		data = set() 
		for data_entry in DataEntry.objects.all(): 
			if is_valid(data_entry, data_type_list, locations_list, industries_list): 
				data.add(data_entry.id)

	
		#return super(TemplateView, self).render_to_response(context)
		return DataEntry.objects.filter(id__in = list(data)) 

class form1(FormView): 
	form_class = DataTypeForm 
	template_name = 'data_search_form_1.html'
	success_url = 'form2'

	print("in form1 view")
	def form_valid(self, form):
		print("in form_valid")
		#create user 
		UserModel.objects.all().delete() 
		action_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2')
		print(action_list) 
		new_user = UserModel(data_type=action_list)
		new_user.id = 1 
		new_user.save() 
		return super(form1, self).form_valid(form)
	
	def form_invalid(self, form): 
		print("in form invalid")
		return super(form1, self).form_valid(form)

class form2(FormView): 
	form_class = LocationForm
	template_name = 'data_search_form_2.html'
	success_url = 'form3'

	def form_valid(self, form):
		locations_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2') + self.request.POST.getlist('field3') + self.request.POST.getlist('field4')
		print(locations_list) 

		#select user 
		user = UserModel.objects.get(id=1)		
		user.location = locations_list
		user.save() 
		return super(form2, self).form_valid(form)
	
	def form_invalid(self, form): 
		print("in form invalid")
		return super(form2, self).form_valid(form)

class form3(FormView): 
	form_class = IndustryForm
	template_name = 'data_search_form_3.html'
	success_url = 'data-vis'

	def form_valid(self, form):
		industries_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2') 
		print(industries_list) 

		#select user 
		user = UserModel.objects.get(id=1)		
		user.industries = industries_list
		user.save() 
		return super(form3, self).form_valid(form)
	
	def form_invalid(self, form): 
		print("in form invalid")
		return super(form3, self).form_valid(form)

def faq(request): 
	return render(request, 'faq.html')

def glossary(request): 
	return render(request, 'glossary.html')

def data_search_info(request): 
	return render(request, 'data_search_info.html')

class AboutUs(TemplateView): 
	template_name = 'about_us.html'
