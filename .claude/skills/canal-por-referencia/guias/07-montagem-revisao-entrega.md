# Fase 5c: montagem, revisão, capas e entrega

## 1. Montagem
```bash
python base_papel.py --only-base      # base.mp4: papel + quadros/clipes na moldura (pode rodar enquanto os blocos renderizam)
python base_papel.py                  # base + camada HTML + voz -> ../tema-final.mp4 (só depois de todos os blocos)
```
- A voz é normalizada a **-14 LUFS**; sem música (a não ser que a ficha do canal diga outra coisa).
- Cena com clipe usa `clips/NNN.mp4` (cortado ou estendido no último quadro); cena sem clipe usa `hf/panels/NNN.jpg` com zoom leve.
- Conferir: `ffprobe` (1920x1080, duração ≈ áudio + 3 s) e `ffmpeg -i final.mp4 -af loudnorm=print_format=summary -f null -` (Integrated perto de -14).

## 2. Revisão
Faça folhas com `check_frames.py` cobrindo todos os blocos (o guia 06 diz o que procurar), corrija e renderize de novo só o necessário. Só entregue depois disso.

## 3. Projeto no DaVinci Resolve (gratuito)
```bash
python make_manifest.py               # grava ~/.canal-por-referencia/manifest_atual.json
```
Na primeira vez, a pessoa copia `ferramentas/scripts/montar_resolve_davinci.py` para a pasta de scripts do Resolve (no Windows: `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\`) com o nome `Canal - Montar video.py`. Depois é só abrir o Resolve e clicar em **Workspace > Scripts > Canal - Montar video**. O script monta V1 fundo, V2 animações (sequências PNG por bloco) e A1 voz.

## 4. Capas
- Higgsfield `gpt_image_2_5`, `quality: high`, `resolution: 2k`, `16:9`. Referências: a folha de personagens e uma capa anterior do canal (se houver).
- Fórmula que funcionou: personagem grande de um lado, texto gigante do outro, **pergunta + ordem** (ex.: "PRENDEU O PÉ?" em branco + "NÃO PUXE!" em amarelo), X vermelho e/ou check verde, alto contraste, fonte arredondada com contorno preto grosso.
- Faça 2 versões (para o teste A/B do YouTube), mostre lado a lado e salve como `capa.jpg` e `capa-alternativa.jpg` (1920x1080).

## 5. Descrição e entrega
`videos/NN-tema/descricao-youtube.md` com: título recomendado + 2 alternativas, descrição de 3 a 4 frases, **capítulos nos tempos reais** (do `scenes.json`), números de emergência ou links úteis do tema, chamada para compartilhar e se inscrever, fontes, aviso de que o vídeo é informativo, hashtags, 15 tags e o lembrete "marque **Conteúdo alterado ou sintético**".

Entregue para a pessoa: o vídeo final, as duas capas e a descrição (envie os arquivos), o caminho do projeto do DaVinci e a lista do que ela precisa conferir (os `[CONFIRMAR]` do roteiro). Copie os recortes novos para `canal/recortes/` e atualize a ficha do canal (tema feito, aprendizados).
