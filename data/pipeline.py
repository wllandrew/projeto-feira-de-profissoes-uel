import os
import numpy as np
import cv2
import pandas as pd
from skimage.feature import hog

"""
Pipeline para converter imagens com HOG e salvar como CSV rotulado.

0: not jumping
1: jumping
"""

# Configurações da função de extrair o hog das imagens
IMAGE_SIZE = (128, 128)
ORIENTATIONS = 8
PIXELS_PER_CELL = (8, 8)
CELLS_PER_BLOCK = (2, 2)

def imagesHogDataset(folder_path, label):
    dataset = []
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            continue

        img = cv2.resize(img, IMAGE_SIZE)

        features = hog(
            img,
            orientations=ORIENTATIONS,
            pixels_per_cell=PIXELS_PER_CELL,
            cells_per_block=CELLS_PER_BLOCK,
            block_norm='L2-Hys',
            visualize=False,
            feature_vector=True
        )

        dataset.append(np.append(features, label))
    return np.array(dataset)

def imagesDataset(folder_path, label):
    dataset = []

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            continue

        img = cv2.resize(img, IMAGE_SIZE)
        reshaped = np.reshape(img, (1, img.shape[0] * img.shape[1]))
       
        # vector = img.flatten().astype(np.uint8) # Alerta com essa parte
        dataset.append(np.append(reshaped, label))
    return np.array(dataset)


JUMPING_PATH = os.path.join(os.getcwd(), 'jumping')
NO_JUMPING_PATH = os.path.join(os.getcwd(), 'no-jumping')

# data_jumping = imagesHogDataset(JUMPING_PATH, label=1)
# data_no_jumping = imagesHogDataset(NO_JUMPING_PATH, label=0)
data_jumping = imagesDataset(JUMPING_PATH, label=1)
data_no_jumping = imagesDataset(NO_JUMPING_PATH, label=0)

print(data_jumping)
print(data_no_jumping)

dataset_total = np.vstack([data_jumping, data_no_jumping])
df = pd.DataFrame(dataset_total)

num_features = df.shape[1] - 1
df.columns = [f'{i}' for i in range(num_features)] + ['Jumping']

print(df)

csv_path = 'dataset.csv'
df.to_csv(csv_path, index=False)
print(f"CSV salvo como {csv_path} | Total: {len(df)} amostras")
