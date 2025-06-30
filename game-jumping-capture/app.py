import cv2
import threading
import keyboard
import time

# Configurações do programa
CAMERA = 1
RESOLUTION = (128, 128)
NORMALIZATION = 255.0
MODEL = 'NN' # SVM or NN
MODEL_PATH = 'nn_model_super.keras'
NN_MIN = 0.96 # S Apenas se for NN model
PREDICTS_PER_SECOND = 10 # Previsões que o modelo faz por segundo
CAM_FPS = 60 # Frames por segundo da camera

predictFrame = None
isJumping = False
pause = True
running = True
lock = threading.Lock()
modelLoading = True

def predict_model(model_type: str, model):
    if model_type.upper() == 'SVM':
        def predictJump(img):
            img = cv2.resize(img, RESOLUTION)
            reshaped = (img / NORMALIZATION).reshape(-1)
            return bool(model.predict([reshaped])[0])
        return predictJump
    elif model_type.upper() == 'NN':
        def predictJump(img):
            img = cv2.resize(img, RESOLUTION)
            reshaped = (img / NORMALIZATION).reshape(1, -1).astype('float32')
            return model.predict(reshaped)[0][0] > NN_MIN
        return predictJump
    else:
        raise ValueError("Modelo não suportado: escolha 'SVM' ou 'NN'.")

def imageProcess(img): 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 155, 105)
    return canny

def classifier_thread():
    global isJumping, predictFrame, running, pause, modelLoading

    if MODEL == 'SVM':
        import joblib
        load_model = lambda path: joblib.load(path)

    elif MODEL == 'NN':
        from tensorflow import keras
        load_model = lambda path: keras.models.load_model(path)
    else:
        raise ValueError("Modelo não suportado")
    
    model = load_model(MODEL_PATH)
    predictJump = predict_model(MODEL, model)
    
    while predictFrame is None:
        pass
    if predictJump(predictFrame): # Primeiro predict para loadingModel
        modelLoading = False


    interval = 1.0 / PREDICTS_PER_SECOND
    while running:  
        start_time = time.time()

        with lock:
            if predictFrame is None:
                continue

        pred = predictJump(predictFrame)

        if pred:
            isJumping = True
        else:
            isJumping = False                   
                  
        if isJumping and not pause:         
            keyboard.press('space')
        else:
            keyboard.release('space')
        
        elapsed = time.time() - start_time
        remaining_time = interval - elapsed
        if remaining_time > 0:
            time.sleep(remaining_time)

def camera_thread():
    global predictFrame, running, pause, modelLoading

    cap = cv2.VideoCapture(CAMERA)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * 0.6)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * 0.6)
    
    cv2.namedWindow("Video")
    cv2.namedWindow("Video_process")
    cv2.moveWindow("Video", 100, 50)
    cv2.moveWindow("Video_process", 100, 400)

    frame_interval = 1.0 / CAM_FPS
    while running:
        start_time = time.time()

        success, img = cap.read()
        if not success:
            continue

        img = cv2.resize(img, (width, height))
        processed = imageProcess(img)

        with lock:
            predictFrame = processed.copy()        

        color = (0, 255, 0) if isJumping else (0, 0, 255)

        cv2.putText(img, f"{'Pulando' if isJumping else 'No chao'}", (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        if modelLoading:
            cv2.putText(img, f"Carregando modelo...", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Video", img)
        cv2.imshow("Video_process", processed)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            running = False 
        elif key == ord('p'):
            pause = not pause

        elapsed = time.time() - start_time
        remaining_time = frame_interval - elapsed
        if remaining_time > 0:
            time.sleep(remaining_time)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    thread_cam = threading.Thread(target=camera_thread)
    thread_cls = threading.Thread(target=classifier_thread)

    thread_cam.start()
    thread_cls.start()

    thread_cam.join()
    thread_cls.join()

    keyboard.release('space')