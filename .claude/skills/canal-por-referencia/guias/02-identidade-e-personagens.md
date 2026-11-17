# Fase 2: identidade do canal e personagens

O tema é da pessoa. A referência dá só a linguagem.

## 1. Tema, nome e fórmula
- Pergunte o tema (se ainda não disse) e o público. Exemplos: segurança no dia a dia, finanças pessoais, curiosidades de história, saúde, animais.
- Proponha 3 nomes curtos e fáceis de falar, e a **fórmula** do canal numa frase. Exemplo (canal de emergências): "o instinto do espectador manda fazer X, e X é exatamente o que piora tudo; o vídeo derruba o instinto com estudos reais e ensina os passos certos".
- Defina o formato do título e da capa a partir do que funcionou na referência (ex.: "[Situação]? NÃO [instinto]. Faça isso" e capa "PERGUNTA?" + "ORDEM!").
- Anote tudo em `canal/ficha-do-canal.md`.

## 2. Personagens próprios
- Crie um elenco pequeno e reaproveitável (um protagonista e de 3 a 7 secundários, mais um animal, se combinar com o tema). Descreva cada um com roupa fixa e uma característica marcante.
- Gere a **folha de personagens** no Higgsfield: `gpt_image_2_5`, quality `high`, `2k`, `16:9`, todos lado a lado no chão, nomes embaixo, fundo liso no tom do papel do canal, no traço definido na perícia. Se a pessoa já tiver um personagem (uma imagem), suba com `media_upload` e use como referência (`role: image_references`).
- Mostre a folha para a pessoa e **espere a aprovação**. Peça ajustes à vontade: é ela que define a cara do canal.
- Salve a folha aprovada em `canal/personagens/folha.png` e anote na ficha o **job id** do Higgsfield. Esse id é usado como referência em todos os quadros e capas (dá para passar o job id direto em `medias`).
- No prompt de todo quadro, repita as características do traço (ex.: "cabeça grande e redonda, olhos de pontinho, braços e pernas de palito em linhas finas azul-marinho") e a roupa de cada personagem citado. Isso evita que o traço "derive" de vídeo para vídeo, um problema real que já aconteceu.

## 3. Estilo dos recortes
- Gere 2 ou 3 recortes de teste (fundo transparente) e mostre junto com um quadro de teste, para a pessoa aprovar o conjunto.
- Suba um recorte aprovado como **referência de estilo** dos próximos recortes e anote o media id na ficha.
- A biblioteca de recortes fica em `canal/recortes/`. Todo recorte novo aprovado de cada vídeo deve ser copiado para lá: o `novo_video.py` já copia essa biblioteca para cada vídeo novo, e o custo cai a cada vídeo.
