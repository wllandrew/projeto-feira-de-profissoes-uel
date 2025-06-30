# image-processing

[Voltar para documentação geral](./README.md)

## Arquivo principal: [app.py](../image-processing/app.py)

Este módulo é responsável por redimensionar e padronizar as imagens do dataset para um tamanho fixo, facilitando o uso em modelos de machine learning.

### Funcionalidades
- Lê imagens de uma pasta de origem (ex: `jumping-tratado`, `no-jumping-tratado`).
- Redimensiona cada imagem para 128x128 pixels.
- Salva as imagens redimensionadas em uma pasta de destino (ex: `jumping-redimensionado`, `no-jumping-redimensionado`).
- Exibe mensagens de sucesso ou falha para cada imagem processada.

### Como usar
1. Defina as pastas de origem e destino no início do arquivo.
2. Execute o script [`app.py`](../image-processing/app.py).
3. As imagens redimensionadas serão salvas automaticamente nas pastas de destino.

### Estrutura do código
- Função `processingImage`: faz o redimensionamento e salvamento das imagens.
- Execução para as duas classes (jumping e no-jumping).

### Pastas e arquivos
- [`app.py`](../image-processing/app.py): Script principal do módulo.
- Pastas de origem e destino configuráveis no início do script.

---

Para aumentar o dataset, consulte o módulo [image-augmentation](./image-augmentation.md).
