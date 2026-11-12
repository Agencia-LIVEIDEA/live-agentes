# live-agentes

Agentes de IA e skills da LIVEIDEA para o Claude. Mantido pelo time de Martech.

Este repositório é a **loja de plugins** do Claude Code da agência. Ele guarda a lista de plugins, o plugin `live-geral` (para todo o time) e os modelos de skill e agente. Cada departamento tem **o seu próprio repositório**, com as suas skills e os seus agentes. A loja aponta para eles.

## Repositórios

| Plugin | Repositório | Para quem | Quem vê |
| --- | --- | --- | --- |
| `live-geral` | `live-agentes` (este) | Todo o time | Todos |
| `live-atendimento` | `live-agentes-atendimento` | Atendimento | Todos |
| `live-producao` | `live-agentes-producao` | Produção | Todos |
| `live-planejamento` | `live-agentes-planejamento` | Planejamento | Todos |
| `live-criacao` | `live-agentes-criacao` | Criação | Todos |
| `live-marketing` | `live-agentes-marketing` | Marketing | Todos |
| `live-martech` | `live-agentes-martech` | Martech | Todos |
| `live-rh` | `live-agentes-rh` | RH | Só RH e Martech |
| `live-financeiro` | `live-agentes-financeiro` | Financeiro | Só Financeiro e Martech |

O que já existe: `memoria-projeto` no `live-geral` e as 7 skills `human-*` no `live-criacao`. Os outros departamentos começam vazios.

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

As skills aparecem como `/live-geral:memoria-projeto`, `/live-criacao:human-image` etc. Skills e agentes também entram sozinhos quando o pedido combina com a descrição deles.

Para receber as novidades: `claude plugin marketplace update live-agentes`.

## Estrutura

```
live-agentes/                          ← este repositório (a loja)
├── .claude-plugin/marketplace.json    ← lista os 9 plugins e onde cada um mora
├── .github/CODEOWNERS                 ← quem aprova mudanças
├── _modelos/                          ← ponto de partida para skill e agente novos
│   ├── skill/SKILL.md
│   └── agente/nome-do-agente.md
└── plugins/live-geral/                ← todo o time
    ├── .claude-plugin/plugin.json
    ├── skills/<skill>/SKILL.md
    └── agents/<agente>.md

live-agentes-<departamento>/           ← um repositório por departamento
├── .claude-plugin/plugin.json         ← o plugin fica na raiz
├── skills/<skill>/SKILL.md
└── agents/<agente>.md
```

## Onde colocar cada coisa

- **Skill ou agente de um departamento** (só faz sentido para um time): `skills/` ou `agents/` no repositório do departamento.
- **Skill ou agente geral** (serve a qualquer departamento): `plugins/live-geral/skills/` ou `plugins/live-geral/agents/`, aqui.
- Na dúvida, comece no departamento. Quando outro time pedir, ela sobe para o geral.

**Skill ou agente?** Uma skill é um passo a passo que o próprio Claude segue na conversa (montar um cronograma, escrever uma ata). Um agente é um especialista que o Claude chama para fazer uma parte do trabalho em separado (revisar um texto, conferir uma planilha) e devolve só o resultado.

## Quem vê e quem aprova

| Quem | O que pode fazer |
| --- | --- |
| Times de departamento | Ver os repositórios a que têm acesso e propor mudanças por pull request |
| Martech | Revisar e aprovar os pull requests |
| Donos da organização | Aprovar e fazer merge também |

Ninguém altera o `main` direto: toda mudança entra por pull request aprovado pelo Martech ou por um dono da organização. A regra está no `.github/CODEOWNERS` de cada repositório.

RH e Financeiro são restritos: só o próprio time e o Martech veem. Mesmo assim, o nome e a descrição desses plugins aparecem na loja para todo mundo, então a descrição em `marketplace.json` não pode revelar nada sensível.

## Como contribuir

Os times só têm leitura, então a mudança sai de uma cópia sua do repositório (fork):

1. No GitHub, abra o repositório certo (o do seu departamento, ou este para o `live-geral`), clique em **Fork** e clone o seu fork fora do OneDrive (ex.: `C:/dev/liveidea/`).
2. Copie o modelo (`_modelos/skill/` ou `_modelos/agente/`, daqui) para `skills/` ou `agents/` e renomeie. O nome da pasta da skill (ou do arquivo do agente) é igual ao `name` dentro dele, em `kebab-case` minúsculo, sem acento.
3. Atualize as listas de skills e agentes no README do plugin.
4. Suba o `version` no `plugin.json` do plugin (0.1.0 → 0.2.0 para skill ou agente novo, 0.1.0 → 0.1.1 para ajuste).
5. Valide: `claude plugin validate .`
6. Envie para o seu fork e abra um pull request para o `main` do repositório original. O Martech revisa e aprova.

Se você não tem familiaridade com git, mande a skill ou o agente para o Martech, que ele abre o pull request por você.

Regras:

- Dentro de uma skill, nunca use caminho fixo do seu computador (`~/.claude/skills/...`). Use `${CLAUDE_PLUGIN_ROOT}/skills/<nome>/...`.
- Nunca coloque chaves de API, tokens, senhas, dados pessoais ou valores de cliente nos arquivos.
- Fontes e materiais licenciados não entram nos repositórios.
- Saídas geradas pelas skills ficam na pasta do projeto de quem usa, nunca nos repositórios.
- O nome da agência é sempre **LIVEIDEA**, junto e em caixa alta.

## Configuração no GitHub (uma vez, feita por um dono da organização)

1. **Permissão base da organização** (**Settings → Member privileges → Base permissions**): **No permission**. Se estiver em **Read**, todo membro vê todos os repositórios privados, inclusive os de RH e Financeiro.
2. **Fork de repositório privado** (**Settings → Member privileges → Repository forking**): ligado. Sem isso, quem só tem leitura não consegue propor mudanças. Ligue também em **Settings → General → Allow forking** de cada repositório.
3. **Acesso aos repositórios** (**Settings → Collaborators and teams**). Martech com **Maintain** em todos. Os times com **Read**:
   - `live-agentes` e os 6 repositórios abertos (atendimento, producao, planejamento, criacao, marketing, martech): os 8 times.
   - `live-agentes-rh`: só o time RH.
   - `live-agentes-financeiro`: só o time Financeiro.
4. **Proteção do `main`** (**Settings → Rules → New branch ruleset**), em cada um dos 9 repositórios:
   - exigir pull request com 1 aprovação;
   - exigir aprovação de **Code Owners**;
   - bloquear push direto e force push;
   - em **Bypass list**, adicionar **Organization admin**, para que os donos da organização também possam aprovar e fazer merge.

   Dica: se o plano da organização permitir, em **Organization settings → Rules** dá para criar o ruleset uma vez só e aplicar a todos os repositórios `live-agentes*`.
5. Confira se `@Agencia-LIVEIDEA/martech` no `.github/CODEOWNERS` é o slug do time Martech (URL `github.com/orgs/Agencia-LIVEIDEA/teams/<slug>`). O GitHub avisa no próprio arquivo se o nome não existir.

Exigir aprovação de Code Owners em repositório privado depende do plano GitHub Team (ou superior) da organização.

## Pendências

- [ ] Licença das skills `human-*` para uso pelo time todo.
- [ ] Primeira skill ou agente de cada departamento.
