# Canal por referência

Responda sempre em português do Brasil, em linguagem simples.

Este projeto produz vídeos de um canal dark a partir de um vídeo de referência. **Use sempre a skill `canal-por-referencia`** (`.claude/skills/canal-por-referencia/SKILL.md`) e os guias dela, na ordem das 5 fases e com as paradas de aprovação.

- A referência fica em `referencia/`. A identidade do canal fica em `canal/ficha-do-canal.md` e `canal/estilo.json`. Leia os dois antes de qualquer vídeo.
- Se `canal/ficha-do-canal.md` ainda estiver em branco, comece pela Fase 1 (perícia da referência).
- Cada vídeo fica em `videos/NN-tema/`. Crie a pasta com `python ferramentas/scripts/novo_video.py NN-tema [audio]`.
- Sempre que escrever um roteiro, entregue na mesma resposta o texto narrado pronto para narração com IA (bloco de código) e salve em `videos/NN-tema/narracao-ia.txt`.
- Nunca gere imagens ou clipes antes de a pessoa aprovar o roteiro de cenas com o custo.
- Guarde em `canal/ficha-do-canal.md` tudo o que a pessoa decidir ou corrigir (IDs da folha de personagens, preferências, temas feitos).
