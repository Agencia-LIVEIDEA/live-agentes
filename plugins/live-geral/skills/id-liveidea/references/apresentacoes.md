# Apresentações (.pptx)

Base: seções "Layout", "Onde o sistema é usado", "Apresentações de projeto" e "Proposta criativa" do
`DS_DIR/README.md`. Este arquivo explica como levar essas regras para o PowerPoint.

## Escala

- Slide 16:9 de 13,333 × 7,5 pol. O palco do sistema é 1920 × 1080 px: **2 px = 1 pt** e 144 px = 1 pol.
- O helper `liveidea_pptx.py` trabalha em px do palco. Copie as medidas do README e das prévias
  (`DS_DIR/components/PropostaCriativa/preview.html`) sem converter.
- Corpos em pt já estão em `DS_KIT/office.json` → `styles.<token>.size_pt`.

## Fontes no Office

Cada peso fora de Regular/Bold é uma família separada no Office. Não escreva o nome à mão: o
`office.json` traz, por arquivo, o nome que o PowerPoint reconhece (`fonts.<família|peso|estilo>.name`)
e se ele entra com negrito/itálico ligado. Exemplos da v1.2.0: Acumin Light Italic =
"Acumin Pro ExtraCondensed Light" + itálico; Acumin Medium = "Acumin Pro ExtraCondensed Med";
PP Editorial New Ultrabold Italic = "PP Editorial New Ultrabold" + itálico. O helper resolve isso
sozinho a partir do markup.

- As fontes são licenciadas e não são embutidas no .pptx. Quem abrir o arquivo precisa delas
  instaladas (máquinas da agência). Por isso o **Ghost e o lettering do cliente vão como PNG** (regra do README).
- Para apresentar fora da agência, sugira exportar PDF.

## Fluxo com o helper

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from liveidea_pptx import Deck
deck = Deck(DS_KIT)                       # avisa se a versão for mais nova que os modelos
deck.capa_padrao()                        # sempre a primeira página
deck.capa_projeto("Nome do projeto", "frase em serifa", ghost="<b>CONCEITO </b><em>EM</em> DUAS")
s = deck.slide("nevoa")                   # nevoa | cinza | laranja | ambar | grafite | foto
deck.eyebrow(s, 1, "Insight", x=1073, y=223)
deck.text(s, "Título com <em>destaque</em>", "headline-l", x=1073, y=281, w=749, size=64, weight=700,
          em_color="laranja")
deck.text(s, "Texto de apoio.", "body-3xl", x=1073, y=554, w=720, color="ink-muted")
deck.chrome(s)                            # marcas de borda, cor automática pelo fundo
deck.peca("kv.png")                       # página de peça: sem texto e sem Chrome
deck.abertura("Desdobramentos", "do KV para o evento", "<b>DO KV À </b><i>experiência</i>")
deck.fechamento("Saúde!")
deck.save("proposta.pptx")
```

Outros métodos: `photo(slide, path, x, y, w, h, veil="leve"|"denso", fade="base", focus=(0.5, 0.3))`,
`stat(slide, value, label, x, y, w, size="m"|"l"|"xl", unit=, note=, subtitle=)`, `rule(...)`,
`rect(...)`, `logo(slide, "nevoa"|"laranja"|"grafite", x, y, w)`, `ghost(slide, markup, size)`.

Markup igual ao dos componentes: texto puro = peso base; `<b>` Bold; `<em>` no Display = Light Italic,
nos títulos Aeonik = PP Editorial New Italic; `<i>` no Display = troca pela serifa em caixa-baixa;
`<br>` quebra de linha.

## Roteiros

- **Apresentação institucional**: capa padrão → conteúdo no padrão da apresentação comercial 2027.
- **Apresentação de projeto**: capa padrão → capa do projeto → páginas de case (cliente em `label`
  `ink-muted`, nome do projeto em Display com a regra da mistura, descrição em `body-tight`, números
  em Stat) → etapas em PillarList (numerada) → fechamento.
- **Proposta criativa**: siga a ordem de 11 passos do README ("Proposta criativa"). O Eyebrow
  numera só insight, tese, conceito, moodboard e KV.

## Mapa de componentes → PowerPoint

| Componente | No .pptx |
|---|---|
| Chrome | `deck.chrome(s)` em toda página, exceto página de peça |
| Ghost | `deck.ghost(...)` (PNG do tamanho do slide) |
| Display / Headline | `deck.text(..., "display-case" / "headline-m" ...)` com markup |
| Stat | `deck.stat(...)`: número âmbar à direita, rótulo `ink` à esquerda, fio `rule` |
| Eyebrow | `deck.eyebrow(...)`; `tone="ambar"` sobre foto e grafite |
| NumberedList / Steps / PillarList | caixas `text` com número `stat-m` (52 px) e fios `rule`; leia o README do componente |
| Photo / PhotoGrid | `deck.photo(...)` com véu/degradê; vãos `space-4` (24 px) |
| Logo | `deck.logo(...)`: arquivo pela cor do fundo (névoa sobre laranja/grafite/foto) |

## Armadilhas do PowerPoint

- Entrelinha dos displays (0,70–0,77) é menor que o corpo: o helper desce a primeira linha para o
  acento não sair da caixa. Mesmo assim, deixe ~0,3 × o corpo livre acima de um título display.
- Transparência (véus, `rule` a 30%) é alpha no XML; o helper já aplica.
- Não use "Ajustar texto automaticamente": o corpo vem do volume de texto, não do espaço.
- Imagens do cliente (KV, lettering, mockups) mantêm as cores originais.

## Revisão visual

```bash
soffice --headless --convert-to pdf proposta.pptx && pdftoppm -r 50 -png proposta.pdf previa
```

Instale antes as fontes do kit (`build_kit.py --install-fonts --out $DS_KIT`) para o render ser fiel.
Olhe cada página contra o `references/checklist.md`.
