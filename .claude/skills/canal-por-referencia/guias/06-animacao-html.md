# Fase 5b: animação em HTML (o motor)

A camada de cima do vídeo (letreiro, recortes, setas, sinais, molduras, contadores) é HTML + GSAP, renderizado em PNG com transparência pelo HyperFrames. O motor é `gen_ref.py`; cada vídeo tem o seu **spec** (`work/spec.py`), que diz o que aparece em cada cena, no tempo de cada palavra falada.

## 1. projeto.json (na pasta work)
```json
{
 "spec": "spec",
 "blocos": [1, 18, 31, 44, 55, 71, 84, 99, 119, 131, 138],
 "clipes": [1, 3, 5, 11],
 "saida": "../tema-final.mp4",
 "projeto_davinci": "Canal_01_Tema"
}
```
`blocos` = primeira cena de cada bloco do roteiro de cenas. Cada bloco vira um HTML e uma sequência de PNG.

## 2. O spec
Copie `modelos/exemplo-spec.py` para `work/spec.py` e reescreva cena por cena. Estrutura:
```python
from gen_ref import *
def P(n, color='teal'):  return FRAME(f'panels/{n:03d}.jpg', 960, 610, 1240, 698, st(n, .05), color)   # quadro parado
def CF(n, color='teal'): return FRAME(None, 960, 610, 1240, 698, st(n, .05), color)                    # só a moldura (o clipe fica embaixo)
S = SPEC = {}
S[1] = [T('20H'), CF(1)]
S[2] = [T('SILÊNCIO'), CUT('geladeira', 820, 650, 360, st(2, .05)), XX(1200, 560, 150, wt(2, 'barulho'))]
```
- **Tempos:** `st(cena, d)` = início da cena + d segundos; `wt(cena, 'palavra', nth=1, d=0)` = instante em que a palavra é falada. Para números, use o que o Whisper escreveu (geralmente dígitos: `wt(34, '1950')`). No fim, o motor lista as palavras que não encontrou: corrija até a lista ficar vazia.
- **Cores da moldura:** `'teal'` (neutro), `'green'` (certo), `'red'` (errado).
- **Letreiro:** `T('TEXTO', color=RED)`, `px=104` para textos longos. Fica sempre no alto, nunca recebe zoom e nunca é cortado. NÃO, NUNCA, FALSO, ERRO e NADA ficam vermelhos sozinhos.
- **Elementos:** `CUT` (recorte, com `enter='pop'`, `wiggle=True`, `beat=True`, `flip=True`), `TAG`, `ARROW`, `LINE`, `NO`, `XX`, `CHECK`, `HALO`, `ZOOM`, `MOVE`, `DROP`, `NUM`, `CARD`, `COUNTER`, `BAR`, `PRESS`, `FLASH`, `DARK`, `BTN`, `ROWS` (quadro-resumo com ícone + texto). A lista e os parâmetros estão no começo do `gen_ref.py`.
- **Palco nunca vazio:** mantenha no fim do spec o laço que traz o primeiro elemento de cada cena para o início dela (está no exemplo). Sem isso, cenas cujo recorte entra numa palavra do fim da frase ficam vazias por 2 ou 3 segundos.
- Posições: a tela é 1920x1080; o letreiro ocupa o topo (y≈130); use y entre 400 e 950 para o palco. Recortes altos são limitados a 660 px de altura automaticamente.
- Clipes entram no retângulo da moldura (340, 261, 1240x698). Cena com clipe usa `CF(n)`; cena com quadro parado usa `P(n)`.

## 3. Gerar e renderizar
```bash
python gen_ref.py                       # todos os blocos -> hf/mg_bNN.html + hf/blocks.json
python gen_ref.py 8                     # só o bloco 8 (depois de uma correção)
cd hf
bash render_blocos.sh 01 02 03 04 05 06 &    # fila 1
bash render_blocos.sh 07 08 09 10 11 &       # fila 2 (em paralelo)
```
Cada bloco de ~1 minuto leva de 5 a 8 minutos. Confira se o número de quadros de `hf/out/bNN` bate com `duração × 30` do `blocks.json` (diferença de 1 quadro é normal).

## 4. Revisar antes de montar
Depois que o `base.mp4` existir (próximo guia):
```bash
python check_frames.py chk.jpg 12.5 40 75.2 ...   # compõe fundo + camada HTML nesses instantes
```
Escolha instantes ~2,4 s depois do início de cenas variadas e leia a imagem. Procure palco vazio, recorte em cima de outro, contador em cima de boneco, texto cortado e moldura sem clipe. Corrija o spec, gere e renderize só o bloco afetado.
