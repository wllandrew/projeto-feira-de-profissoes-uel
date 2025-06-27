import cv2
import numpy as np
import time
import os

cap = cv2.VideoCapture(2)

LINE_Y = 50 

success, img = cap.read()
first_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
first_gray = cv2.GaussianBlur(first_gray, (21, 21), 0)

while True:
    success, img = cap.read()
    if not success:
        break

    movimento_detectado = False
    
    LINE_Y = max(0, min(LINE_Y, img.shape[0] - 1))
    key = cv2.waitKey(30) & 0xFF

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    frame_delta = cv2.absdiff(first_gray, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(img, (0, LINE_Y), (img.shape[1], LINE_Y), (0, 255, 255), 2)

    movimento_detectado = False

    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        # center_y = y + h // 2
        center_y = y

        if center_y <= LINE_Y:
            timestamp = int(time.time())

            name_file = f"captura_{timestamp}.jpg"
            local_dir = os.path.dirname(os.path.abspath(__file__))

            directory = os.path.join(local_dir, 'jumping')
            os.makedirs(directory, exist_ok=True)

            arquivo = os.path.join(directory, name_file)

            cv2.imwrite(arquivo, img)
            print(f"[INFO] Movimento detectado! Imagem salva: captura_{timestamp}.jpg")
            movimento_detectado = True


        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    if not movimento_detectado:
        first_gray = gray.copy()

    cv2.imshow("Detecção de Movimento", img)

    if key == 115:  # seta para baixo
        LINE_Y += 10
    elif key == 119:  # seta para cima
        LINE_Y -= 10
    elif key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
