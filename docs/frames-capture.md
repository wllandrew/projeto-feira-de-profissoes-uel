# frames-capture

[Voltar para documentação geral](./README.md)

Este script é utilizado para capturar imagens da webcam e criar datasets de pulos (jumping) e não pulos (not-jumping) para projetos de visão computacional e machine learning.

## Como funciona
- O script abre a webcam e exibe dois frames: a imagem original com linhas de referência e a imagem processada (Canny) que será salva.
- O usuário pode controlar o início e pausa da captura, além de ajustar as linhas de referência para definir o que é considerado pulo.
- As imagens são salvas automaticamente nas pastas `jumping` e `not-jumping` dentro da pasta do script.

## Controles do teclado
- **p**: Inicia/pausa a captura de imagens.
- **Seta para cima (w)**: Sobe a linha amarela (linha de pulo).
- **Seta para baixo (s)**: Desce a linha amarela (linha de pulo).
- **e**: Sobe a linha azul (linha mínima).
- **d**: Desce a linha azul (linha mínima).
- **ESC**: Encerra o programa.

## Linhas de referência
- **Linha amarela (LINE_Y)**: Quando o topo do contorno detectado cruza essa linha, é considerado um pulo e a imagem é salva em `jumping`.
- **Linha azul (LINE_MINY)**: Usada como referência para distinguir movimentos que não são pulos. Se o contorno não ultrapassa essa linha, a imagem pode ser salva em `not-jumping`.

## Pastas de saída
- As imagens de pulos são salvas em `jumping/`.
- As imagens de não pulos são salvas em `not-jumping/`.

## Uso típico
1. Execute o script.
2. Ajuste as linhas de referência conforme necessário usando as teclas.
3. Pressione `p` para iniciar a captura.
4. Realize movimentos de pulo e não pulo na frente da câmera.
5. As imagens serão salvas automaticamente nas pastas corretas.
6. Pressione `ESC` para sair.

