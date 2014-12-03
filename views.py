from django.core import serializers
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from form import UserImageForm
from models import UserImage
from decimal import Decimal
import json

def index(request):
	if request.method == 'POST':
		post_data = request.POST
		lat = Decimal(post_data['latitude'])
		lon = Decimal(post_data['longitude'])
		try:
			#check for the key that will by passed our android application
			if post_data['source']:
				range_val = Decimal(.0002)
				#make 2 separate queries for userimage objects in range because 
				#the app engine non-relational database has a limit on joins
				results_lat = UserImage.objects.filter(latitude__gte=(lat - range_val),
										 latitude__lte=(lat + range_val))
				results_lon = UserImage.objects.filter(longitude__gte=(lon - range_val),
										 longitude__lte=(lon + range_val))
				#take the common objects between the 2 sets
				joined_results =  set(results_lat) & set(results_lon)
				json_data = serializers.serialize("json", joined_results)
				return HttpResponse(json_data,mimetype='application/json')	
		except MultiValueDictKeyError:
			url = post_data['image_url']
			#populate model with data and save to database
			a = UserImage()
			a.longitude = lon
			a.latitude = lat
			a.image_url = url
			a.save()
			json_data = json.dumps({'success':True, 'status':HttpResponse.status_code})
			return HttpResponse(json_data,mimetype='application/json')	
	ctx = {}	
	ctx['form'] = UserImageForm
	return render_to_response('main.html', ctx, context_instance=RequestContext(request))
