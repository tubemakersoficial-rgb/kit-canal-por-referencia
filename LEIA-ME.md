# Kit: canal dark por referência

Este kit ensina o Claude Code a montar e produzir um canal dark (vídeos sem rosto, narrados, ilustrados e animados) **a partir de um vídeo de referência que você escolhe**. Você coloca o vídeo na pasta `referencia/`, diz o tema do seu canal, e o Claude:

1. faz a perícia da referência: ritmo, enquadramento, cores, traço, tipo de animação, estrutura do roteiro e fórmula de título;
2. cria a identidade do **seu** canal: nome, fórmula, personagens próprios e folha de personagens;
3. dá ideias de vídeo e escreve o roteiro com o texto pronto para você gravar ou gerar com voz de IA;
4. transforma o seu áudio num roteiro de cenas para você aprovar;
5. produz o vídeo inteiro: quadros, recortes, clipes animados, animação em HTML, montagem, revisão, capas, descrição e projeto no DaVinci Resolve.

O processo é o mesmo usado num canal real de cerca de 10 vídeos de 10 minutos. Copiamos só a **linguagem** da referência, nunca o conteúdo: o roteiro, os personagens e as imagens são originais seus.

## O que você precisa

| Ferramenta | Para quê | Custo |
|---|---|---|
| [Claude Code](https://claude.com/claude-code) (app desktop ou terminal) | Faz tudo | Plano do Claude |
| Conector **Higgsfield** no Claude | Quadros, recortes, capas e clipes Omni | Créditos do Higgsfield (~700 por vídeo de 10 min com 20 clipes) |
| **Google Vids** / **Google Flow** + Chrome com a extensão Claude in Chrome | Clipes extras | Dentro do plano Google (opcional) |
| Python 3.10+ | Scripts | Grátis |
| ffmpeg | Montagem | Grátis |
| Node.js 18+ | Render das animações (HyperFrames) | Grátis |
| DaVinci Resolve (opcional) | Ajustes finais na linha do tempo | Grátis |

## Instalação (uma vez)

1. Baixe esta pasta (ou `git clone` deste repositório).
2. Instale o Python e rode:
   ```bash
   pip install faster-whisper numpy Pillow
   ```
3. Instale o ffmpeg. No Windows:
   ```bash
   winget install Gyan.FFmpeg
   ```
4. Instale o Node.js e, dentro da pasta do kit:
   ```bash
   cd ferramentas/hyperframes
   npm install
   ```
5. No Claude, conecte o **Higgsfield** em Configurações > Conectores.

Se preferir, abra o Claude Code na pasta do kit e diga "instala tudo o que o kit precisa". Ele confere cada ferramenta e diz o que falta.

## Como usar

1. Coloque o vídeo de referência em `referencia/` (um `.mp4`) ou escreva o link do YouTube em `referencia/link.txt`.
2. Abra o Claude Code **nesta pasta** e diga:
   > Analisa minha referência. Meu canal vai ser sobre **[seu tema]**.
3. Siga as paradas de aprovação. O Claude sempre espera o seu "ok" antes de gastar créditos:
   - resumo da perícia;
   - folha de personagens;
   - escolha da ideia;
   - roteiro (com o texto para narrar);
   - roteiro de cenas, com o custo;
   - vídeo final.
4. Para cada vídeo novo:
   > Me dá 3 ideias de vídeo.

   Depois, quando tiver gravado:
   > Aqui está o áudio do vídeo 02: `C:/caminho/audio.wav`

## Pastas

```
referencia/        o vídeo (ou link) de referência
canal/             ficha-do-canal.md, estilo.json, personagens/, recortes/ (cresce a cada vídeo)
modelos/           prompt mestre de roteiro e exemplos reais (roteiro de cenas, spec, prompts)
ferramentas/       scripts, assets (GSAP, fontes, papel) e o renderizador HyperFrames
videos/NN-tema/    cada vídeo: roteiros, work/ (produção), vídeo final, capas e descrição
.claude/skills/    a skill "canal-por-referencia" com os 8 guias do processo
```

## Avisos

- **Direitos autorais:** use a referência para estudar o estilo. Não reaproveite trechos, falas, personagens, músicas nem capas dela.
- **Conteúdo sintético:** ao publicar, marque "Conteúdo alterado ou sintético" no YouTube.
- **Fatos:** o Claude confere os dados na web e marca `[CONFIRMAR]` o que não conseguiu confirmar. Revise antes de gravar.
- **Contas:** o Claude nunca digita senhas. Você faz o login no Higgsfield, no Google e no YouTube.
- **Publicar é com você.** O Claude entrega o vídeo, as capas e a descrição, mas não publica.

## Créditos

Fontes: Chewy e Baloo 2 (Google Fonts, licença SIL Open Font License). Animação: GSAP. Render: HyperFrames.
