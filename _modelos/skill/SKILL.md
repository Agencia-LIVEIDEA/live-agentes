---
name: nome-da-skill
description: O que a skill faz, em uma ou duas frases, e QUANDO usar. Liste as frases que a pessoa costuma dizer ("monta o cronograma", "faz a ata dessa reunião"). É por esta descrição que o Claude decide sozinho quando entrar, então seja específico.
---

# Nome da skill

Uma linha sobre o que esta skill entrega. Fale sempre em português.

## Antes de começar

- O que perguntar à pessoa, se faltar (uma pergunta por vez).
- O que ler antes (arquivos do projeto, memória do job via `memoria-projeto`).

## Passo a passo

1. ...
2. ...
3. ...

## Entrega

- Formato (Markdown, PowerPoint, planilha, texto para colar).
- Onde salvar (dentro da pasta do projeto de quem está usando, nunca dentro do plugin).

## Regras

- Nunca invente dado de cliente, valor ou prazo: pergunte.
- Arquivos de apoio desta skill: `${CLAUDE_PLUGIN_ROOT}/skills/nome-da-skill/reference/...` (nunca um caminho fixo do seu computador).
