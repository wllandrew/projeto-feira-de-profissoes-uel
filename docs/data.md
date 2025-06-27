# Documentação do módulo: data

## Arquivos: pipeline..py e Pipeline.ipynb

### pipeline..py
Script para converter imagens em um arquivo CSV rotulado, facilitando o uso em modelos de machine learning.

- Lê imagens das pastas 'jumping' e 'no-jumping'.
- Converte cada imagem para escala de cinza e achata em um vetor.
- Cria um DataFrame com todas as imagens e adiciona uma coluna 'Jumping' (1 para jumping, 0 para no-jumping).
- Salva o DataFrame em 'jumping-dataset-rotulado.csv'.

### Pipeline.ipynb
Notebook que realiza o pipeline de tratamento das imagens para o modelo:
- Conta o número de imagens em cada classe.
- Redimensiona, converte para cinza e achata as imagens.
- Cria um DataFrame e adiciona rótulos ('Jumping' ou 'Not Jumping').
- Salva o resultado em um CSV ('ans.csv').

### Uso
Esses arquivos são essenciais para preparar os dados de entrada para o treinamento e avaliação dos modelos de classificação.
