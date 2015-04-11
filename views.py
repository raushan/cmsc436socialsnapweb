from django.core import serializers
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from form import UserImageForm
from models import UserImage
from decimal import Decimal, localcontext
from utils import haversine
import json

def index(request):
	if request.method == 'POST':
		post_data = request.POST
		lat = Decimal(post_data['latitude'])
		lon = Decimal(post_data['longitude'])
		try:
			#check for the key that will by passed our android application
			if post_data['source']:
				results = []
				for uimg in list(UserImage.objects.all()):
					if haversine(lon, lat, uimg.longitude,uimg.latitude) < .5:
						results.append(uimg)
			
				#take the common objects between the 2 sets
				json_data = serializers.serialize("json",results)
				return HttpResponse(json_data,mimetype='application/json')	
		except MultiValueDictKeyError:
			a = UserImage()
			url = post_data['image_url']
			if 'comment' in post_data.keys():
				a.comment = post_data['comment']
			#populate model with data and save to database
			a.longitude = lon
			a.latitude = lat
			a.image_url = url
			a.save()
			json_data = json.dumps({'success':True, 'status':HttpResponse.status_code})
			return HttpResponse(json_data,mimetype='application/json')	
	ctx = {}	
	ctx['form'] = UserImageForm
	return render_to_response('main.html', ctx, context_instance=RequestContext(request))
