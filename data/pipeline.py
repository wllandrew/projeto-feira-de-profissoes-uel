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

RESOLUTION = (128, 128)

def imagesDataset(folder_path, label):
    dataset = []

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            continue

        img = cv2.resize(img, RESOLUTION)
        reshaped = np.reshape(img, (1, img.shape[0] * img.shape[1]))
       
        dataset.append(np.append(reshaped, label))
    return np.array(dataset)


JUMPING_PATH = os.path.join(os.getcwd(), 'jumping')
NO_JUMPING_PATH = os.path.join(os.getcwd(), 'not_jumping')

data_jumping = imagesDataset(JUMPING_PATH, label=1)
data_no_jumping = imagesDataset(NO_JUMPING_PATH, label=0)

print(data_jumping)
print(data_no_jumping)

dataset_total = np.vstack([data_jumping, data_no_jumping])
df = pd.DataFrame(dataset_total)

num_features = df.shape[1] - 1
df.columns = [f'{i}' for i in range(num_features)] + ['Jumping']

print(df)

csv_path = 'dataset-no-noise.csv'
df.to_csv(csv_path, index=False)
print(f"CSV salvo como {csv_path} | Total: {len(df)} amostras")
