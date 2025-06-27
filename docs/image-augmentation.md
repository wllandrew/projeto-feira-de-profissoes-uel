# Documentação do módulo: image-augmentation

## Arquivo: augmentation.py

Este script aplica técnicas de aumento de dados (data augmentation) em imagens para expandir o dataset de treinamento.

### Funcionalidades principais:
- Utiliza a biblioteca Albumentations para aplicar transformações como flip horizontal, escala, rotação e ruído gaussiano.
- Lê imagens de uma pasta de entrada, aplica múltiplas variações e salva em uma pasta de saída.
- Converte as imagens aumentadas para escala de cinza antes de salvar.
- Exibe o progresso do aumento de dados no terminal.

### Uso
Aumenta a diversidade do dataset, ajudando a evitar overfitting e melhorando a robustez do modelo de machine learning.
