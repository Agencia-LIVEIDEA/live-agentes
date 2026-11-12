# Artefatos HTML (artifacts, páginas, site, peças de redes, slides em HTML)

Base: "Site", "Outras aplicações", "Movimento", "Botões" e "Componentes" do `DS_DIR/README.md`, e o
`index.d.ts` dos componentes (props).

## Montagem da página

Tudo vem do kit. Para um arquivo único (artifact do claude.ai, e-mail, anexo), embuta inline:

```html
<style>/* conteúdo de DS_KIT/fonts-inline.css */</style>
<style>/* conteúdo de DS_KIT/tokens.css */</style>
<style>/* conteúdo de DS_KIT/components/bundle.css */</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.3.1/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.3.1/umd/react-dom.production.min.js"></script>
<script>/* conteúdo de DS_KIT/components/bundle.js -> window.LiveIdea */</script>
```

- Com arquivos ao lado (site, pasta de entrega), use `fonts.css` + pasta `fonts/` em vez do inline.
- Sem React, use só tokens + classes de texto `.ts-<token>` (ex.: `.ts-display-case`, `.ts-body-l`) e
  escreva o HTML seguindo o README de cada componente. Os nomes de variável CSS são os nomes dos
  tokens (`var(--laranja)`, `var(--ink)`, `var(--space-4)`).
- Componentes disponíveis em `window.LiveIdea`: Icon, Button, ProgressBar, Photo, PhotoGrid, Chrome,
  Logo, Display, Headline, CaseHeader, Stat, PillarList, ReadPill, PressCard, TeamCard, ArrowLink,
  Stamp, Eyebrow, NumberedList, Steps, Ghost. Confira a lista no bundle da versão baixada.

## Temas

`tokens.css` traz o tema Claro em `:root` e o Grafite em `[data-theme="dark"]`. Quando o contrato do
artifact pedir modo escuro automático, repita o bloco Grafite dentro de
`@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { ... } }`. Fundo explícito no
`body` (`var(--surface)`).

## Fontes e licença

Acumin Pro ExtraCondensed, PP Editorial New e Aeonik são licenciadas pela agência; Space Grotesk é
aberta. Embutir as três licenciadas num artifact **privado** ou num arquivo interno é o uso esperado.
Antes de publicar um site ou compartilhar um artifact fora da LIVEIDEA, avise o usuário e peça para
confirmar a licença web (regra do README). Se não houver confirmação, use as fontes de reserva do
próprio token (`Arial Narrow`, `Georgia`, `Helvetica Neue`) e diga isso.

## Imagens

- Fotos de `DS_DIR/assets/Fotografia`, capas de `DS_DIR/assets/Capas`, logos e ícones de
  `DS_KIT/assets`. Num arquivo único, embuta como data URI (atenção ao limite de 16 MB do artifact:
  reduza fotos para ~1600 px no maior lado antes).
- As prévias do repositório apontam para `/_blob/<id>`: isso só funciona dentro do design system do
  claude.ai. Fora dele, use os arquivos de `assets/`.

## Design system publicado no claude.ai

O repositório guarda a cópia em arquivos do design system publicado no claude.ai (link no
`README.md` da raiz do repositório). Se for usar um tipo de Artifact que puxa design system
(slides, design), confira antes que o `lastChange.note` publicado começa pela mesma versão de
`DS_VERSION`. Se o publicado estiver atrás, avise o usuário e siga as regras do repositório.

## Formatos

- **Site/landing:** coluna até 640 px no mobile, gutter `space-3`, respiro `space-7`, corpos pela
  tabela mobile do README, barra de progresso âmbar de 3 px no topo, movimento do README com
  `prefers-reduced-motion`. Texto, links e campos nunca em laranja ou âmbar sobre fundo claro; foco
  visível com `focus`.
- **Slide em HTML:** palco 1920 × 1080 escalado, Chrome em todas as páginas exceto a de peça.
- **Peça de rede:** uma ideia por peça, título com a regra da mistura, foto com véu ou degradê quando
  tem texto por cima, tamanhos pela tabela mobile, logo névoa sobre foto/laranja e laranja sobre névoa,
  sem marcas de borda. Exporte com
  `node <skill>/scripts/render.js --kit $DS_KIT --html peca.html --width 1080 --height 1350 --scale 2 --out peca.png`.
