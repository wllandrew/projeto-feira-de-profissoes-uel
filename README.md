# Projeto de introdução do curso CDIA - Feira de Profissões UEL 2025

Este projeto foi desenvolvido para a Feira de Profissões da UEL em 2025, como uma introdução prática ao curso de Ciência de Dados e Inteligência Artificial (CDIA). O objetivo é demonstrar, de forma interativa, como visão computacional e machine learning podem ser aplicados para detectar pulos humanos em tempo real e controlar jogos usando apenas a webcam.

## Autores
- Andrew Willian Freitas
- Kauã Felipe Martins
- Leonardo Madeira Alves Pereira

---

## Como rodar o projeto

### 1. Pré-requisitos
- **Python 3.12** instalado ([download aqui](https://www.python.org/downloads/release/python-3120/)).
- Recomenda-se usar um ambiente virtual (venv) para evitar conflitos de dependências.

### 2. Instale as dependências
Abra o terminal na pasta do projeto e execute:

```bash
python -m venv venv
# Ative o ambiente virtual:
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
# source venv/bin/activate

pip install -r requirements.txt
```

### 3. Prepare os modelos
O programa principal ([game-jumping-capture/app.py](game-jumping-capture/app.py)) pode usar dois tipos de modelo:
- **SVM**: Modelo tradicional de machine learning, mais simples e rápido.
- **Rede Neural (NN)**: Modelo mais robusto, baseado em deep learning (TensorFlow/Keras).

Já existem dois modelos prontos disponíveis no projeto:
- Para SVM: arquivo `svm-super-model.pkl`
- Para NN: arquivo `nn_model_super.keras`
> Modelo de NN ainda precisa ser ajustado, mas já pode ser utilizado!

Basta selecionar o tipo de modelo e o caminho do arquivo no início do [`app.py`](game-jumping-capture/app.py) usando as variáveis `MODEL` e `MODEL_PATH`.

Se desejar, você pode treinar novos modelos utilizando os notebooks do módulo [model](model/README.md).

### 4. Configure o programa
No início do arquivo [`game-jumping-capture/app.py`](game-jumping-capture/app.py), ajuste as variáveis:
- `MODEL = 'SVM'` ou `MODEL = 'NN'` para escolher o tipo de modelo.
- `MODEL_PATH` para o caminho do arquivo do modelo treinado.
- `CAMERA` para o índice da sua webcam (geralmente 0 ou 1).

### 5. Execute o programa principal
No terminal, rode:

```bash
python game-jumping-capture/app.py
```

O programa irá:
- Capturar frames da webcam.
- Processar as imagens e detectar pulos em tempo real usando o modelo escolhido.
- Simular a tecla 'space' automaticamente quando um pulo for detectado, permitindo controlar jogos (como o Dino Game do Chrome) apenas pulando na frente da câmera.

### 6. Dicas de uso
- Certifique-se de que a iluminação e o enquadramento estejam adequados para melhor detecção.
- Para treinar ou ajustar modelos, utilize os scripts e notebooks dos módulos `frames-capture`, `image-processing`, `image-augmentation`, `data` e `model`.

---

## Estrutura dos módulos principais
- **[frames-capture](frames-capture/README.md)**: Captura imagens da webcam para criar o dataset de pulos e não pulos.
- **[image-augmentation](image-augmentation/README.md)**: Aplica técnicas de aumento de dados para expandir o dataset.
- **[image-processing](image-processing/README.md)**: Redimensiona e padroniza imagens para uso em modelos de machine learning.
- **[data](data/README.md)**: Scripts e notebooks para preparar e rotular os dados em formato CSV.
- **[model](model/README.md)**: Notebooks para treinar, validar e avaliar modelos SVM e redes neurais.
- **[game-jumping-capture](game-jumping-capture/README.md)**: Programa principal que detecta pulos em tempo real e simula comandos de teclado em jogos.

Cada módulo possui documentação detalhada na pasta [`docs/`](docs/).