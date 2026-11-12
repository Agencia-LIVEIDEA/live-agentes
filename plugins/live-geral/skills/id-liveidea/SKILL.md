---
name: id-liveidea
description: Aplica o design system da LIVEIDEA, sempre na última versão da branch main do repositório GitHub Agencia-LIVEIDEA/id-liveidea, em apresentações (PowerPoint, decks, propostas criativas, apresentações de projeto), documentos (Word, PDF, propostas comerciais, orçamentos, relatórios) e artefatos gerados (páginas HTML, artifacts, landing pages, peças de redes). Use sempre que for criar, adaptar ou revisar qualquer material que a LIVEIDEA assina em nome próprio, mesmo quando o pedido só diz "no padrão da agência", "com a nossa identidade", "com a cara da LIVEIDEA", "no nosso template" ou cita a marca LIVEIDEA. Não use para peças de eventos de clientes (cenografia, credenciais, KVs do cliente), que seguem o design system do próprio cliente.
---

# Design system LIVEIDEA

Esta skill não guarda cores, fontes nem regras de marca. Ela busca a **última versão** do design system no
GitHub a cada uso, monta um kit de aplicação a partir dela e aplica no formato pedido. Se algo aqui
divergir do `design-system/README.md` da versão baixada, **o README vence**.

## Passo 0 · Buscar a última versão (obrigatório, toda vez)

```bash
bash <skill>/scripts/sync_ds.sh
```

`<skill>` é a pasta desta skill (no plugin `live-geral`: `${CLAUDE_PLUGIN_ROOT}/skills/id-liveidea`). O script clona ou atualiza um cache com a `main` de
`Agencia-LIVEIDEA/id-liveidea` (nunca o seu checkout de trabalho), confere se `tokens.json` e
`CHANGELOG.md` concordam na versão e monta o kit. Ele imprime:

- `DS_DIR`: a pasta `design-system/` da versão baixada (brand book, tokens, componentes, assets).
- `DS_KIT`: o kit gerado (`tokens.css`, `fonts.css`, `fonts-inline.css`, `office.json`, logos, ícones, bundle).
- `DS_VERSION`, `DS_DATE`, `DS_COMMIT`: o que foi aplicado. **Diga ao usuário** no início:
  "Design system LIVEIDEA v1.2.0 (main @ ce5a99f, 11, novembro, 2026)".

"Última versão" é a `main`: só entra o que foi mergeado. Branch ou PR aberto não conta. Se a última
tag `vX.Y.Z` estiver atrás da `main`, vale a `main` (o script avisa).

**Se o script sair com código 2 (sem acesso ao GitHub), siga nesta ordem:**
1. **Conector GitHub**, se houver na conversa: leia da `main` `design-system/README.md`, `design-system/tokens.json`,
   `design-system/CHANGELOG.md`, `design-system/components/bundle.js` e os SVGs de `design-system/assets/Logos`
   (e `Icones`, se for usar), salve numa pasta com essa mesma estrutura e rode
   `bash <skill>/scripts/sync_ds.sh --local <pasta>`. Fontes e fotos não precisam vir: a skill usa as da cópia do pacote.
2. **Sem conector, ou com o conector sem acesso ao repositório: recomende conectar o GitHub** e mostre o
   passo a passo de `references/conectar-github.md`. É o caminho principal.
3. Se o usuário não puder conectar agora: peça o **ZIP da `main`** (GitHub > Code > Download ZIP) e rode
   `bash <skill>/scripts/sync_ds.sh --from-zip <arquivo.zip>`. Diga que não deu para confirmar se é a última versão.
4. **Último caso: seguir com a cópia do pacote.** Se o usuário não puder conectar nem enviar o ZIP e quiser seguir
   mesmo assim, ofereça a cópia do design system que veio no pacote da skill. Antes, diga a versão e a data dela
   (`<skill>/snapshot/VERSION`) e que ela pode estar desatualizada. **Só use com o "sim" do usuário.** Então rode
   `bash <skill>/scripts/sync_ds.sh --snapshot`, siga os passos normais e, na entrega, registre:
   "Feito com a cópia do pacote (vX.Y.Z, de <data>), sem confirmar a versão atual. Revise quando o acesso ao
   repositório voltar."
5. **Nunca aplique a marca de memória** nem com valores de uma conversa anterior. Sem nenhuma das fontes acima, pare e explique.

**Cópia do pacote.** O ZIP da skill traz em `<skill>/snapshot/` uma cópia do design system tirada da `main` no
empacotamento (versão em `snapshot/VERSION`). Além do último caso acima, as fontes dela são a reserva quando a
versão baixada vem sem os arquivos de fonte; o kit avisa e registra em `manifest.json` (`fonts_from_skill_package`).
Se a cópia for de uma versão anterior a `DS_VERSION`, avise o usuário que o pacote da skill precisa ser
reempacotado e reenviado. No Claude Code, dentro do repositório, a cópia não existe: lá a skill lê a `main` direto.

