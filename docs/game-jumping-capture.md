# game-jumping-capture

[Voltar para documentação geral](./README.md)

## Arquivo principal: [app.py](../game-jumping-capture/app.py)

Este módulo executa uma aplicação que utiliza um modelo de machine learning (SVM ou rede neural) para detectar pulos em tempo real via webcam e simular comandos de teclado em jogos.

### Funcionalidades
- Captura frames da webcam e processa com Canny.
- Usa modelo treinado (SVM ou NN) para prever se o usuário está pulando.
- Simula pressionamento da tecla 'space' para controlar jogos automaticamente.
- Suporta troca fácil entre modelos SVM e NN.
- Permite pausar e retomar a predição.

### Como usar
1. Configure o tipo de modelo e caminho do modelo em `MODEL` e `MODEL_PATH` no início do arquivo.
2. Execute o script [`app.py`](../game-jumping-capture/app.py).
3. Pule na frente da webcam: o script detecta o pulo e simula a tecla 'space' no jogo.
4. Para pausar ou retomar a predição, utilize as teclas conforme instruções na tela.

### Estrutura do código
- `predict_model`: Função que retorna a função de predição adequada ao tipo de modelo.
- `imageProcess`: Pré-processamento dos frames (cinza + Canny).
- `classifier_thread`: Thread responsável por carregar o modelo, processar frames e simular o pulo.

### Pastas e arquivos
- [`app.py`](../game-jumping-capture/app.py): Script principal do módulo.
- Modelos treinados devem estar no caminho especificado em `MODEL_PATH`.

---

Para detalhes sobre o funcionamento do modelo, consulte também a documentação do módulo [model](./model.md).
