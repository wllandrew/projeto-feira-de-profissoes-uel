'''
sair de x para (128px,72px)
'''

import cv2
import os

def processingImage(pasta_origem, pasta_destino):
    novo_tamanho = (128, 72)

    for nome_arquivo in os.listdir(pasta_origem):
        caminho_arquivo = os.path.join(pasta_origem, nome_arquivo)

        imagem = cv2.imread(caminho_arquivo)

        if imagem is not None:
            imagem_redimensionada = cv2.resize(imagem, novo_tamanho)

            caminho_salvar = os.path.join(pasta_destino, nome_arquivo)
            cv2.imwrite(caminho_salvar, imagem_redimensionada)

            print(f"Imagem salva: {nome_arquivo}")
        else:
            print(f"Falha ao abrir: {nome_arquivo}")

origem_jumping = "./frames-capture/jumping-tratado"
destino_jumping = "./image-processing/jumping-redimensionado"

origem_nojumping = "./frames-capture/no-jumping-tratado"
destino_nojumping = "./image-processing/no-jumping-redimensionado"

os.makedirs(destino_jumping, exist_ok=True)
os.makedirs(destino_nojumping, exist_ok=True)

processingImage(origem_jumping, destino_jumping)
processingImage(origem_nojumping, destino_nojumping)

