"""Helper python-docx para documentos LIVEIDEA (propostas em PDF, orçamentos, relatórios),
alimentado pelo office.json da versão baixada. Regra do README (Outras aplicações > Documentos):
fundo névoa, texto body-l em grafite, títulos headline-m com destaque em serifa itálica, números em
PP Editorial New, tabelas com fios rule. Laranja só em títulos grandes (26 pt ou mais) e no logo.

    import sys; sys.path.insert(0, "<skill>/scripts")
    from liveidea_docx import Doc
    d = Doc("<DS_KIT>")
    d.logo("laranja")
    d.eyebrow("Proposta comercial")
    d.title("Verão Grupo EMS <em>2026</em>")          # headline-statement reduzido, destaque laranja
    d.heading("O que <em>entregamos</em>")             # headline-m, destaque em serifa grafite
    d.para("Traduzimos objetivos de negócio em experiências...")
    d.stats([("+ 50.000", "PESSOAS"), ("5 <em>dias</em>", "DE MONTAGEM")])
    d.table(["Item", "Valor"], [["Cenografia", "R$ 120.000"]])
    d.save("proposta.docx")    # PDF: soffice --headless --convert-to pdf proposta.docx
"""
import json, subprocess
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from liveidea_pptx import parse_markup  # mesmo markup: <b>, <em>, <i>

HERE = Path(__file__).resolve().parent
ACCENT_MIN_PT = 26  # 52 px do palco: abaixo disso, laranja/âmbar sobre fundo claro não passa no contraste


