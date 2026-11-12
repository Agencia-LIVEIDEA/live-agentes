# live-agentes

Agentes de IA e skills da Live Idea para o Claude. Mantido pelo time de Martech.

O repositório é uma **loja de plugins** do Claude Code. Cada pessoa instala o plugin geral e o do seu departamento.

## Plugins

| Plugin | Para quem | O que traz |
| --- | --- | --- |
| `live-geral` | Todo o time | Skills e agentes gerais. Hoje: `memoria-projeto`. |
| `live-atendimento` | Atendimento | A criar |
| `live-producao` | Produção | A criar |
| `live-financeiro` | Financeiro | A criar |
| `live-planejamento` | Planejamento | A criar |
| `live-criacao` | Criação | `human-image`, `human-motion`, `human-cinematic`, `human-carrossel`, `human-social`, `human-dna`, `human-team` |
| `live-marketing` | Marketing | A criar |
| `live-rh` | RH | A criar |
| `live-martech` | Martech | A criar |

## Como instalar (Claude Code)

Uma vez por computador. Você precisa ter acesso à organização `Agencia-LIVEIDEA` no GitHub.

1. Adicione a loja:

   ```bash
   claude plugin marketplace add Agencia-LIVEIDEA/live-agentes
   ```

2. Instale o plugin geral e o do seu departamento (troque `live-criacao` pelo seu):

   ```bash
   claude plugin install live-geral@live-agentes
   claude plugin install live-criacao@live-agentes
   ```

3. Para a skill `memoria-projeto`, clone também a memória, fora do OneDrive:

   ```bash
   git clone https://github.com/Agencia-LIVEIDEA/live-memoria.git C:/dev/liveidea/live-memoria
   ```

As skills aparecem como `/live-geral:memoria-projeto`, `/live-criacao:human-image` etc. Elas também entram sozinhas quando o pedido combina com a descrição.

Para receber as novidades: `claude plugin marketplace update live-agentes`.

## Estrutura

```
live-agentes/
├── .claude-plugin/marketplace.json     ← lista os plugins da loja
├── .github/CODEOWNERS                  ← qual time aprova mudanças em cada pasta
├── _modelos/                           ← ponto de partida para skill e agente novos
│   ├── skill/SKILL.md
│   └── agente/nome-do-agente.md
└── plugins/
    ├── live-geral/                     ← todo o time
    │   ├── .claude-plugin/plugin.json
    │   ├── skills/<skill>/SKILL.md
    │   └── agents/<agente>.md
    └── live-<departamento>/            ← um por departamento
        ├── .claude-plugin/plugin.json
        ├── README.md
        └── skills/<skill>/SKILL.md
```

## Onde colocar cada coisa

- **Skill geral** (serve a qualquer departamento): `plugins/live-geral/skills/`.
- **Agente**: `plugins/live-geral/agents/`. Agentes são todos gerais por enquanto.
- **Skill de departamento** (só faz sentido para um time): `plugins/live-<departamento>/skills/`.
- Na dúvida entre geral e departamento, comece no departamento. Quando outro time pedir, ela sobe para o geral.

## Quem cuida de cada pasta

Cada time da organização no GitHub é dono da pasta do seu departamento. O dono revisa e aprova tudo que muda ali. A regra está em `.github/CODEOWNERS`.

| Pasta | Time dono |
| --- | --- |
| `plugins/live-geral/`, `_modelos/`, `.claude-plugin/`, raiz | Martech |
| `plugins/live-atendimento/` | Atendimento |
| `plugins/live-producao/` | Produção |
| `plugins/live-financeiro/` | Financeiro |
| `plugins/live-planejamento/` | Planejamento |
| `plugins/live-criacao/` | Criação |
| `plugins/live-marketing/` | Marketing |
| `plugins/live-rh/` | RH |
| `plugins/live-martech/` | Martech |

Isso controla **quem aprova**, não quem enxerga: todo mundo com acesso ao repositório lê todas as pastas, e qualquer pessoa pode instalar qualquer plugin. Skill com informação que um time não pode ver não entra aqui.

## Como contribuir

1. Copie o modelo (`_modelos/skill/` ou `_modelos/agente/`) para o lugar certo e renomeie. O nome da pasta da skill é igual ao `name` do SKILL.md, em `kebab-case` minúsculo, sem acento.
2. Atualize a tabela de skills no `README.md` do plugin.
3. Suba o `version` no `plugin.json` do plugin (0.1.0 → 0.2.0 para skill nova, 0.1.0 → 0.1.1 para ajuste).
4. Valide: `claude plugin validate .`
5. Abra um pull request. O time dono da pasta revisa e aprova. Plugin novo ou mudança na lista da loja também passa pelo Martech.

Regras:

- Dentro de uma skill, nunca use caminho fixo do seu computador (`~/.claude/skills/...`). Use `${CLAUDE_PLUGIN_ROOT}/skills/<nome>/...`.
- Nunca coloque chaves de API, tokens, senhas, dados pessoais ou valores de cliente nos arquivos.
- Fontes e materiais licenciados não entram no repositório.
- Saídas geradas pelas skills ficam na pasta do projeto de quem usa, nunca aqui.

## Configuração no GitHub (uma vez, feita por um admin da organização)

1. Em **Settings → Collaborators and teams** do repositório, dê aos 8 times o papel **Write**. Sem isso eles não conseguem abrir pull request a partir de um branch do repositório.
2. Em **Settings → Rules** (ou **Branches**), proteja o `main`: exigir pull request, exigir aprovação de **Code Owners** e bloquear push direto.
3. Confira se os nomes dos times em `.github/CODEOWNERS` batem com o slug de cada time (URL `github.com/orgs/Agencia-LIVEIDEA/teams/<slug>`). Times com acento, como Produção e Criação, podem ter slug diferente. O GitHub avisa no próprio arquivo se algum nome não existir.

Exigir aprovação de Code Owners em repositório privado depende do plano GitHub Team (ou superior) da organização.

## Pendências

- [ ] Licença das skills `human-*` para uso pelo time todo.
- [ ] Primeira skill de cada departamento.
