import os
import time
import urllib.request

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from pynput.keyboard import Key, Controller

_keyboard = Controller()

CAMERA_INDEX = 0             
CALIBRATION_FRAMES = 45      
JUMP_THRESHOLD_RATIO = 0.06  
                              
                          

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pose_landmarker_lite.task")
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/pose_landmarker/"
    "pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
)

LEFT_HIP_IDX = 23
RIGHT_HIP_IDX = 24

POSE_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5), (5, 6), (6, 8),
    (9, 10), (11, 12), (11, 13), (13, 15), (15, 17), (15, 19), (15, 21),
    (17, 19), (12, 14), (14, 16), (16, 18), (16, 20), (16, 22), (18, 20),
    (11, 23), (12, 24), (23, 24), (23, 25), (24, 26), (25, 27), (26, 28),
    (27, 29), (28, 30), (29, 31), (30, 32), (27, 31), (28, 32),
]


def set_space_held(should_hold: bool):
    if should_hold:
        _keyboard.press(Key.space)
    else:
        _keyboard.release(Key.space)


def ensure_model():
    """Garante que o arquivo de modelo do PoseLandmarker existe localmente,
    baixando-o na primeira execução."""
    if os.path.exists(MODEL_PATH):
        return
    print("Baixando modelo de detecção de pose (isso só acontece uma vez)...")
    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print(f"Modelo salvo em: {MODEL_PATH}")
    except Exception as e:
        raise RuntimeError(
            "Não foi possível baixar o modelo automaticamente. "
            f"Baixe manualmente em {MODEL_URL} e salve como '{MODEL_PATH}'.\n"
            f"Erro original: {e}"
        )


def draw_landmarks(frame, landmarks):
    """Desenha o esqueleto detectado sobre o frame (substitui o antigo
    mp_drawing.draw_landmarks, que não existe mais na API nova)."""
    h, w, _ = frame.shape
    points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

    for a, b in POSE_CONNECTIONS:
        if a < len(points) and b < len(points):
            cv2.line(frame, points[a], points[b], (0, 255, 0), 2)
    for p in points:
        cv2.circle(frame, p, 3, (0, 0, 255), -1)


ensure_model()

base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
options = mp_vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=mp_vision.RunningMode.VIDEO,
    num_poses=1,
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)
detector = mp_vision.PoseLandmarker.create_from_options(options)

cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    raise RuntimeError("Não foi possível acessar a câmera. Verifique o índice/conexão.")

paused = False
calibrated = False
baseline_y = None
calibration_values = []

is_jumping = False
frame_timestamp_ms = 0  

print("Iniciando... fique de pé, parado e visível para a câmera para calibrar.")
print("Controles: P = pausar/retomar | Q = sair")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar frame da câmera.")
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("Encerrando...")
            break
        elif key == ord('p'):
            paused = not paused
            print("Pausado." if paused else "Retomado.")

        status_text = ""
        color = (0, 255, 0)

        if not paused:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            frame_timestamp_ms += 1
            result = detector.detect_for_video(mp_image, frame_timestamp_ms)

            if result.pose_landmarks:
                landmarks = result.pose_landmarks[0]  # primeira pessoa detectada
                draw_landmarks(frame, landmarks)

                left_hip = landmarks[LEFT_HIP_IDX]
                right_hip = landmarks[RIGHT_HIP_IDX]
                hip_y = (left_hip.y + right_hip.y) / 2

                if not calibrated:
                    calibration_values.append(hip_y)
                    status_text = f"Calibrando... ({len(calibration_values)}/{CALIBRATION_FRAMES})"
                    color = (0, 255, 255)

                    if len(calibration_values) >= CALIBRATION_FRAMES:
                        baseline_y = sum(calibration_values) / len(calibration_values)
                        calibrated = True
                        print(f"Calibração concluída. Baseline = {baseline_y:.4f}")

                else:
                    diff = baseline_y - hip_y
                    currently_up = diff > JUMP_THRESHOLD_RATIO
                    is_jumping = currently_up

                    set_space_held(is_jumping)

                    if is_jumping:
                        status_text = "PULANDO! (espaço pressionado)"
                        color = (0, 0, 255)
                    else:
                        status_text = "No chao"
                        color = (0, 255, 0)

                    baseline_px = int(baseline_y * h)
                    threshold_px = int((baseline_y - JUMP_THRESHOLD_RATIO) * h)
                    cv2.line(frame, (0, baseline_px), (w, baseline_px), (255, 0, 0), 1)
                    cv2.line(frame, (0, threshold_px), (w, threshold_px), (0, 255, 255), 1)
            else:
                status_text = "Nenhuma pessoa detectada"
                color = (0, 0, 255)
                set_space_held(False)  # ninguém detectado -> garante que a tecla não fique presa
        else:
            status_text = "PAUSADO (pressione P para retomar)"
            color = (0, 165, 255)
            set_space_held(False)  # pausou -> solta a tecla imediatamente

        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(
            frame,
            "Q: sair | P: pausar/retomar",
            (10, h - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

        cv2.imshow("Detector de Pulo - OpenCV", frame)

finally:
    set_space_held(False)  
    cap.release()
    cv2.destroyAllWindows()
    detector.close()