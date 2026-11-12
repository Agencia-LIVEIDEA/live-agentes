# live-agentes

Loja de plugins do Claude Code com os agentes e skills da LIVEIDEA. Leia o `README.md` antes de mexer.

- Este repositório guarda só a loja (`.claude-plugin/marketplace.json`), o plugin `plugins/live-geral/` (skills e agentes de todo o time) e os modelos em `_modelos/`.
- Cada departamento tem o seu repositório (`live-<departamento>`), com o plugin na pasta `agentes/` (`skills/` e `agents/`). A loja busca o plugin nessa pasta (fonte `git-subdir`). Nada de conteúdo de departamento aqui.
- RH e Financeiro são restritos ao próprio time e ao Martech.
- Skill nova parte de `_modelos/skill/`; agente novo parte de `_modelos/agente/`.
- Ao mexer num plugin: atualize as listas do README dele e suba o `version` no `plugin.json`.
- Plugin ou repositório de departamento novo precisa entrar também em `.claude-plugin/marketplace.json`.
- Os times só leem e abrem pull request; quem aprova é o Martech ou um dono da organização. Nada vai direto para o `main`.
- Caminhos dentro das skills usam `${CLAUDE_PLUGIN_ROOT}`, nunca caminho do computador.
- Nada de chaves, tokens, dados pessoais ou valores de cliente.
- O nome da agência é sempre LIVEIDEA, junto e em caixa alta.
- Textos em português, diretos, sem jargão.
