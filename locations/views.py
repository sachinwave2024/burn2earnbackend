from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction

from locations.models import Country,State,Cities
import json

def insert_countries(request):
	
	json_data = open('locations/fixtures/countries.json').read()
	file_name = 'locations/fixtures/countries'
	pk = 0
	new_list = []

	with open('{}.json'.format(file_name)) as json_data:
		d = json.load(json_data)
		for item in d:
			pk+=1
			item = {"model": "locations.country", "pk": pk, "fields": item}
			new_list.append(item)
			json_data.close()
	with open(file_name+'.json', 'w') as file:
		json.dump(new_list, file)
	return JsonResponse({"result": "OK"})