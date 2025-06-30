# model

[Voltar para documentação geral](./README.md)

## Notebooks principais

- [nn-model.ipynb](../model/nn-model.ipynb): Treinamento de uma rede neural para classificar pulos a partir de imagens. Inclui preparação dos dados, definição do modelo, treinamento, avaliação e salvamento do modelo.
- [new-svm-model.ipynb](../model/new-svm-model.ipynb): Treinamento de um modelo SVM para detecção de pulos. Inclui preparação dos dados, treinamento, avaliação e salvamento do modelo.
- [grid_search.ipynb](../model/grid_search.ipynb): Busca dos melhores hiperparâmetros para o SVM usando GridSearchCV.
- [dataset/merge-dataset.ipynb](../model/dataset/merge-dataset.ipynb): Unificação de diferentes datasets em um único arquivo CSV para facilitar o treinamento.

### Funcionalidades
- Treinamento, validação e avaliação de modelos SVM e redes neurais.
- Busca de melhores hiperparâmetros para SVM.
- Manipulação e unificação de datasets.

### Como usar
1. Execute os notebooks conforme o modelo desejado.
2. Ajuste os caminhos dos datasets e modelos conforme necessário.
3. Os modelos treinados serão salvos para uso em outros módulos do projeto.

### Pastas e arquivos
- Todos os notebooks estão na pasta [`model`](../model/).
- Modelos treinados são salvos na subpasta `models/`.

---

Para usar os modelos em aplicações, consulte o módulo [game-jumping-capture](./game-jumping-capture.md).
