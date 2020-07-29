# Recognise-Yourself

This is a face recognition system which uses convolutional neural network to recognise faces. 
if the face captured is system recognisable then it output as recognised personnel else returns unrecognised while sending an email with the image of person. 
It also stores the given name, image location and time of entry of person in csv file.
System trained on 6 people faces and it also contains self data collection module to collect images for training.

* Base Language :- Python
* User interface :- Flask framework
* Recognition system :- keras, sklearn, opencv
* Email :- email, smtplib
* To csv :- csv

## Files

* main.py :- flask based gui and the main executible file
* Create_Img_Dataset.py :- to create image dataset
* Convolutional_Net.ipynb :- contains the CNN model for face recognition
* facereco.py :- capture face image and prediction of face
* send_email.py :- module for sending email
* write2csv.py :- save person data to csv


## Installation

### Requirements

  * Python 3.0+
  * clone this repository
  * git clone "github_url_link"
  * do a pip install 
  * pip install -r requirements.txt


## Thanks

* Thanks to stackoverflow and package documentations.
* Thanks to everyone who works on all the python libraries that made this project possible.

