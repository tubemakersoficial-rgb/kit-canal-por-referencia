# Fase 5a: quadros, recortes e clipes

Trabalhe na pasta `videos/NN-tema/work`. Use `jobs.py` para guardar todo job id (`python jobs.py panel 1:<id> 3:<id> ...`, `python jobs.py omni ...`, `python jobs.py cut ...`) e não perder nada se a sessão cair.

## 1. Quadros com personagem (Higgsfield)
- Modelo `gpt_image_2_5`, `quality: medium`, `resolution: 1k`, `aspect_ratio: 16:9`, `medias: [{value: <job id da folha de personagens>, role: image_references}]`.
- Gere em lotes de 12 com `generate_image_batch` e espere com `jobs_wait` (até 12 por chamada). Um lote leva ~1 minuto.
- Prompt (veja `modelos/exemplo-quadros.py`): **cena** (quem faz o quê, onde, com a roupa de cada personagem) + **sufixo de estilo** fixo do canal ("no MESMO traço da referência: cabeça grande e redonda, olhos de pontinho, braços e pernas de PALITO…; cenário simples, cores suaves; desenhe SOMENTE os personagens citados; sem texto, sem letras, sem números, sem moldura").
- Cena de ambiente (para clipe do Vids): troque o sufixo por "SEM personagens, sem pessoas".
- Cena de noite: "tons azul-escuros suaves, iluminação quente só onde há lanterna ou chama".
- Baixe pelo `result_url` (ou `HF_URL_BASE=... python dlp.py panel panels_raw png 1=HHMMSS ...`, que tenta os segundos vizinhos) para `panels_raw/NNN.png`. Converta para `hf/panels/NNN.jpg` (`ffmpeg -i panels_raw/NNN.png -q:v 3 hf/panels/NNN.jpg`).
- **Revise numa folha de contato** (`python grid.py panels_raw folha.jpg 6 320`) e leia a imagem. Refaça o que fugiu do traço, tem texto escrito, mostra ferimento ou tem personagem a mais.

## 2. Recortes ilustrados (Higgsfield)
- Liste os nomes usados no spec que ainda não existem em `hf/cut/` e gere só esses.
- Mesmo modelo, `aspect_ratio: 1:1` (ou `16:9` para objetos compridos), `background: transparent`, referência de estilo = um recorte aprovado do canal (suba com `media_upload` → `curl -X PUT` → `media_confirm`). Para recorte de personagem, use a folha de personagens como referência.
- Prompt: "[objeto com detalhes]. Ilustração isolada em lápis de cor e aquarela, mesmo traço da referência, contorno fino azul-escuro. Inteiro, centralizado, FUNDO TRANSPARENTE, sem texto."
- Corte as bordas transparentes antes de usar (o `dlcut` do exemplo faz `getbbox` no canal alfa com margem de 12 px) e salve em `hf/cut/<nome>.png`. Depois copie os aprovados para `canal/recortes/`.

## 3. Clipes Omni no Higgsfield (cenas com personagens)
- `generate_video_batch` com `model: gemini_omni_flash_1_2`, **`mode: "image-to-video"`** (obrigatório), `resolution: "720p"`, `duration: 15` (ou 10), `aspect_ratio: "16:9"`, `medias: [{value: <job id do quadro>, role: "start_image"}]`. Lotes de até 12.
- Prompt em inglês, descrevendo um movimento simples + sufixo: "Keep the exact hand-drawn colored-pencil and watercolor style of the image, the same characters…, camera almost still, gentle natural motion, no text, no new characters." Veja `modelos/exemplo-clipes.py`.
- Antes de gerar, confira o custo com `generate_video` + `get_cost: true`.
- Se um clipe voltar como `nsfw` (o filtro é sensível a faíscas, fogo e alguém em perigo), refaça com um prompt mais calmo, sem o elemento de perigo. Se recusar de novo, a cena fica com o quadro parado.
- Baixe para `clips/NNN.mp4`.

## 4. Clipes no Google Vids (cenas de ambiente; sem custo extra)
Pelo Chrome com a extensão do Claude, na conta Google da pessoa (ela faz o login):
1. vids.google.com → **Vídeo em branco** → ícone **Clipe de vídeo gerado com IA** (no topo da barra lateral direita) → aba **Animar** (já vem em Omni, 720p, 10 s).
2. O botão "Adicionar imagem" abre o seletor do Drive. Para enviar do computador, rode antes no console da página o ajuste que "prende" o campo de arquivo:
   ```js
   const oc=HTMLInputElement.prototype.click;HTMLInputElement.prototype.click=function(){if(this.type==='file'){if(!this.isConnected){this.style.display='none';document.body.appendChild(this);}window.__fi=this;return;}return oc.call(this)};HTMLInputElement.prototype.showPicker=function(){if(this.type==='file'){if(!this.isConnected)document.body.appendChild(this);window.__fi=this;return;}};
   ```
   Depois use `find` ("file-input in Animar panel") e `file_upload` com o JPG do quadro (`vids_in/vNNN.jpg`).
3. Clique no campo de texto, digite o movimento (em português funciona; termine com "Mantém o estilo desenhado…, sem pessoas, sem texto"), clique em enviar, expanda o painel (seta ao lado das abas) e clique em **Limpar** para o campo de arquivo voltar. Repita. Dá para enfileirar 20 ou mais.
4. Para baixar: quando todos estiverem em 100%, rode na página
   ```js
   const vs=[...document.querySelectorAll('video')]; for (let k=0;k<vs.length;k++){ const b=await (await fetch(vs[k].currentSrc,{credentials:'include'})).blob(); const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download='vids_'+k+'.mp4'; document.body.appendChild(a); a.click(); a.remove(); await new Promise(r=>setTimeout(r,800)); }
   ```
   (sem `credentials:'include'` dá erro de CORS). Os arquivos caem em Downloads.
5. **Ligue cada clipe à cena comparando o primeiro quadro** com os JPGs enviados (diferença média de pixels em 64x36 em tons de cinza; o menor valor ganha). Copie para `clips/NNN.mp4`.
- O Vids põe uma pequena marca (✦) no canto. Tudo bem dentro da moldura.

## 5. Clipes no Google Flow (créditos do plano)
- flow.google.com, modelo de vídeo Omni Flash, modo Frames, 720p, 10 s (15 créditos cada). Envie o quadro como frame inicial pelo "Enviar mídia" (nomes únicos), clique de verdade no chip "Início" e baixe pelo menu (720p). Use para cenas extras quando sobrar crédito.
- As **imagens** do Flow (Nano Banana) não gastam crédito: é uma alternativa para os quadros se o Higgsfield estiver fora, mas o traço pode variar.

## 6. Conferir os clipes
Tire um quadro de cada clipe aos 3,5 s e monte uma folha de contato. Veja se o estilo e os personagens se mantiveram. Atualize `clipes` no `projeto.json` com **todas** as cenas que têm clipe.
