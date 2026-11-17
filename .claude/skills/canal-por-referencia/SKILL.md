---
name: canal-por-referencia
description: Cria vídeos de canal dark (sem rosto, narrados, ilustrados e animados) a partir de um vídeo de referência que a pessoa coloca na pasta referencia/. Faz a perícia da referência, monta a identidade do canal no tema que a pessoa escolher (personagens próprios, estilo, letreiro), escreve o roteiro com a narração pronta para gravar ou para voz de IA, transforma o áudio num roteiro de cenas para aprovação e produz o vídeo completo (quadros e recortes no Higgsfield, clipes no Higgsfield/Google Vids/Google Flow, animação em HTML com HyperFrames, montagem com ffmpeg, projeto no DaVinci Resolve, capas e descrição). Use quando a pessoa disser "analisa minha referência", "cria um canal igual a esse", "faz um vídeo no estilo da referência", "escreve o roteiro", "aqui está o áudio, faz o vídeo", "me dá ideias de vídeo", "faz a capa", ou rodar /canal-por-referencia.
---

# Canal por referência

Você vai ajudar a pessoa a montar e produzir um canal dark copiando o **processo** e a **linguagem visual** de um vídeo de referência, nunca o conteúdo dele. O tema, os personagens, os roteiros e as imagens são sempre **originais da pessoa**.

Fale sempre em português do Brasil, em linguagem simples. A produção é longa: mantenha a pessoa informada a cada etapa (quantos quadros prontos, quantos clipes, o que falta) e mostre folhas de contato para ela ver o resultado.

## Pastas do kit (raiz do projeto)

| Pasta | Para quê |
|---|---|
| `referencia/` | A pessoa coloca aqui o vídeo de referência (`.mp4`) ou um `link.txt` com o endereço do YouTube |
| `canal/` | A identidade do canal: `ficha-do-canal.md`, `estilo.json`, `personagens/` (folha de personagens) e `recortes/` (biblioteca de recortes que cresce a cada vídeo) |
| `modelos/` | Prompt mestre de roteiro, exemplos reais de roteiro de cenas, spec de animação, prompts de quadros, clipes e recortes |
| `ferramentas/scripts/` | Os scripts da produção (transcrição, cenas, motor de animação, montagem, revisão, DaVinci) |
| `ferramentas/assets/` | GSAP, fontes do letreiro e o papel de fundo |
| `ferramentas/hyperframes/` | Renderizador das animações (`npm install` uma vez) |
| `videos/NN-tema/` | Cada vídeo: roteiros, `work/` (produção), vídeo final, capas e descrição |

## As 5 fases (sempre nesta ordem, com as paradas de aprovação)

1. **Perícia da referência**: guia [01-pericia-referencia.md](guias/01-pericia-referencia.md). Resultado: `canal/ficha-do-canal.md` e `canal/estilo.json`. **Pare e mostre o resumo.**
2. **Identidade do canal no tema da pessoa**: guia [02-identidade-e-personagens.md](guias/02-identidade-e-personagens.md). Pergunte o tema (se a pessoa não disse), crie nome, fórmula, personagens próprios e a folha de personagens. **Pare e espere a aprovação da folha de personagens** antes de qualquer vídeo.
3. **Ideias e roteiro**: guia [03-roteiro.md](guias/03-roteiro.md). Dê 3 opções de vídeo (com pesquisa de outliers, se a pessoa quiser). Depois da escolha, escreva o roteiro e **entregue sempre, na mesma resposta, o texto narrado pronto para gravar ou para voz de IA** (bloco de código + `narracao-ia.txt`). A pessoa grava (ou gera a voz) e manda o áudio.
4. **Roteiro de cenas**: guia [04-roteiro-de-cenas.md](guias/04-roteiro-de-cenas.md). Transcreva o áudio, monte a tabela de cenas, escolha onde entram os clipes, calcule o custo. **Não gere nada antes de a pessoa aprovar.**
5. **Produção e entrega**: guias [05-producao-imagens-e-clipes.md](guias/05-producao-imagens-e-clipes.md), [06-animacao-html.md](guias/06-animacao-html.md) e [07-montagem-revisao-entrega.md](guias/07-montagem-revisao-entrega.md). Quadros → recortes → clipes → spec da animação → render → montagem → revisão em quadros compostos → capas → descrição → projeto do DaVinci.

Antes de qualquer fase, leia o [08-erros-conhecidos.md](guias/08-erros-conhecidos.md): ele lista os problemas que já custaram retrabalho e como evitar.

## Regras que valem sempre

- **Nunca copie** roteiro, falas, personagens, logotipo, capas, músicas ou trechos do vídeo de referência. Copie só o que é linguagem: ritmo, tipo de enquadramento, paleta, estilo de traço, tipo de animação, estrutura do roteiro e fórmula de título.
- **Personagens próprios e consistentes**: sempre gere quadros com a folha de personagens aprovada como referência e descreva a roupa de quem aparece. Se a pessoa reclamar que o traço mudou, volte para a folha original e reforce o traço no prompt.
- **Dados reais**: todo número ou estudo do roteiro precisa existir. Na dúvida, marque `[CONFIRMAR]` e avise a pessoa. Cite as fontes na descrição.
- **Custos**: antes de gerar em massa, mostre quanto vai custar (créditos por item × quantidade) e espere o ok no roteiro de cenas. Prefira ferramentas sem custo quando a qualidade é igual (Google Vids, imagens do Flow).
- **Temas sensíveis**: nada de ferimento, sangue ou criança em sofrimento nas imagens. Mostre o perigo com objetos, setas, sinais e diagramas.
- **Nunca digite senhas** nem faça login pela pessoa. Ela faz o login no Higgsfield, no Google Vids e no Flow; você usa as sessões abertas.
- **Publicar é da pessoa.** Você entrega o vídeo, as capas e a descrição; lembre de marcar "conteúdo alterado ou sintético" no YouTube.
- Guarde o que aprender sobre o canal (preferências, IDs da folha de personagens, regras novas) em `canal/ficha-do-canal.md`, para os próximos vídeos seguirem igual.

## Ferramentas que a produção usa

- **Higgsfield** (conector MCP): imagens `gpt_image_2_5` (quadros, recortes com fundo transparente, capas) e clipes `gemini_omni_flash_1_2` (image-to-video). Se o conector não aparecer na sessão, peça para a pessoa conectar em Configurações > Conectores e, se ainda assim não aparecer, para abrir uma sessão nova.
- **Google Vids** e **Google Flow** (pelo navegador Chrome com a extensão do Claude): clipes extras sem custo ou com créditos do plano.
- **Python 3** com `faster-whisper`, `numpy` e `Pillow`; **ffmpeg**; **Node.js** (para o HyperFrames). O [LEIA-ME](../../../LEIA-ME.md) da raiz explica a instalação.
