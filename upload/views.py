from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.core.files.storage import FileSystemStorage

import csv

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['OWID']

@csrf_exempt
def upload_csv(request):

	# Handles CSV upload

	if request.method == 'POST' and request.FILES['file']:

		# Save CSV file
		uploaded_csv = request.FILES['file']
		fs = FileSystemStorage(location = settings.MEDIA_ROOT)
		csv_name = fs.save(uploaded_csv.name, uploaded_csv)

		# Parse file
		parseUploadedCsv(csv_name)

		# We no longer need the file, delete it
		fs.delete(csv_name)

	elif request.method == 'GET':

		# Ignore if request method is GET
		pass

	return HttpResponse("Done.")

def parseUploadedCsv(fileName):

	fs = FileSystemStorage(location = settings.MEDIA_ROOT)
	
	with fs.open(fileName, 'r') as fp:

		reader = csv.reader(fp)
		row_num = 0

		for row in reader:
			# Iterate over all rows of CSV

			if row_num == 0:

				# First line is header
				header = row

			else:

				valid = True

				for val in row:

					if len(val) == 0:

						# empty data point, we will not insert the row
						valid = False

				if valid:
					
					# Insert only if row is valid
					newPoint = {}

					# Generate dictionary to insert into MONGODB
					for i in range(len(row)):
						newPoint[header[i]] = row[i]

					# If data point doesn't exist in DB, insert

					if db.owid.find(newPoint).count() == 0:
						db.owid.insert(newPoint)

					else:
						# point already exists, ignore
						pass

				else:
					pass

			row_num += 1