Código 3 = repositório inconsistente (versões divergentes): avise e não siga sem o usuário decidir.

## Passo 1 · Ler a versão baixada

Leia sempre, da versão baixada:
1. `DS_DIR/CHANGELOG.md`, a entrada do topo: o que mudou e se há regra de transição.
2. `DS_DIR/README.md` inteiro (cerca de 22 KB): princípios, tom, cor, tipografia, layout, onde o sistema é usado, fotografia, logo, ícones.
3. O `README.md` de cada componente que a peça vai usar (`DS_DIR/components/<Componente>/README.md`).
4. `DS_DIR/tokens.json` quando precisar do uso de um token específico (`usage`).

## Passo 2 · Escolher o caminho pelo formato

| Pedido | Leia | Ferramenta |
|---|---|---|
| Apresentação, deck, proposta criativa, apresentação de projeto (.pptx) | `references/apresentacoes.md` | `scripts/liveidea_pptx.py` |
| Documento, proposta comercial, orçamento, relatório (.docx, .pdf) | `references/documentos.md` | `scripts/liveidea_docx.py` |
| Artifact, página HTML, landing, site, peça de rede, slide em HTML | `references/artefatos-html.md` | `DS_KIT/tokens.css` + fontes + `components/bundle.js` |
| Planilha (.xlsx) | `references/documentos.md` (seção Planilhas) | openpyxl com `office.json` |

Se houver uma skill de formato disponível (pptx, docx, pdf, xlsx), use-a para a mecânica do arquivo e
esta skill para tudo o que é marca. Para peças de redes e Ghost/lettering em PNG, use
`scripts/render.js`.

## Passo 3 · Produzir

- Valores sempre do kit (`office.json` ou `tokens.css`), nunca digitados à mão. Cor pelo nome do token (`laranja`, `ink`, `rule`), estilo de texto pelo nome do token (`display-case`, `headline-m`, `body-l`).
- Conteúdo e tom seguem a seção "Conteúdo e tom" do README: português, primeira pessoa do plural, sem emoji, sem exclamação, números no padrão brasileiro com a unidade em itálico, datas por extenso em minúscula. Reescreva o texto do usuário quando ele quebrar essas regras e diga o que mudou.
- O sistema vale para o que a LIVEIDEA assina. Marca de cliente entra só pelo arquivo oficial, na cor original, onde o README permite (capa do projeto e fechamento).
- Falta conteúdo real (foto do evento, número de entrega, logo do cliente)? Use as fotos de `DS_DIR/assets/Fotografia` só se forem do mesmo tipo de evento e diga isso; caso contrário, deixe o espaço marcado como pendente. Nunca use banco de imagem nem invente número de entrega.

## Passo 4 · Revisar antes de entregar

1. Renderize e olhe: PPTX/DOCX → PDF com `soffice --headless --convert-to pdf` e `pdftoppm -r 50 -png`; HTML → `node <skill>/scripts/render.js --kit $DS_KIT --html pagina.html --out previa.png`. Para o render bater com o original, instale as fontes do kit no ambiente: `python3 <skill>/scripts/build_kit.py --install-fonts --out $DS_KIT`.
2. Passe o `references/checklist.md` item a item e corrija o que falhar.
3. Na entrega, informe: versão aplicada (versão + commit), arquivos gerados, desvios conscientes do sistema e por quê, e pendências (fotos, logo do cliente, números a confirmar).

## Regras que mais quebram (confira na versão baixada)

- Toda apresentação abre com a **capa padrão** e, se for projeto, a capa do projeto vem em seguida.
- **Ghost** em caixa-alta, centralizado, inteiro na largura, sangrando só a base. No PowerPoint vai como PNG transparente.
- **Marcas de borda** (Chrome) em toda página de apresentação, exceto página de peça (KV/mockup em página inteira).
- **Laranja e âmbar sobre fundo claro** só em 52px de palco (26pt) ou mais. Texto corrido nunca em laranja.
- **Números** sempre em PP Editorial New; **corpo de texto** pelo volume de texto (um por página).
- **Estimativa** de proposta marcada como estimativa (PÚBLICO ESTIMADO), nunca como entrega.
- Fotos retas, sem moldura, sem canto arredondado, sem texto sem véu ou degradê.

## Quando a versão for mais nova que os helpers

`liveidea_pptx.py` traz modelos de página (capas, abertura, fechamento) medidos na versão indicada em
`TEMPLATES_FROM`. Se o kit for de uma versão MINOR ou MAJOR mais nova, o helper avisa. Leia o
CHANGELOG desde aquela versão; se capa, Ghost, Chrome, grid ou tipografia mudaram, ajuste a chamada
(ou o helper) para a regra nova antes de gerar e diga ao usuário que ajustou.
