# Fase 1: perícia do vídeo de referência

Objetivo: entender **como** o vídeo de referência funciona (ritmo, visual, estrutura, título e capa) para reproduzir a linguagem num canal com tema e personagens próprios.

## 1. Pegar o vídeo
- Se houver um `.mp4` em `referencia/`, use-o.
- Se houver só `referencia/link.txt`, peça para a pessoa baixar o vídeo (por exemplo, com uma ferramenta que ela já usa) e colocar em `referencia/`. Se não der, analise pela página do vídeo no navegador: assista em pontos espaçados, tire screenshots e leia o título, a descrição e os capítulos. Avise que a análise fica mais pobre sem o arquivo.
- Abra também a página do **canal** de referência (aba "Vídeos", ordenada por mais populares) e anote os 10 vídeos mais vistos com as views e o tempo. Isso mostra quais temas e títulos funcionam.

## 2. Medir (com o arquivo)
Crie `referencia/pericia/` e rode:

```bash
# um quadro a cada 3 s para ver o ritmo e o estilo
ffmpeg -i referencia/VIDEO.mp4 -vf "fps=1/3,scale=480:-1" referencia/pericia/q_%04d.jpg
# folha de contato (6 colunas)
python ferramentas/scripts/grid.py referencia/pericia referencia/pericia/folha.jpg 6 320
# transcrição com tempos (para medir palavras por minuto e a estrutura)
python ferramentas/scripts/transcrever.py referencia/VIDEO.mp4 referencia/pericia/transcricao.json
# cortes de cena (quantos por minuto)
ffmpeg -i referencia/VIDEO.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2> referencia/pericia/cortes.txt
```

Olhe as folhas de contato (leia as imagens) e anote:

| Item | O que medir |
|---|---|
| Duração e ritmo | Duração total, cortes por minuto, segundos por cena, palavras por minuto da narração |
| Estrutura | Blocos do roteiro com os tempos (gancho, explicação, prova, mitos, passos, virada, prevenção, resumo, chamada final) |
| Visual | Fundo (cor, textura), traço (vetor, lápis, aquarela, 3D, foto), personagens (como são, quantos), quadros/molduras, texto na tela (fonte, cor, posição, como entra) |
| Animação | O que se mexe e como (letra por letra, pincelada, zoom, setas, sinais, contadores, câmera) e com que frequência |
| Áudio | Voz (gênero, ritmo, tom), música (sim/não, volume), efeitos |
| Título e capa | Fórmula do título (ex.: "Se [situação], faça ISSO"), texto da capa (palavras, cores), composição |

Para a paleta, tire as cores principais de 5 a 10 quadros típicos (por exemplo, com Pillow: `Image.quantize(6)`) e anote os códigos hex.

## 3. Entregar
1. `canal/ficha-do-canal.md` (use o modelo que já está na pasta): preencha a seção "Linguagem da referência" com tudo o que mediu.
2. `canal/estilo.json`: as cores do motor de animação, a fonte do letreiro e a cor do papel. Campos: `tinta` (texto e contornos), `alerta` (NÃO/ERRADO), `destaque` (setas), `ok` (certo), `neutro`, `marca_texto` (faixa atrás do rótulo), `papel` (fundo), `fonte_nome`, `fonte_arquivo` (o arquivo `.ttf` vai em `ferramentas/assets/`; use só fontes livres, como as do Google Fonts).
3. Uma folha de contato da referência ao lado de uma proposta de como o canal novo vai ficar (texto curto).
4. **Pare e mostre o resumo para a pessoa**: o que vamos copiar da linguagem, o que NÃO vamos copiar e qualquer ponto em que ela precise decidir (por exemplo, "a referência usa música; quer música ou só voz?").

## O que nunca copiar
Roteiro, falas, nomes e aparência dos personagens, logotipo, capas, trilha sonora, trechos de vídeo ou imagem. Se a pessoa pedir "igual", explique que fazemos **no mesmo estilo**, com conteúdo original, para não ter problema de direitos autorais nem de "conteúdo reutilizado" no YouTube.
