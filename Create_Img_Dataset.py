import cv2
import time
import os

par_path = r"C:\Users\RAIDEN\Desktop\face_reco_project\face_img\\"


print("enter name of person: ")
name = input()
path = os.path.join(par_path, name) 

try:  
    os.mkdir(path)  
except OSError:  
    print("directory name already exists")
    exit(0)


face_cascade = cv2.CascadeClassifier(r'C:\Users\RAIDEN\Desktop\face_reco_project\haarcascade_frontalface_default.xml')

cam = cv2.VideoCapture(0)
cv2.namedWindow("test")
time.sleep(3)



def face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        #roi_color = frame[y:y+h, x:x+w]
        
        return roi_gray


img_counter = 0
while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    
    frame = face(frame)
    
    if(frame is None):
        continue
    
    frame = cv2.resize(frame,(128,128),interpolation = cv2.INTER_AREA)
    
    
    if not ret:
        print("webcam not working")
        break
    k = cv2.waitKey(1)

        
    if k%256 == 27:
        # ESC pressed
        print("Escape pressed, closing...")
        break
    
    img_name = "testImg{}.png".format(img_counter)
    cv2.imwrite(os.path.join(par_path+name , img_name), frame)
    img_counter+=1
    print("{} written!".format(img_name))
    

cam.release()
time.sleep(3)
cv2.destroyAllWindows()