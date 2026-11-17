# Fase 4: roteiro de cenas (para aprovação)

## 1. Preparar a pasta e transcrever
```bash
python ferramentas/scripts/novo_video.py 01-tema "C:/caminho/do/audio.wav"
cd videos/01-tema/work
python transcrever.py narracao.wav transcricao.json
```
- A transcrição usa o faster-whisper (`large-v3-turbo`, CPU). Um áudio de 10 minutos leva de 12 a 17 minutos: rode em segundo plano e escreva o roteiro de cenas enquanto isso.
- Se o Whisper "comer" um trecho (o filtro de voz às vezes corta uma lista falada rápido), transcreva só aquele trecho sem VAD e corrija o `transcricao.json`.
- Compare a transcrição com o texto do roteiro (`difflib` nas palavras normalizadas) e ajuste a narração das cenas para o que a pessoa **realmente falou**.

## 2. A tabela de cenas
Crie `videos/01-tema/roteiro-cenas.md` (veja `modelos/exemplo-roteiro-cenas.md`). Uma linha por frase (~3,5 a 4 s; junte frases muito curtas):

`| # | Narração | Imagem | Texto na tela | Tipo |`

- **Texto na tela:** palavra-chave de 1 a 3 palavras em MAIÚSCULAS em toda cena.
- **Tipos:**
  - `IMG`: quadro ilustrado com personagem, parado dentro de uma moldura.
  - `MG`: recortes ilustrados + letreiro + setas e sinais (a maioria das cenas).
  - `🎬`: clipe animado a partir do quadro (Higgsfield Omni) nas cenas com personagens.
  - `🎬 Vids`: clipe do Google Vids (ou Flow) nas cenas de ambiente, sem personagens.
  - `✨ HTML`: animação mais elaborada (contador, zoom, seta que percorre, lista que se escreve).
- **Tudo é animado o tempo todo.** Nenhuma cena fica parada.
- Divida em blocos (`### Bloco N: nome ({BN})`) pela estrutura do roteiro. A primeira cena de cada bloco vira a lista `blocos` do `projeto.json`.
- Escreva no topo: configuração (voz, visual, personagens, onde gera cada coisa), cuidados com o tema, **custo estimado** e as listas de cenas com clipe.
- No fim: 3 títulos, descrição com capítulos (`{CAP}`), fontes e tags.

## 3. Tempos
```bash
python build_scenes.py        # gera scenes.json (início e fim de cada cena + palavras com tempo)
```
Preencha os tempos dos blocos e os capítulos da descrição a partir do `scenes.json`.

## 4. Quantos clipes
O padrão que funcionou: **30 clipes por vídeo de ~10 minutos**, sendo 20 a 25 Omni no Higgsfield (personagens) e 10 ou mais no Google Vids (ambientes). Se a pessoa tiver créditos sobrando no Flow, use também. Se ela pedir "o máximo possível no Vids", transforme cenas `MG` de objeto ou lugar em quadros de ambiente.

## 5. Custo (exemplo de referência)
| Item | Quantidade | Créditos |
|---|---|---|
| Quadros `gpt_image_2_5` medium 1k | ~40 | 0,5 cada |
| Recortes com fundo transparente | ~40 a 75 | 0,5 cada |
| Clipes Omni Flash 1.2 de 15 s (720p) | 20 a 25 | 33,75 cada (10 s = 22,5) |
| Capas `gpt_image_2_5` high 2k | 2 | ~2,75 cada |
| Google Vids | 10 a 20 | dentro do plano Google |

Um vídeo de 10 minutos com 20 clipes de 15 s fica perto de **720 créditos** no Higgsfield.

**Pare aqui. Envie o roteiro de cenas e espere a pessoa aprovar.** Se ela pedir mudanças (mais clipes, outra ferramenta), atualize o arquivo e registre no topo o que foi aprovado.