class Doc:
    def __init__(self, kit, margins_cm=2.0):
        self.kit = Path(kit)
        self.o = json.loads((self.kit / "office.json").read_text(encoding="utf-8"))
        self.version = self.o.get("version")
        self.d = Document()
        for s in self.d.sections:
            s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Cm(margins_cm)
        self._background("nevoa")
        self._base_styles()

    # ------------------------------------------------------------------ base
    def hex(self, name):
        return self.o["colors"]["light"][name]["hex"]

    def blend(self, name, bg="nevoa"):
        """Cor com transparência (ex.: rule 30%) misturada ao fundo, para o Word que não tem alpha."""
        c = self.o["colors"]["light"][name]
        a = c.get("alpha", 1.0)
        fg, bgc = bytes.fromhex(c["hex"]), bytes.fromhex(self.hex(bg))
        return "".join(f"{round(f * a + b * (1 - a)):02X}" for f, b in zip(fg, bgc))

    def font_for(self, role, weight, style):
        fam = next(s["family"] for s in self.o["styles"].values() if s["role"] == role)
        best, score = None, None
        for key, info in self.o["fonts"].items():
            f, w, st = key.split("|")
            if f != fam:
                continue
            d = min(abs(int(weight) - int(x)) for x in w.split()) + (0 if st == style else 1000)
            if score is None or d < score:
                best, score = info, d
        return best

    def _background(self, name):
        bg = OxmlElement("w:background"); bg.set(qn("w:color"), self.hex(name))
        self.d.element.insert(0, bg)
        settings = self.d.settings.element
        disp = OxmlElement("w:displayBackgroundShape"); settings.insert(0, disp)

    def _base_styles(self):
        st = self.o["styles"]["body-l"]
        normal = self.d.styles["Normal"]
        info = self.font_for("sans", 400, "normal")
        normal.font.name = info["name"]
        normal.element.rPr.rFonts.set(qn("w:eastAsia"), info["name"])
        normal.font.size = Pt(st["size_pt"])
        normal.font.color.rgb = RGBColor.from_string(self.hex("ink"))
        pf = normal.paragraph_format
        pf.line_spacing = st["line_height"]
        pf.space_after = Pt(st["size_pt"] * 0.8)

    def _runs(self, p, markup, style, color="ink", em_color=None, size_pt=None, upper=None):
        st = self.o["styles"][style]
        size = size_pt or st["size_pt"]
        role, base_w, base_s = st["role"], st["weight"], st["style"]
        up = (role == "display") if upper is None else upper
        for chunk, tags in parse_markup(markup):
            if chunk == "\n":
                p.add_run().add_break(); continue
            r_role, w, s, u, col = role, base_w, base_s, up, color
            if "b" in tags or "strong" in tags:
                w = 700
            if "em" in tags or "i" in tags:
                if role == "display" and "em" in tags:      # Acumin Light Italic
                    w, s = 300, "italic"
                elif role in ("sans", "display"):           # troca pela serifa itálica
                    r_role, w, s, u = "serif", 400, "italic", False
                else:
                    s = "italic"
                col = em_color or col
            info = self.font_for(r_role, w, s)
            r = p.add_run(chunk.upper() if u else chunk)
            r.font.name = info["name"]
            r._element.rPr.rFonts.set(qn("w:eastAsia"), info["name"])
            r.font.bold, r.font.italic = info["bold"], info["italic"]
            r.font.size = Pt(size)
            r.font.color.rgb = RGBColor.from_string(self.hex(col))
            spc = st["letter_spacing_em"] * size * 20  # twips
            if spc:
                sp = OxmlElement("w:spacing"); sp.set(qn("w:val"), str(int(round(spc))))
                r._element.get_or_add_rPr().append(sp)
        return p

    def _para(self, before=0, after=None, line=None, align=None):
        p = self.d.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(before)
        if after is not None:
            pf.space_after = Pt(after)
        if line is not None:
            pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE; pf.line_spacing = line
        if align:
            p.alignment = {"center": WD_ALIGN_PARAGRAPH.CENTER, "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
        return p

    # ------------------------------------------------------------- conteúdo
    def logo(self, variant="laranja", width_cm=4.0):
        svg = self.kit / "assets" / "Logos" / f"liveidea-{variant}.svg"
        png = self.kit / "png" / f"logo-{variant}.png"
        png.parent.mkdir(exist_ok=True)
        if not png.exists():
            subprocess.run(["node", str(HERE / "render.js"), "--kit", str(self.kit), "--svg", str(svg),
                            "--width", "1600", "--out", str(png)], check=True)
        p = self._para(after=24)
        p.add_run().add_picture(str(png), width=Cm(width_cm))

    def eyebrow(self, text, number=None):
        label = (f"{int(number):02d} · " if number is not None else "") + text.upper()
        return self._runs(self._para(after=6), label, "eyebrow")

    def title(self, markup, size_pt=36):
        """Título de abertura do documento: Aeonik Bold caixa-alta com o fim em serifa itálica.
        Destaque em laranja só se o corpo for >= 26 pt."""
        em = "laranja" if size_pt >= ACCENT_MIN_PT else "ink"
        return self._runs(self._para(after=18, line=1.0), markup, "headline-statement", em_color=em,
                          size_pt=size_pt, upper=True)

    def heading(self, markup, size_pt=None):
        st = self.o["styles"]["headline-m"]
        size = size_pt or st["size_pt"]
        em = "laranja" if size >= ACCENT_MIN_PT else "ink"
        p = self._para(before=18, after=8, line=1.0)
        p.style = self.d.styles["Heading 1"]
        p.paragraph_format.keep_with_next = True
        return self._runs(p, markup, "headline-m", em_color=em, size_pt=size)

    def para(self, markup, style="body-l", color="ink"):
        return self._runs(self._para(), markup, style, color=color)

    def stats(self, rows, size="stat-m", size_pt=None):
        """Números em coluna: rótulo à esquerda (label), número à direita (PP Editorial New), fio rule.
        Número em âmbar só a partir de 26 pt; abaixo disso, grafite."""
        num_pt = size_pt or self.o["styles"][size]["size_pt"]
        num_color = "accent-number" if num_pt >= ACCENT_MIN_PT else "ink"
        t = self.d.add_table(rows=0, cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for value, label in rows:
            c1, c2 = t.add_row().cells
            c1.vertical_alignment = c2.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.BOTTOM
            self._runs(c1.paragraphs[0], label, "label")
            p = c2.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            self._runs(p, value, size, color=num_color, em_color=num_color, size_pt=num_pt)
        self._rules(t, inner_only=False, horizontal_only=True)
        self._para(after=6)
        return t

    def table(self, header, rows):
        t = self.d.add_table(rows=1, cols=len(header))
        for c, h in zip(t.rows[0].cells, header):
            self._runs(c.paragraphs[0], h, "label")
        for r in rows:
            cells = t.add_row().cells
            for c, v in zip(cells, r):
                self._runs(c.paragraphs[0], str(v), "body-l")
        self._rules(t, horizontal_only=True)
        self._para(after=6)
        return t

    def _rules(self, table, inner_only=False, horizontal_only=True):
        color = self.blend("rule")
        tblPr = table._tbl.tblPr
        borders = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = OxmlElement(f"w:{edge}")
            on = edge in ("insideH", "bottom") or (edge == "top" and not inner_only)
            if horizontal_only and edge in ("left", "right", "insideV"):
                on = False
            el.set(qn("w:val"), "single" if on else "nil")
            if on:
                el.set(qn("w:sz"), "4"); el.set(qn("w:color"), color)
            borders.append(el)
        tblPr.append(borders)

    def save(self, path):
        self.d.save(path)
        print(f"Documento salvo em {path} (design system LIVEIDEA v{self.version}, commit {self.o.get('commit')})")
        return path
