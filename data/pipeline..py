import os
import numpy as np
import cv2
import pandas as pd

"""
Pipeline para converter as imagens em csv com rótulos

0: not jumping
1: jumping
"""

def getImagesToNumpy(images_path):
    dataset = []
    for file in os.listdir(JUMPING_IMAGE_PATH):
        img_path = os.path.join(JUMPING_IMAGE_PATH, file)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if img is None:
            continue    

        dataset.append(img.flatten())
    return dataset

def createDataframeLabeled(dataset, label, value):
    df = pd.DataFrame(dataset)
    df[label] = value
    return df


JUMPING_IMAGE_PATH = os.path.join(os.getcwd(), 'jumping')
NO_JUMPING_IMAGE_PATH = os.path.join(os.getcwd(), 'no-jumping')

dfJumping = createDataframeLabeled(getImagesToNumpy(JUMPING_IMAGE_PATH), 'Jumping', 1)
dfNoJumping = createDataframeLabeled(getImagesToNumpy(JUMPING_IMAGE_PATH), 'Jumping', 0)
df = pd.concat([dfJumping, dfNoJumping])

df.to_csv('jumping-dataset.csv', index=False)

    