import os
import cv2
import numpy as np
import joblib
from skimage.feature import hog
import time
import keyboard
import keras

# Configurações
CAMERA = 2 # Saber qual de camera hardware 
# Configurações de tratamento de imagem
RESOLUTION = (128, 128)
# HOG configs
ORIENTATIONS = 9
PIXELS_PER_CELL = (8, 8)
CELLS_PER_BLOCK = (2, 2)

# Carrega a camera                        
cap = cv2.VideoCapture(CAMERA)                
# Carrega o modelo svm treinado
# model = joblib.load('svm_no_noise_test_1.pkl') 
model = keras.models.load_model("nn_model.keras")


def getCamResolution(cap):
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height      

def imageResizeToShow(img):
    return cv2.resize(img, getCamResolution(cap))

def imageProcess(img):
    if img is None:
        return 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (21, 21), 0)
    canny = cv2.Canny(gray, 155, 105)
    img = cv2.resize(canny, RESOLUTION)

    return img

def extractImagesHog(img):
    if img is None:
        return

    features, hog_img = hog(
        img,
        orientations=ORIENTATIONS,
        pixels_per_cell=PIXELS_PER_CELL,
        cells_per_block=CELLS_PER_BLOCK,
        block_norm='L2-Hys',
        visualize=True,
        feature_vector=True
    )

    return features, hog_img

def predict(feature):
    return model.predict(feature)

# First test init cap
success, img = cap.read()
img = imageProcess(img)



last_prediction_time = time.time()
capture_interval = 0.2

isJumping = False

pause = False
# main loop
while True:
    camFail = False
    success, img = cap.read()
    if not success:
        break


    key = cv2.waitKey(1) & 0xFF

    now = time.time()
    if now - last_prediction_time >= capture_interval:
        processed = imageProcess(img)
        # processed, hog_img = extractImagesHog(processed)

        if processed is not None:
            # processed = processed/255.0
            reshaped = np.reshape(processed, (processed.shape[0] * processed.shape[1]))
            # reshaped = (processed).reshape(-1) 
            pred = predict(reshaped.reshape(1, -1))  
            print(pred)             
            # pred = predict(processed.flatten().astype(np.uint8))
            # print(pred)
            print(pred.shape)
            if pred[0][1] > 0.90:
                isJumping = True
            else:
                isJumping = False
                
            if not pause:
                if isJumping:
                    keyboard.press('space')
                else:
                    keyboard.release('space')
 
        last_prediction_time = now

        cv2.imshow('IMAGEM PROCESSADA', cv2.resize(processed, getCamResolution(cap)))

    label = f"PULANDO: {isJumping}"
    color = (255, 0, 0) if isJumping else (0, 0, 255)
    cv2.putText(img, label, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    cv2.imshow('Video', img)

    if key == ord('q'):
        break

    if key == ord('p'):
        pause = not pause

cap.release()
cv2.destroyAllWindows()
