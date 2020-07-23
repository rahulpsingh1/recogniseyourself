import csv 
from datetime import datetime


class csv_writer:

	def __init__(self):
          # this is an instance variable.
          # name of csv file
          self.filename = "RY_entry_records.csv"

	def create_csv_file(self):

		# field names 
		fields = ['Name', 'EntryTime', 'ImageLocation'] 


		with open(self.filename, 'w', newline='') as csvfile: 
		    # creating a csv writer object 
		    csvwriter = csv.writer(csvfile) 
		      
		    # writing the fields 
		    csvwriter.writerow(fields)


	def writeIntoCsv(self, name, imageLoc, correctlyRecognised):

		now = datetime.now()
		dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

		# checking the image is correctly recognised or not and save detail according to that
		if correctlyRecognised:
			recogCheck = "Correctly Recognised"
		else:
			recogCheck = "Not Recognised"

		rows = [ [name, dt_string, imageLoc, recogCheck] ]
		print(rows)

		# writing to csv file
		with open(self.filename, 'a+', newline='') as csvfile:
		    # creating a csv writer object 
		    csvwriter = csv.writer(csvfile) 
		      
		    # writing the data rows 
		    csvwriter.writerows(rows)


