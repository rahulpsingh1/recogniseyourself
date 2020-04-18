from numpy import loadtxt
from keras.models import load_model
import numpy as np
import time
import matplotlib.pyplot as plt
import cv2


class recognise:


	def face(frame):
		
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
		
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		for (x,y,w,h) in faces:
			roi_gray = gray[y:y+h, x:x+w]

			#resizing to make the image (128,128) for prediction
			pic=cv2.resize(roi_gray,(128,128),interpolation = cv2.INTER_AREA)
			pic = np.array(pic)
			pic = pic.reshape([-1,128, 128,1])

			return pic

	def prediction(image):
		
		model = load_model("./face_recognition.h5")

		t = model.predict(image)
		t = np.argmax(t, axis = 1)


		#model is trained on these people dataset

		dic = {"sandeep":0, "rahul":1, "sajan":2, "karishma":3, "utkarsh":4, "aashu":5}
		inv_dict = {v: k for k, v in dic.items()} 

		return inv_dict[t[0]]