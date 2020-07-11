#to run- python main.py --ip 127.0.0.1 --port 8000

#made in flask

from imutils.video import VideoStream
from flask import Response, url_for, redirect, request
from flask import Flask, flash
from flask import render_template
from numpy import loadtxt
from keras.models import load_model
from facereco import recognise
from facereco import takeImageWindow as imgwin
import argparse
import datetime
import imutils
import time
import cv2


app = Flask(__name__)

vs = VideoStream(src=0).start()
time.sleep(2.0)

reco = recognise()

@app.route("/")
def index():
    return render_template("index.html")


def generate():
	
	#global frame, passframe


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

		cv2.imwrite(".\static\FinalImg.jpg", frame)


		passframe = reco.face(frame)

		try:
			if passframe == None:
				flash('Cannot detect face. Kindly be steady and in front of camera and hit submit again.')
				time.sleep(5)

				return render_template("index.html")
		except:
			pass


		
		
		rec = reco.prediction(passframe)
		rec = rec.lower()



		return render_template("result.html",name = user,pred = rec, image_name=frame)

   


if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True)
	ap.add_argument("-o", "--port", type=int, required=True)
	
	args = vars(ap.parse_args())

	app.secret_key = 'SECRET KEY'
	# start the flask app
	app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)


vs.stop()