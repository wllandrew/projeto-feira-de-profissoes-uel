# model

Este módulo reúne notebooks e scripts para treinar, validar e avaliar modelos de machine learning para detecção de pulos, incluindo SVM e redes neurais. Também contém scripts para ajuste de hiperparâmetros e manipulação de datasets.

### Funcionalidades
- Treinamento, validação e avaliação de modelos SVM e redes neurais.
- Busca de melhores hiperparâmetros para SVM (grid search).
- Manipulação e unificação de datasets para experimentos.

### Notebooks e scripts principais
- **[nn-model.ipynb](nn-model.ipynb)**: Treinamento de uma rede neural para classificar pulos a partir de imagens.
- **[new-svm-model.ipynb](new-svm-model.ipynb)**: Treinamento de um modelo SVM para detecção de pulos.
- **[grid_search.ipynb](grid_search.ipynb)**: Busca dos melhores hiperparâmetros para o SVM usando GridSearchCV.
- **[dataset/merge-dataset.ipynb](dataset/merge-dataset.ipynb)**: Unificação de diferentes datasets em um único arquivo CSV para facilitar o treinamento.

### Como usar
1. Execute os notebooks conforme o modelo desejado.
2. Ajuste os caminhos dos datasets e modelos conforme necessário.
3. Os modelos treinados serão salvos para uso em outros módulos do projeto.

Consulte a documentação detalhada em [`docs/model.md`](../docs/model.md) para mais informações e exemplos.
