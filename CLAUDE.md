# live-agentes

Loja de plugins do Claude Code com os agentes e skills da Live Idea. Leia o `README.md` antes de mexer.

- `plugins/live-geral/` guarda skills e agentes de todo o time. `plugins/live-<departamento>/` guarda skills de um só time.
- Skill nova parte de `_modelos/skill/`; agente novo parte de `_modelos/agente/`.
- Ao mexer num plugin: atualize a tabela do README dele e suba o `version` no `plugin.json`.
- Plugin novo precisa entrar também em `.claude-plugin/marketplace.json` e no `.github/CODEOWNERS`.
- Cada pasta de departamento é do time correspondente no GitHub (ver `.github/CODEOWNERS`). Não mexa na pasta de outro departamento sem pedido.
- Caminhos dentro das skills usam `${CLAUDE_PLUGIN_ROOT}`, nunca caminho do computador.
- Nada de chaves, tokens, dados pessoais ou valores de cliente.
- Textos em português, diretos, sem jargão.
