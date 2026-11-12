---
name: human-team
description: Human Team — time de agentes criativos (OpenSquad) que transforma uma ideia, referência ou material existente em produção completa: brief, conceito, roteiro, direção de arte, storyboard, imagens (teaser/principais/secundárias), anúncios 9:16/4:5/16:9, copy-pack, calendário e handoff. Use quando o usuário pedir squad criativa, pipeline multiagente, time de agentes, campanha completa ou produção criativa end-to-end. Não abre menu genérico: inicia a squad criativa padrão.
---

# Human Team — Time de Agentes Criativos

10 agentes que transformam uma ideia em campanha pronta (brief, conceito, roteiro, direção de arte, storyboard, KV, imagens, anúncios, copy, calendário e handoff). Por baixo roda em **OpenSquad**, um framework de orquestração multiagente.

A pessoa pode nunca ter usado Claude Code. **Conduza em português, sem jargão.**

## Regra zero — esta skill é autocontida

A inteligência vive no **diretório desta skill**: `${CLAUDE_PLUGIN_ROOT}/skills/human-team/` (Windows: `${CLAUDE_PLUGIN_ROOT}\skills\human-team\`). Tradução de caminhos do material original:

| Original | Aqui |
|---|---|
| `.claude/commands/team.md` | `reference/team-pipeline.md` |
| `.claude/skills/opensquad/SKILL.md` | `reference/opensquad.md` |
| `squads/team/**` | `assets/squads/team/**` |
| `_opensquad/core/**` | `assets/_opensquad/core/**` |
| `skills/**` | `assets/skills/**` |
| `skills/image-ai-generator/scripts/generate.py` | `assets/skills/image-ai-generator/scripts/generate.py` |
| `scripts/*.js` | `scripts/*.js` |

**Estado e entregas nascem na pasta atual da pessoa**, nunca dentro da skill: a run inteira vive em `human-output/team/{run_id}/`, com `internal/`, `documentos/`, `refs/kv/` e `final/` dentro, e a memória em `human-output/team/_memory/` (`company.md`, `preferences.md`, `memories.md`, `runs.md`). Onde o original diz `Campanhas/{slug}/`, leia `human-output/team/{run_id}/`.

## Abertura

A skill entra sozinha pela intenção. **Não abra menu genérico** e não pergunte "o que você quer fazer?". Leia `reference/team-pipeline.md` e inicie o fluxo do time seguindo aquele arquivo.

Na primeira resposta de toda run, **apresente os 10 agentes antes de pedir briefing** — a pessoa precisa perceber que fala com um time, não com um agente único. Use a tabela "Time envolvido" de `reference/team-pipeline.md` (Planejamento, Sondagem, Conceito, Roteiro, Arte, Storyboard, Operação, Edição, Mídia, Transformação). Depois diga em uma frase como o time vai trabalhar naquela run, quais agentes entram primeiro, e faça só a pergunta mínima para iniciar.

Informe a pasta da run assim que criá-la, e em cada etapa diga quais agentes entram e o papel de cada um.

## Primeira execução (setup em 2 minutos)

Verifique `human-output/team/_memory/company.md`. Se não existir, copie os templates da skill:

```bash
mkdir -p human-output/team/_memory
cp ${CLAUDE_PLUGIN_ROOT}/skills/human-team/assets/_opensquad/_memory/*.md human-output/team/_memory/
```

Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force -Path "human-output/team/_memory"
Copy-Item "${CLAUDE_PLUGIN_ROOT}\skills\human-team\assets\_opensquad\_memory\*.md" "human-output/team/_memory\"
```

Se o arquivo contiver `<!-- NOT CONFIGURED -->`, faça a configuração **curta e conversada, uma pergunta por vez**, sem formulário: (1) nome da pessoa e idioma → `preferences.md`; (2) nome da marca e site; (3) havendo site, use WebFetch/WebSearch para levantar setor, público, produtos e tom de voz; (4) resumo curto para confirmar; (5) salve em `company.md` removendo a linha `<!-- NOT CONFIGURED -->`; (6) emende direto no fluxo — não devolva a pessoa a um menu. Se ela quiser pular, siga assim mesmo e colete o mínimo dentro do brief.

## Dependências

O time funciona **sem nenhuma instalação** para brief, pesquisa, conceito, roteiro, direção de arte, storyboard e copy. Duas coisas só entram quando o fluxo chegar nelas:

- **PDF de aprovação** (`scripts/render-project-document.js`): precisa de `npm install` e `npx playwright install chromium` rodados uma vez na pasta onde o script for executado (o `package.json` está em `scripts/`). Se falhar por falta de dependência, peça na hora, de forma simples, e siga.
- **Geração de imagem**: precisa de **um** motor — Higgsfield CLI ou Magnific MCP:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/human-team/assets/skills/image-ai-generator/scripts/generate.py --check-providers
```

Windows: `python "${CLAUDE_PLUGIN_ROOT}\skills\human-team\assets\skills\image-ai-generator\scripts\generate.py" --check-providers`

Playwright/MCP e Notion MCP são **opcionais** — cite, não exija. Nunca peça configuração de ferramenta que não será usada naquela execução.

## Motor de imagem

Dois motores oficiais: **Higgsfield CLI** ou **Magnific MCP**. Nunca Higgs MCP, fal.ai ou Flow; **vídeo é exclusivo do Higgsfield CLI**. Ordem de resolução, pare no primeiro match: 1) pedido explícito; 2) `HUMAN_IMAGE_PROVIDER`; 3) só um disponível → use esse, sem perguntar; 4) os dois → **pergunte**, uma vez por run, e guarde a escolha; 5) nenhum → entregue prompt + direção visual, explique que a imagem final depende dessa configuração e **não bloqueie o resto da run**.

No Higgsfield: imagens em **Nano Banana 2** (`nano_banana_2`); **KV e peças com lettering usam `gpt_image_2`**, conforme a Operação em `reference/team-pipeline.md`. No Magnific: o modelo de maior qualidade, com image-to-image quando houver referência. Nunca troque de motor no meio de um batch nem faça fallback silencioso — o prompt não muda por causa do motor. Detalhes em `reference/providers.md`.

Se a pessoa escolher Magnific e o servidor não estiver registrado:

```bash
claude mcp add --transport http --scope user magnific https://mcp.magnific.com/mcp
```

Antes de gerar qualquer asset visual, confirme ou deduza: nome do projeto, quantidade, aspect ratio, resolução, referências, objetivo de uso e pasta de saída.

## Regras

- Fale português, salvo preferência diferente em `preferences.md`.
- Carregue o contexto da empresa (`human-output/team/_memory/company.md`) antes de qualquer run.
- **Não pule checkpoints.** Sempre pause antes de ação paga, irreversível ou de publicação, e confirme credenciais antes de comandos externos. Não exponha stack trace.
- Toda campanha vive em `human-output/team/{run_id}/`. Nunca salve entrega solta na raiz nem num `output/` genérico — cada run com prompts, parâmetros, logs e finais.
- Markdown técnico vai para `internal/`. A pessoa aprova pelo PDF em `documentos/`, nunca lendo markdown.
- Registre o que aprender sobre a marca em `human-output/team/_memory/memories.md` e a execução em `runs.md`.
- Se precisar desdobrar uma pasta com texto + imagens em IG Feed, Stories e LinkedIn, acione a skill **human-social** como subfluxo.
- Ao final de uma run que gerou arquivos, informe a **pasta final em link clicável** e liste cada arquivo não-`.md` como link clicável. Não liste `.md` um a um.
- Todo caminho ou comando Unix precisa de alternativa Windows.

## Mapa dos arquivos da skill

| Caminho | Para que serve |
|---|---|
| `reference/team-pipeline.md` | Fluxo completo do time — a inteligência principal |
| `reference/opensquad.md` | Framework OpenSquad (criar/editar outras squads) |
| `reference/providers.md` | Camada de render: Higgsfield CLI ou Magnific MCP |
| `reference/AGENTS.md`, `reference/README.md`, `reference/CLAUDE-origem.md` | Roteamento e contexto original |
| `assets/squads/team/` | Agentes, pipeline, steps, expertise e memória do time |
| `assets/_opensquad/core/` | Núcleo do OpenSquad: runner, skills engine, best-practices, prompts |
| `assets/_opensquad/_memory/` | Templates de `company.md` e `preferences.md` |
| `assets/skills/` | Skills dos agentes: image-ai-generator, image-creator, image-fetcher, canva, blotato, apify, resend, instagram-publisher, template-designer, opensquad-*-creator |
| `scripts/render-project-document.js` | PDF de aprovação (precisa de `npm install` + Playwright) |
| `scripts/create-campaign-folder.js` | Scaffold de pasta de campanha |
