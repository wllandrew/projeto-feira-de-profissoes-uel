import os
import cv2
import joblib
from skimage.feature import hog
import time

# Configurações
CAMERA = 0 # Saber qual de camera hardware 
# Configurações de tratamento de imagem
RESOLUTION = (128, 128)
# HOG configs
ORIENTATIONS = 9
PIXELS_PER_CELL = (8, 8)
CELLS_PER_BLOCK = (2, 2)

# Carrega a camera
cap = cv2.VideoCapture(CAMERA)
# Carrega o modelo svm treinado
model = joblib.load('hog_svm_model.pkl')
last_capture_time = 0
capture_interval = 0.2  # 200 ms


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

isJumping = False
# main loop
while True:
    camFail = False
    success, img = cap.read()
    if not success:
        break

    processed_img = imageProcess(img)
    feature, hog_img = extractImagesHog(processed_img)

    cv2.imshow('HOG', cv2.resize(hog_img, getCamResolution(cap)))

    if feature is not None:
        if predict(feature)[0] == 1:
            isJumping = True
        else:
            isJumping = False
    else:
        camFail = True

    if not camFail:
        cv2.putText(img, f'PULANDO: {isJumping}', (480//2, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),3)
    else:
        cv2.putText(img, f'Erro', (480//2, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)

    cv2.imshow('Video', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
