# from numpy import loadtxt
from keras.models import load_model
import numpy as np
import time
import matplotlib.pyplot as plt
import cv2
import copy


# this class is for testing
class takeImageWindow:

    # this function returns the image from disk.
    def picFromDisk(self):
        pic = cv2.imread("opencv_frame_0.png")
        pict1 = cv2.resize(pic, (128, 128), interpolation=cv2.INTER_AREA)
        plt.imshow(pict1)
        return pict1

    # this function captures image from webcam and return the image.
    def picFromCamera(self):
        cam = cv2.VideoCapture(0)
        time.sleep(2)
        cv2.namedWindow("Input Picture")
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        img_counter = 0
        while True:
            ret, frame = cam.read()

            finalframe = copy.deepcopy(frame)

            if ret == True:

                # Convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Detect the faces
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                # Draw the rectangle around each face
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                cv2.imshow("test", frame)

                k = cv2.waitKey(1)

                if k % 256 == 27:
                    # when esc pressed
                    print("Escape hit, closing...")
                    break
                elif k % 256 == 32:
                    # when space pressed
                    img_name = 'compressed.jpg'
                    cv2.imwrite(img_name, finalframe)
                    print("{} written!".format(img_name))

                    # compress

                    pic = cv2.imread("compressed.jpg")

                    plt.imshow(frame)

                    break
            else:
                break
        cam.release()
        time.sleep(3)
        cv2.destroyAllWindows()

        return pic


class faceblock:

    # this function captures the face in image and return only the face image.
    def face(self, frame):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print("faces blocks ----------------------")
        print(faces)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]

            # resizing to make the image (128,128) for prediction
            pic = cv2.resize(roi_gray, (128, 128), interpolation=cv2.INTER_AREA)
            pic = np.array(pic)
            pic = pic.reshape([-1, 128, 128, 1])

            return pic


class recognise(faceblock):

    # returns the predicted person by face recognition model.
    def prediction(self, image):
        model = load_model("./face_recognition.h5")

        t = model.predict(image)
        print(t)
        print("--------------------------------")
        # put a constraint to accuracy more than 60% then found else not recognisable.
        t = np.argmax(t, axis=1)

        # model is trained on these people dataset

        dic = {"sandeep": 0, "rahul": 1, "sajan": 2, "karishma": 3, "utkarsh": 4, "aashu": 5}
        inv_dict = {v: k for k, v in dic.items()}

        return inv_dict[t[0]]
