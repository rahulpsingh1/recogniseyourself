#made in flask

from imutils.video import VideoStream
from flask import Response, url_for, redirect, request
from flask import Flask, flash
from flask import render_template
from facereco import recognise
#from facereco import takeImageWindow as imgwin
import time
import cv2
from send_email import emails
from write2csv import csv_writer
import uuid
import os


app = Flask(__name__)

vs = VideoStream(src=0).start()
time.sleep(2.0)

reco = recognise()
mail = emails()
csv_write = csv_writer()


@app.route("/")
def index():
    return render_template("index.html")


def generate():

	# loop over frames from the output stream
	while True:
		
		frame = vs.read()

		cv2.imwrite("flaskImage.jpg", frame)

		if frame is None:
			continue

		# encode the frame in JPG format
		(flag, encodedImage) = cv2.imencode(".jpg", frame)

		# encode successful check
		if not flag:
			continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():

	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")



#Name taken from user and the predicted image name both are necessary to recognise the person

@app.route('/result',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		user = request.form["nm"]
		user = user.lower()
		time.sleep(2.0)

		frame = cv2.imread("flaskImage.jpg")

		# get face from image
		face_frame = reco.face(frame)

		try:
			# if reco.face does'nt return any face then render the same page again
			if face_frame == None:
				flash('Cannot detect face. Kindly be steady and in front of camera and hit submit again.')
				time.sleep(5)
				return render_template("index.html")
		except:
			pass

		# predict the preson in image
		predicted_name = reco.prediction(face_frame)
		predicted_name = predicted_name.lower()

		unique_filename = str(uuid.uuid4().hex)
		imgLocation = ".\\static\\" + unique_filename + ".jpg"

		cv2.imwrite(imgLocation, frame)

		# also store passed name, time and the image location in csv file
		csv_write.writeIntoCsv(user, imgLocation, user == predicted_name)

		# if passed name and predicted name is not same then send email to admin
		if(user!=predicted_name):
			mail.sendEmail(imgLocation)


		return render_template("result.html",name = user,pred = predicted_name, image_name=imgLocation)

   


if __name__ == "__main__":

	# start the flask app
	app.secret_key = os.urandom(24)
	app.run(host="127.0.0.1", port=8000, debug=True, threaded=True, use_reloader=False)


vs.stop()