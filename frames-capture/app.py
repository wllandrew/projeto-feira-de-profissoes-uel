import cv2
import time
import os

def saveImageJPG(directory, image, file_name):
    local_dir = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(local_dir, directory)
    os.makedirs(dir, exist_ok=True)

    file = f"{file_name}.jpg"
    path = os.path.join(dir, file)
    cv2.imwrite(path, image)

    print(f"[INFO] Imagem salva: {file}")

cap = cv2.VideoCapture(0)

LINE_Y = 50 
LINE_MINY = 100

success, img = cap.read()
first_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

capturing = False
while True:
    success, img = cap.read()
    if not success:
        break
    key = cv2.waitKey(30) & 0xFF

    movimento_detectado = False
    
    LINE_Y = max(0, min(LINE_Y, img.shape[0] - 1))
    LINE_MINY = max(0, min(LINE_MINY, img.shape[0] - 1))
    cv2.line(img, (0, LINE_Y), (img.shape[1], LINE_Y), (0, 255, 255), 2)
    cv2.line(img, (0, LINE_MINY), (img.shape[1], LINE_MINY), (255, 0, 0), 2)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    save_img = cv2.resize(gray, (128,128))
    save_img = cv2.Canny(save_img, 155,105)

    frame_delta = cv2.absdiff(first_gray, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if capturing:
            timestamp = int(time.time())

            if y <= LINE_Y: # Passou da linha de pulo
                saveImageJPG('jumping', save_img, f'jumping_{timestamp}')
                movimento_detectado = True
            
            elif timestamp % 2 == 0 and y >= LINE_MINY: # não passou da linha mínima
                saveImageJPG('not-jumping', save_img, f'not_jumping_{timestamp}')

    if not movimento_detectado:
        first_gray = gray.copy()

    cv2.imshow("Detecção de Movimento", img)

    if key == ord('p'):
        capturing = not capturing
    elif key == 115:  # seta para baixo
        LINE_Y += 10
    elif key == 119:  # seta para cima
        LINE_Y -= 10
    elif key == 101:
        LINE_MINY -= 10
    elif key == 100:
        LINE_MINY += 10
    elif key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
