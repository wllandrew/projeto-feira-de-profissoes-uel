# Documentação do módulo: dino-game

## Arquivo: dino-game.py

Este script implementa uma versão customizada do jogo Dino Game (inspirado no jogo do Chrome), integrando um modelo de machine learning para detectar pulos reais do usuário via webcam.

### Funcionalidades principais:
- Utiliza OpenCV para capturar frames da webcam e processá-los.
- Usa um modelo SVM treinado para detectar se o usuário está pulando, a partir da imagem da webcam.
- Integração com Pygame para renderizar o jogo, controlar obstáculos, pontuação e sons.
- O personagem do jogo pula automaticamente quando o modelo detecta um pulo real do usuário.

### Uso
Permite jogar o Dino Game usando movimentos reais capturados pela webcam, tornando a experiência interativa e divertida.
