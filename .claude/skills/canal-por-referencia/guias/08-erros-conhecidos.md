# Erros conhecidos (e como evitar)

Problemas que já aconteceram de verdade na produção e custaram retrabalho.

## Personagens e imagens
- **O traço "deriva" entre vídeos.** Com o tempo, o personagem ficou com corpo "humano" e perdeu a característica original. A pessoa percebeu e reclamou. Sempre use a folha aprovada como referência e repita as características do traço no prompt. Se mudar, refaça a folha a partir da original.
- **Roupa comprida esconde o traço.** Pijama ou calça comprida fazem o modelo desenhar pernas grossas. Peça roupa curta e diga que as pernas de palito ficam à mostra.
- **Personagens a mais.** O modelo tende a pôr a família inteira em qualquer cena. Escreva "desenhe SOMENTE os personagens citados" ou "SEM nenhuma pessoa".
- **Recorte errado da biblioteca.** Um nome genérico (`mao`, `boca`, `maos`) pode ser outra coisa (mão caída, beijo). Olhe a imagem antes de usar e crie nomes específicos (`mao_acenando`, `boca_gritando`).
- **Imagem que mostra sofrimento.** Uma criança em pânico na água foi trocada por um adulto encenando. Em temas sensíveis, mostre com objetos, setas e diagramas.

## Higgsfield
- Clipe Omni sem `mode: "image-to-video"` dá erro 422.
- O filtro `nsfw` recusa faíscas, fogo perto de gente e alguém em perigo. Refaça mais calmo.
- **Conector sumiu da sessão:** a sessão não carrega conectores novos no meio do caminho. Peça para a pessoa conectar em Configurações > Conectores e, se ainda não aparecer, abrir uma sessão nova no mesmo projeto. Os arquivos ficam salvos e a produção continua de onde parou.
- Limite de requisições (429) no TTS: reenvie só os que falharam.

## Google Vids e Flow
- Sem o ajuste do `HTMLInputElement.click`, o "Adicionar imagem" abre o seletor do Drive em vez do arquivo local.
- Depois de cada envio, clique em **Limpar**; senão o campo de arquivo não volta.
- Baixar com `fetch` sem `credentials:'include'` dá erro de CORS.
- No Flow, o clique no chip "Início" por JavaScript é ignorado: precisa ser um clique de verdade. O download 2K parou sem aviso depois de ~66 imagens; o tamanho original basta.
- Mantenha cada chamada de JavaScript no navegador abaixo de ~45 s.

## Áudio e transcrição
- O Whisper com VAD cortou falas (uma lista falada rápido). Transcreva o trecho de novo sem VAD e corrija.
- O Whisper escreve números com dígitos ("1950", "1 400"). Use os dígitos no `wt()`.
- A voz do Gemini lê em voz alta qualquer instrução de estilo que estiver no texto. Mande só o texto.
- Narração de IA costuma vir com picos altos. O `base_papel.py` já normaliza a -14 LUFS e passa um limitador; confira o pico no fim (`loudnorm=print_format=summary`, True Peak abaixo de -1 dBTP).

## ffmpeg, Windows e scripts
- No ffmpeg 8/9, use `-/filter_complex arquivo.txt` (o `-filter_complex_script` foi removido) e `-fps_mode` (não `-vsync`).
- No Windows, defina `PYTHONIOENCODING=utf-8` para não quebrar acentos na saída.
- Arquivos baixados da internet: guarde em pasta própria e rode o Python com `-I` quando ler esses arquivos.

## Animação
- Palco vazio no começo da cena: mantenha o laço "palco nunca vazio" no fim do spec.
- Elemento preso à última palavra da frase aparece tarde demais e a cena fica vazia: ancore em palavras do começo ou do meio.
- Contador e boneco no mesmo lugar: posicione o contador ao lado, não embaixo.
- O GSAP apaga `transform`; o motor já posiciona os recortes com `top` e `height`. Não use `slide` sem a tupla `(dx, dy, instante)`.
- Recorte alto invadindo o título: o motor limita a 660 px de altura.

## Processo
- Nunca gere nada antes de a pessoa aprovar o roteiro de cenas.
- Mostre folhas de contato a cada etapa (quadros, recortes, clipes, quadros compostos); é aí que os erros aparecem.
- Mostre o custo antes de gerar em massa.
