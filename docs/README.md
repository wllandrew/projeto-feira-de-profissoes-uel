# Projeto: Detecção de Pulos com Visão Computacional

Este projeto utiliza visão computacional e machine learning para detectar pulos de pessoas usando webcam, com aplicações em jogos interativos e análise de movimentos.

## Estrutura dos módulos e documentação

- [frames-capture](./frames-capture.md): Captura imagens da webcam para criar o dataset.
- [image-augmentation](./image-augmentation.md): Aumento de dados para expandir o dataset.
- [image-processing](./image-processing.md): Redimensionamento de imagens para padronização.
- [data](./data.md): Scripts e notebooks para preparação e rotulação dos dados.
- [model](./model.md): Treinamento e avaliação do modelo SVM para classificação de pulos.
- [dino-game](./dino-game.md): Jogo Dino Game controlado por pulos reais detectados pela webcam.

Cada módulo possui um arquivo de documentação detalhado na pasta `docs/` explicando seu funcionamento e uso.

## Resumo
O fluxo do projeto envolve:
1. Captura de imagens (pulos e não pulos)
2. Processamento e aumento do dataset
3. Preparação dos dados em CSV
4. Treinamento do modelo SVM
5. Aplicação do modelo em um jogo interativo

Ideal para estudos de visão computacional, machine learning e aplicações lúdicas.

---

## Propósito dos módulos

- **frames-capture**: Captura e salva imagens da webcam para compor o dataset de treinamento.
- **image-augmentation**: Aplica técnicas de aumento de dados para expandir e diversificar o dataset.
- **image-processing**: Redimensiona e padroniza imagens para uso em modelos de machine learning.
- **data**: Scripts para converter imagens em CSV rotulado e notebooks para pipeline de preparação dos dados.
- **model**: Notebooks para treinamento, validação e avaliação do modelo SVM.
- **dino-game**: Jogo interativo controlado por detecção de pulos em tempo real.

Consulte cada arquivo `.md` correspondente para detalhes e funções de cada módulo.
