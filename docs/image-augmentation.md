# image-augmentation

[Voltar para documentação geral](./README.md)

## Arquivo principal: [augmentation.py](../image-augmentation/augmentation.py)

Este módulo aplica técnicas de aumento de dados (data augmentation) para expandir o dataset de imagens, gerando variações artificiais a partir das imagens originais usando a biblioteca Albumentations.

### Funcionalidades
- Lê imagens de uma pasta de entrada (ex: `no-jumping-redimensionado`).
- Aplica transformações como flip horizontal, rotação, shift, scale, resize, etc.
- Converte as imagens aumentadas para escala de cinza.
- Salva as imagens aumentadas em uma pasta de saída (ex: `augmented-no-jumping-noise`).
- Exibe o progresso do aumento de dados no terminal.

### Como usar
1. Defina as pastas de entrada e saída em `INPUT_DIR` e `OUTPUT_DIR` no início do arquivo.
2. Execute o script [`augmentation.py`](../image-augmentation/augmentation.py).
3. As imagens aumentadas serão salvas automaticamente na pasta de saída.

### Estrutura do código
- `transform`: Pipeline de aumentação com Albumentations.
- Loop principal: lê cada imagem, aplica as transformações e salva as variações.

### Pastas e arquivos
- [`augmentation.py`](../image-augmentation/augmentation.py): Script principal do módulo.
- Pastas de entrada e saída configuráveis no início do script.

---

Para preparar as imagens antes do aumento, consulte o módulo [image-processing](./image-processing.md).