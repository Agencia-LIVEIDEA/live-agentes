# live-agentes

Agentes de IA e skills da LIVEIDEA para o Claude. Mantido pelo time de Martech.

O repositório é uma **loja de plugins** do Claude Code. Cada pessoa instala o plugin geral e o do seu departamento.

Quase todos os plugins moram aqui, em `plugins/`. Os de **RH** e **Financeiro** moram em repositórios privados próprios, que só o time de cada um consegue ver. A loja aponta para eles, e quem não tem acesso não consegue instalar.

## Plugins

| Plugin | Para quem | O que traz |
| --- | --- | --- |
| `live-geral` | Todo o time | Skills e agentes gerais. Hoje: `memoria-projeto`. |
| `live-atendimento` | Atendimento | A criar |
| `live-producao` | Produção | A criar |
| `live-financeiro` | Financeiro | A criar. Repositório privado `live-agentes-financeiro` |
| `live-planejamento` | Planejamento | A criar |
| `live-criacao` | Criação | `human-image`, `human-motion`, `human-cinematic`, `human-carrossel`, `human-social`, `human-dna`, `human-team` |
| `live-marketing` | Marketing | A criar |
| `live-rh` | RH | A criar. Repositório privado `live-agentes-rh` |
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
    └── live-<departamento>/            ← um por departamento (menos RH e Financeiro)
        ├── .claude-plugin/plugin.json
        ├── README.md
        └── skills/<skill>/SKILL.md

live-agentes-rh/           ← repositório privado, só RH e Martech
live-agentes-financeiro/   ← repositório privado, só Financeiro e Martech
├── .claude-plugin/plugin.json    ← o plugin fica na raiz
└── skills/<skill>/SKILL.md
```

## Onde colocar cada coisa

- **Skill geral** (serve a qualquer departamento): `plugins/live-geral/skills/`.
- **Agente**: `plugins/live-geral/agents/`. Agentes são todos gerais por enquanto.
- **Skill de departamento** (só faz sentido para um time): `plugins/live-<departamento>/skills/`. Para RH e Financeiro, `skills/` no repositório privado de cada um.
- Na dúvida entre geral e departamento, comece no departamento. Quando outro time pedir, ela sobe para o geral.

## Quem vê e quem aprova

| Quem | O que pode fazer |
| --- | --- |
| Times de departamento | Ver o repositório e propor mudanças por pull request |
| Martech | Revisar e aprovar os pull requests |
| Donos da organização | Aprovar e fazer merge também |

Ninguém altera o `main` direto: toda mudança entra por pull request aprovado pelo Martech ou por um dono da organização. A regra está em `.github/CODEOWNERS`.

Todo mundo com acesso a este repositório vê todas as pastas. Por isso RH e Financeiro ficam fora daqui, em repositórios privados com as mesmas regras: só o próprio time vê, só Martech e donos aprovam. Se outro departamento precisar esconder o conteúdo, ele ganha um repositório próprio do mesmo jeito.

Mesmo para RH e Financeiro, o nome e a descrição do plugin aparecem na loja para todo mundo. A descrição em `marketplace.json` não pode revelar nada sensível.

## Como contribuir

Como os times só têm leitura, a mudança sai de uma cópia sua do repositório (fork):

1. No GitHub, clique em **Fork** no repositório e clone o seu fork fora do OneDrive (ex.: `C:/dev/liveidea/`).
2. Copie o modelo (`_modelos/skill/` ou `_modelos/agente/`) para o lugar certo e renomeie. O nome da pasta da skill é igual ao `name` do SKILL.md, em `kebab-case` minúsculo, sem acento.
3. Atualize a tabela de skills no `README.md` do plugin.
4. Suba o `version` no `plugin.json` do plugin (0.1.0 → 0.2.0 para skill nova, 0.1.0 → 0.1.1 para ajuste).
5. Valide: `claude plugin validate .`
6. Envie para o seu fork e abra um pull request para o `main` deste repositório. O Martech revisa e aprova.

Se você não tem familiaridade com git, mande a skill para o Martech, que ele abre o pull request por você.

Regras:

- Dentro de uma skill, nunca use caminho fixo do seu computador (`~/.claude/skills/...`). Use `${CLAUDE_PLUGIN_ROOT}/skills/<nome>/...`.
- Nunca coloque chaves de API, tokens, senhas, dados pessoais ou valores de cliente nos arquivos.
- Fontes e materiais licenciados não entram no repositório.
- Saídas geradas pelas skills ficam na pasta do projeto de quem usa, nunca aqui.

## Configuração no GitHub (uma vez, feita por um dono da organização)

1. **Permissão base da organização** (**Settings → Member privileges → Base permissions**): **No permission**. Se estiver em **Read**, todo membro vê todos os repositórios privados, inclusive os de RH e Financeiro.
2. **Fork de repositório privado** (**Settings → Member privileges → Repository forking**): ligado. Sem isso, quem só tem leitura não consegue propor mudanças. Ligue também em **Settings → General → Allow forking** de cada repositório.
3. **Acesso aos repositórios** (**Settings → Collaborators and teams**):
   - `live-agentes`: os 8 times com **Read**; Martech com **Maintain**.
   - `live-agentes-rh`: só o time RH com **Read**; Martech com **Maintain**.
   - `live-agentes-financeiro`: só o time Financeiro com **Read**; Martech com **Maintain**.
4. **Proteção do `main`** (**Settings → Rules → New branch ruleset**), em cada repositório:
   - exigir pull request com 1 aprovação;
   - exigir aprovação de **Code Owners**;
   - bloquear push direto e force push;
   - em **Bypass list**, adicionar **Organization admin**, para que os donos da organização também possam aprovar e fazer merge.
5. Confira se `@Agencia-LIVEIDEA/martech` em `.github/CODEOWNERS` é o slug do time Martech (URL `github.com/orgs/Agencia-LIVEIDEA/teams/<slug>`). O GitHub avisa no próprio arquivo se o nome não existir.

Exigir aprovação de Code Owners em repositório privado depende do plano GitHub Team (ou superior) da organização.

## Pendências

- [ ] Licença das skills `human-*` para uso pelo time todo.
- [ ] Primeira skill de cada departamento.
