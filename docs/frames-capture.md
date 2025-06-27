# Documentação do módulo: frames-capture

## Arquivo: app.py

Este script é responsável por capturar imagens da webcam para criar um dataset de imagens de pessoas pulando e não pulando. Ele utiliza OpenCV para acessar a webcam, processar as imagens (conversão para escala de cinza e detecção de bordas), e salva as imagens em diretórios específicos ('jumping' e 'no-jumping') dentro da própria pasta do script.

### Funcionalidades principais:
- Inicia a webcam e exibe o vídeo em tempo real.
- Realiza uma contagem regressiva para orientar o usuário a pular.
- Salva imagens em sequência nos diretórios corretos, garantindo que o caminho seja sempre relativo ao local do script.
- Permite pausar e retomar a captura de imagens com as teclas 'p' e 's'.
- Encerra a captura ao pressionar 'q'.

### Uso
Ideal para criar datasets balanceados para tarefas de classificação de imagens (ex: detecção de pulo).
