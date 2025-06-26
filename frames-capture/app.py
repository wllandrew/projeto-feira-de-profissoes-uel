import cv2
import numpy as np
import os
import time

i = 0
cap = cv2.VideoCapture(1)
directory = r'./jumping'
os.makedirs(directory, exist_ok=True)

next_timer_start = time.time() + 3
timer_phase = -1 
last_phase_time = 0

capturing_frames = False
capture_start_time = 0
frames_captured = 0

print("Pressione 'q' para sair.")

while True:
    success, img = cap.read()
    if not success:
        print("Erro ao acessar a câmera.")
        break

    cv2.imshow("Webcam", img)

    now = time.time()

    if timer_phase == -1 and now >= next_timer_start:
        print("\nPULE EM:")
        timer_phase = 3
        last_phase_time = now

    elif timer_phase in [3, 2, 1] and now - last_phase_time >= 1:
        print(timer_phase)
        last_phase_time = now
        timer_phase -= 1

    elif timer_phase == 0 and now - last_phase_time >= 1:
        print("PULE!")
        last_phase_time = now
        timer_phase = -2
        capturing_frames = True
        capture_start_time = now
        frames_captured = 0

    elif capturing_frames:
        if frames_captured < 5 and now - capture_start_time <= 1:
            if now - last_phase_time >= 0.4:
                last_phase_time = now
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                imgCanny = cv2.Canny(gray, 155, 105)
                cv2.imwrite(f'{directory}/image_{i}.png', gray)
                print(f"Imagem {i} salva!")
                i += 1
                frames_captured += 1
        else:
            capturing_frames = False
            timer_phase = -1
            next_timer_start = now + 3
            print()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()