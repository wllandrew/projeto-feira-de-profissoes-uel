import os
import cv2
# import numpy as np
# import pandas as pd
import albumentations as A

os.system('')

INPUT_DIR = "jumping"
OUTPUT_DIR = "augmented-jumping"
AUGMENT = 15
RESOLUTION = (128, 128)  
ROTULO = 1  # 'jumping' = 1
CSV_NAME = 'dataset-jumping.csv'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Augmentation pipeline
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.1, rotate_limit=4, border_mode=cv2.BORDER_REFLECT_101, p=0.7),
    A.Resize(RESOLUTION[1], RESOLUTION[0])
])

# Processar imagens e salvar imagens
cont = len(os.listdir(INPUT_DIR))+1
for file in os.listdir(INPUT_DIR):
    caminho = os.path.join(INPUT_DIR, file)
    imagem = cv2.imread(caminho)

    if imagem is None:
        continue

    print(f'\n\x1b[36mPATH: {caminho}\x1b[0m')
    print(f'Aumentando: {file}\t', end='\x1b[s')
    for i in range(AUGMENT):
        imagem_aug = transform(image=imagem)['image']
        imagem_cinza = cv2.cvtColor(imagem_aug, cv2.COLOR_BGR2GRAY)

        imagem_path = os.path.join(OUTPUT_DIR, f'imagem_{cont}.png')
        cv2.imwrite(imagem_path, imagem_cinza)

        print(f'\x1b[0K\x1b[u\x1b[32m{i+1:02d}/{AUGMENT:02d} Imagens aumentadas \x1b[0m', end='')
        cont += 1
    print()

print(f"\nTotal de amostras geradas: {cont+1}")
