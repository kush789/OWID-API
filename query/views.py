from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

# MONGO DB connections

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['OWID']


@csrf_exempt
def query(request):

	# Handles a query request

	if request.method == 'GET':

		# Query parameters from GET request
		qDict = request.GET.dict()

		# Filter from the database
		results = list(db.owid.find(qDict))

		# Delete DB ID from results

		for result in results:
			del result['_id']

		resp = {"results" : results}

		# Return JSON with results
		return HttpResponse(json.dumps(resp))

	else:

		# if request method POST, return empty dict

		return HttpResponse(json.dumps({}))