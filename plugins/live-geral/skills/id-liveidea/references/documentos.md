# Documentos (.docx, .pdf) e planilhas

Base: "Outras aplicações > Documentos", "Cor", "Tipografia" e "Conteúdo e tom" do `DS_DIR/README.md`.

## O que o sistema define para documentos

- Fundo névoa, texto `body-l` em grafite.
- Títulos `headline-m` (Aeonik Bold) com o trecho que importa em PP Editorial New Italic.
- Números em PP Editorial New. Tabelas com fios `rule`.
- Laranja só em títulos grandes e no logo.

O que o sistema **não** define para documentos (margens, cabeçalho e rodapé, numeração de página,
formato A4 ou carta): use o padrão do helper (A4, margens de 2 cm, sem marcas de borda) e não invente
elemento de marca novo. Se o usuário pedir algo fora disso, faça e registre como desvio na entrega.

## Escala

Mesma relação do palco: 2 px = 1 pt. `body-l` 20 px = 10 pt, `headline-m` 40 px = 20 pt,
`stat-m` 52 px = 26 pt. Os valores estão em `DS_KIT/office.json`.

**Contraste:** laranja e âmbar sobre névoa só a partir de 26 pt (52 px). Abaixo disso, o destaque em
serifa e os números vão em grafite. O helper aplica isso sozinho (`ACCENT_MIN_PT`).

## Fluxo com o helper

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from liveidea_docx import Doc
d = Doc(DS_KIT)
d.logo("laranja")                                  # sobre névoa: laranja ou grafite
d.eyebrow("Proposta comercial")
d.title("Convenção Ypê <em>APAS 2027</em>")        # 36 pt, fim da frase em serifa laranja
d.heading("O que <em>entregamos</em>")
d.para("Traduzimos objetivos de negócio em experiências...")
d.stats([("+ 3.000", "PÚBLICO ESTIMADO"), ("5 <em>dias</em>", "PREVISÃO DE MONTAGEM")])
d.table(["Item", "Escopo", "Valor"], [["Cenografia", "Estande 600m²", "R$ 420.000"]])
d.save("proposta.docx")
```

PDF: `soffice --headless --convert-to pdf proposta.docx` (com as fontes do kit instaladas). Para PDF
gerado direto de HTML, siga `artefatos-html.md` e imprima com Playwright (`page.pdf`).

## Conteúdo

- Primeira pessoa do plural; o cliente é tratado pela marca dele, nunca por "você".
- Valores em reais no padrão brasileiro (R$ 420.000). Números de proposta são previsões: rótulo
  marca a estimativa (PÚBLICO ESTIMADO, PREVISÃO DE MONTAGEM).
- Datas por extenso em minúscula: "14, agosto, 2026."
- Sem emoji e sem ponto de exclamação.

## Planilhas (.xlsx)

O sistema não tem regra própria para planilhas. Leve o mínimo reconhecível, com openpyxl e `office.json`:
cabeçalho em Aeonik Bold 8 pt caixa-alta (`label`), corpo Aeonik 10 pt grafite, números alinhados à
direita no padrão brasileiro, fios horizontais `rule` (misture a 30% sobre névoa: `#AFAFAF`
na v1.2.0, ou calcule com `Doc.blend("rule")`), sem preenchimento colorido nas células. Laranja só no
título da aba, se houver título grande.
