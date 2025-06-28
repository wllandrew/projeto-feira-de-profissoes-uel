import os
import cv2
import numpy as np
import joblib
from skimage.feature import hog
import time

# Configurações
CAMERA = 1 # Saber qual de camera hardware 
# Configurações de tratamento de imagem
RESOLUTION = (128, 128)
# HOG configs
ORIENTATIONS = 9
PIXELS_PER_CELL = (8, 8)
CELLS_PER_BLOCK = (2, 2)

# Carrega a camera
cap = cv2.VideoCapture(CAMERA)
# Carrega o modelo svm treinado
model = joblib.load('svm_model_test.pkl')

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
    return model.predict([feature])

# First test init cap
success, img = cap.read()
img = imageProcess(img)

last_prediction_time = time.time()
capture_interval = 0.1

isJumping = False
# main loop
while True:
    camFail = False
    success, img = cap.read()
    if not success:
        break

    now = time.time()
    if now - last_prediction_time >= capture_interval:
        processed = imageProcess(img)
        # feature, hog_img = extractImagesHog(processed)

        if processed is not None:
            pred = predict(processed.flatten().astype(np.uint8))
            isJumping = bool(pred[0])
 
        last_prediction_time = now

        cv2.imshow('IMAGEM PROCESSADA', cv2.resize(processed, getCamResolution(cap)))

    label = f"PULANDO: {isJumping}"
    color = (255, 0, 0) if isJumping else (0, 0, 255)
    cv2.putText(img, label, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    cv2.imshow('Video', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
