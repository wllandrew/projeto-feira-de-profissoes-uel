# data

[Voltar para documentação geral](./README.md)

## Arquivo principal: [pipeline.ipynb](../data/pipeline.ipynb)

Este módulo contém notebooks e scripts para preparação, rotulação e manipulação dos dados de entrada do projeto. Inclui pipelines para converter imagens em CSV rotulado e outras tarefas de pré-processamento.

### Funcionalidades
- Lê imagens das pastas de pulos (`jumping`) e não pulos (`not_jumping`).
- Redimensiona, normaliza e achata as imagens.
- Cria um DataFrame com as imagens e rótulos (`Jumping`: 1 para pulo, 0 para não pulo).
- Salva o DataFrame em um arquivo CSV para uso em modelos de machine learning.

### Como usar
1. Ajuste os caminhos das pastas de imagens e do CSV no início do notebook.
2. Execute o notebook [`pipeline.ipynb`](../data/pipeline.ipynb) célula por célula.
3. O arquivo CSV será gerado com todas as imagens e rótulos.

### Estrutura do código
- Função `imagesDataset`: lê, processa e rotula as imagens.
- Criação do DataFrame e exportação para CSV.

### Pastas e arquivos
- [`pipeline.ipynb`](../data/pipeline.ipynb): Notebook principal do módulo.
- Pastas de imagens e CSV configuráveis no início do notebook.

---

Para treinar modelos com esses dados, consulte o módulo [model](./model.md).