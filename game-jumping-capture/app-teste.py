import cv2
import numpy as np
import joblib
import threading
import time
import keyboard
from skimage.feature import hog
import keras
# import tensorflow
# import warning

CAMERA = 2
RESOLUTION = (128, 128)
ORIENTATIONS = 9         
PIXELS_PER_CELL = (8, 8) 
CELLS_PER_BLOCK = (2, 2)
capture_interval = 0.2 

# model = joblib.load('grid_brest_estimator.pkl')  
model = keras.models.load_model("nn_model_super.keras")


 
frame = None
lock = threading.Lock()
isJumping = False
pause = True
running = True

def imageProcess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 155, 105)
    resized = cv2.resize(canny, RESOLUTION)
    return resized 

def imageProcessToShow(img): 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 155, 105)  
    return canny
 
def predict(img):
    # feature = img.flatten()
  
    # reshaped = img.reshape(-1) 
    reshaped = (img / 255.0).reshape(-1)
    # reshaped = np.reshape(img, (img.shape[0] * img.shape[1]))  
    return model.predict(reshaped.reshape(1, -1))[0]


def classifier_thread():
    global isJumping, frame, running, pause

    while running:
        # time.sleep(capture_interval)      
        if pause:
            continue
     
        with lock:
            if frame is None:
                continue
            img_copy = frame.copy()
     
        processed = imageProcess(img_copy)
        pred = predict(processed)

            
        print(pred)
        if pred[0] > 0.94:
            isJumping = True
        else:
            isJumping = False                   
                  
        if isJumping:         
            keyboard.press('space')
        else:
            keyboard.release('space')


def camera_thread():
    global frame, running, pause

    cap = cv2.VideoCapture(CAMERA)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * 0.6)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * 0.6)
 
    cv2.namedWindow("Video")
    cv2.namedWindow("Video_process")
    cv2.moveWindow("Video", 100, 50)
    cv2.moveWindow("Video_process", 100, 400)

    while running:
        success, img = cap.read()
        if not success:
            continue

        with lock:
            frame = img.copy()
        
        img = cv2.resize(img, (width, height))
        processed = imageProcessToShow(img)
        

        label = f"PULANDO: {isJumping}"
        color = (255, 0, 0) if isJumping else (0, 0, 255)
        cv2.putText(img, label, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.imshow("Video", img)
        cv2.imshow("Video_process", processed)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            running = False 
        elif key == ord('p'):
            pause = not pause

    cap.release()
    cv2.destroyAllWindows()

thread_cam = threading.Thread(target=camera_thread)
thread_cls = threading.Thread(target=classifier_thread)

thread_cam.start()
thread_cls.start()

thread_cam.join()
thread_cls.join()

keyboard.release('space')