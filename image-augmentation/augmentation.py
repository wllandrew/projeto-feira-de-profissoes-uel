import os
import cv2
# import numpy as np
# import pandas as pd
import albumentations as A

os.system('')

INPUT_DIR = "jumping"
OUTPUT_DIR = "augmented-jumping"
AUGMENT = 4 # devemos sair de 250 até mil (proximo do total de no-jumping) -> 4
RESOLUTION = (128, 72)  
ROTULO = 1  # 'jumping' = 1
CSV_NAME = 'dataset-jumping.csv'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Augmentation pipeline
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomScale(scale_limit=0.1, p=0.5),
    A.Rotate(limit=(-3, 3), border_mode=cv2.BORDER_REFLECT, p=0.5),
    A.GaussNoise(std_range=(0.05, 0.12), mean_range=(-0.2, 0.2), p=0.1)
    # A.Resize(RESOLUTION[1], RESOLUTION[0])
])

# Processar imagens e salvar imagens
cont = 0
# dataset = []
for file in os.listdir(INPUT_DIR):
    caminho = os.path.join(INPUT_DIR, file)
    imagem = cv2.imread(caminho)

    if imagem is None:
        continue

    print(f'\n\x1b[36mPATH: {caminho}\x1b[0m')
    print(f'Aumentando: {file}\t', end='\x1b[s')
    for i in range(AUGMENT):
        imagem_aug = transform(image=imagem)['image'] # Aplicar aumento
        imagem_cinza = cv2.cvtColor(imagem_aug, cv2.COLOR_BGR2GRAY)

        imagem_path = os.path.join(OUTPUT_DIR, f'Imagem_{cont}.png')
        # print(f'\n\x1b[36m{imagem_path}', end='')
        cv2.imwrite(imagem_path, imagem_cinza)

        # vetor = imagem_cinza.flatten()
        # dataset.append(np.append(vetor, ROTULO))
        
        print(f'\x1b[0K\x1b[u\x1b[32m{i+1:02d}/{AUGMENT:02d} Imagens aumentadas \x1b[0m', end='')
        cont += 1
    print()

print(f"\nTotal de amostras geradas: {cont+1}")

# df = pd.DataFrame(dataset)
# col = [f'{i}' for i in range(RESOLUTION[0] * RESOLUTION[1])] + ['jumping']
# df.columns = col
# df.to_csv(CSV_NAME, index=False)

# print(f"CSV salvo como {CSV_NAME}")
