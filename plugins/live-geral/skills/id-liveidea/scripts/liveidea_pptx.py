"""Helper python-pptx para apresentações LIVEIDEA, alimentado pelo kit da versão baixada
(office.json, fontes, logos). Coordenadas sempre em px do palco 1920x1080 (2 px = 1 pt).

    import sys; sys.path.insert(0, "<skill>/scripts")
    from liveidea_pptx import Deck
    deck = Deck("<DS_KIT>")
    deck.capa_padrao()
    deck.capa_projeto("Verão Grupo EMS 2026", "nova proposta de KV", ghost="<b>SAÚDE </b><em>&</em> ENERGIA")
    s = deck.slide("nevoa")
    deck.eyebrow(s, 1, "Insight", x=1073, y=223)
    deck.text(s, "No Brasil, a gente comemora <em>desejando saúde.</em>", "headline-l", x=1073, y=281, w=749,
              size=64, weight=700, em_color="laranja")
    deck.save("proposta.pptx")

Markup dos textos (o mesmo dos componentes): texto puro = peso base do estilo; <b> Bold;
<em> no Display = Acumin Light Italic, nos títulos Aeonik = PP Editorial New Italic;
<i> no Display = troca por PP Editorial New Italic em caixa-baixa (serif-display); <sbi> Semibold Italic.

Os modelos de página (capas, abertura, fechamento) seguem a página Proposta criativa da versão
TEMPLATES_FROM. Se o kit for de uma versão MINOR/MAJOR mais nova, o Deck avisa: confira o
CHANGELOG antes de usar os modelos e ajuste aqui se a regra mudou.
"""
import copy, json, os, re, subprocess, sys
from html.parser import HTMLParser
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

TEMPLATES_FROM = "1.2.0"
EMU_PER_PX = 6350  # 914400 EMU/in / 144 px/in
HERE = Path(__file__).resolve().parent
DARK_BGS = {"grafite", "foto"}
ALIGN = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}
ANCHOR = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}


def E(v):
    return Emu(int(round(v * EMU_PER_PX)))


class _Markup(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.runs = [], []

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.runs.append(("\n", tuple(self.stack)))
        else:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.stack:
            idx = len(self.stack) - 1 - self.stack[::-1].index(tag)
            self.stack.pop(idx)

    def handle_data(self, data):
        if data:
            self.runs.append((data, tuple(self.stack)))


def parse_markup(s):
    p = _Markup(); p.feed(s); p.close()
    return p.runs


class Deck:
    def __init__(self, kit, template=None):
        self.kit = Path(kit)
        self.o = json.loads((self.kit / "office.json").read_text(encoding="utf-8"))
        self.version = self.o.get("version") or "?"
        self._warn_version()
        self.prs = Presentation(template) if template else Presentation()
        if not template:
            self.prs.slide_width, self.prs.slide_height = E(1920), E(1080)
        self.blank = self.prs.slide_layouts[6 if len(self.prs.slide_layouts) > 6 else -1]
        self.png_dir = self.kit / "png"
        self.png_dir.mkdir(exist_ok=True)
        self._bg = {}

    # ------------------------------------------------------------------ base
    def _warn_version(self):
        try:
            k = [int(x) for x in self.version.split(".")[:2]]
            t = [int(x) for x in TEMPLATES_FROM.split(".")[:2]]
            if k > t:
                print(f"[liveidea_pptx] Kit v{self.version} é mais novo que os modelos (v{TEMPLATES_FROM}). "
                      "Leia o CHANGELOG: se capas, Ghost, Chrome ou grid mudaram, ajuste os modelos antes.",
                      file=sys.stderr)
        except ValueError:
            pass

    def color(self, name, theme="light"):
        c = self.o["colors"][theme].get(name) or self.o["colors"]["light"][name]
        return c["hex"], c.get("alpha", 1.0)

    def theme_of(self, slide):
        return "dark" if self._bg.get(slide.slide_id) in DARK_BGS else "light"

    def font_for(self, family, weight, style):
        best, score = None, None
        for key, info in self.o["fonts"].items():
            fam, w, st = key.split("|")
            if fam != family:
                continue
            d = min(abs(int(weight) - int(x)) for x in w.split()) + (0 if st == style else 1000)
            if score is None or d < score:
                best, score = info, d
        return best

    def family(self, role):
        for s in self.o["styles"].values():
            if s["role"] == role:
                return s["family"]
        raise KeyError(role)

    def slide(self, bg="nevoa"):
        """Página nova. bg: nevoa, cinza, laranja, ambar, grafite ou foto (foto = tema escuro, fundo grafite)."""
        s = self.prs.slides.add_slide(self.blank)
        self._bg[s.slide_id] = bg
        fill = s.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor.from_string(self.color("grafite" if bg == "foto" else bg)[0])
        return s

    def _set_alpha(self, fill_el_parent, alpha):
        if alpha >= 1:
            return
        clr = fill_el_parent.find(".//" + qn("a:srgbClr"))
        a = clr.makeelement(qn("a:alpha"), {"val": str(int(alpha * 100000))})
        clr.append(a)

    # ----------------------------------------------------------------- texto
    def text(self, slide, markup, style, x, y, w, h=None, color=None, em_color=None, align="left",
             anchor="top", size=None, weight=None, line_height=None, uppercase=None, wrap=True):
        """Caixa de texto com um estilo de tokens.json (ex.: display-case, headline-m, body-l, label).
        size em px do palco sobrescreve o corpo; color/em_color são nomes de token de cor."""
        st = self.o["styles"][style]
        theme = self.theme_of(slide)
        size_px = size or st["size_px"]
        lh = line_height or st["line_height"]
        h = h or size_px * max(lh, 1.0) * 1.15
        tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(h))
        tf = tb.text_frame
        tf.word_wrap = wrap
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = ANCHOR[anchor]
        if lh < 1:  # entrelinha menor que o corpo: desce a 1ª linha para o topo da letra ficar na caixa
            tf.margin_top = E((1 - lh) * size_px * 0.45)
        role = st["role"]
        base_w = weight or st["weight"]
        base_style = st["style"]
        upper = (role == "display") if uppercase is None else uppercase
        default_color = color or ("accent" if role == "display" else "ink")
        p = tf.paragraphs[0]
        p.alignment = ALIGN[align]
        p.line_spacing = Pt(size_px / 2 * lh)
        for chunk, tags in parse_markup(markup):
            if chunk == "\n":
                p = tf.add_paragraph(); p.alignment = ALIGN[align]; p.line_spacing = Pt(size_px / 2 * lh)
                continue
            fam_role, wgt, sty, up, col = role, base_w, base_style, upper, default_color
            if "b" in tags or "strong" in tags:
                wgt = 700
            if "sbi" in tags:
                wgt, sty = 600, "italic"
            if "em" in tags:
                if role == "display":
                    wgt, sty = 300, "italic"
                elif role == "sans":
                    fam_role, wgt, sty, up = "serif", 400, "italic", False
                    if st.get("group") == "Títulos" and style.startswith("pillar"):
                        wgt = 800
                else:
                    sty = "italic"
                col = em_color or col
            if "i" in tags:
                if role == "display":
                    fam_role, wgt, sty, up = "serif", 400, "italic", False
                else:
                    fam_role, sty, up = "serif", "italic", False
                col = em_color or col
            info = self.font_for(self.family(fam_role), wgt, sty)
            r = p.add_run()
            r.text = chunk.upper() if up else chunk
            f = r.font
            f.name = info["name"]
            f.bold = info["bold"]
            f.italic = info["italic"]
            f.size = Pt(size_px / 2)
            hexv, alpha = self.color(col, theme)
            f.color.rgb = RGBColor.from_string(hexv)
            rpr = r._r.get_or_add_rPr()
            spc = st["letter_spacing_em"] * size_px / 2 * 100
            if spc:
                rpr.set("spc", str(int(round(spc))))
            if alpha < 1:
                self._set_alpha(rpr, alpha)
        return tb

    # ------------------------------------------------------------- elementos
    def rect(self, slide, x, y, w, h, color, alpha=None):
        shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
        hexv, a = self.color(color, self.theme_of(slide)) if not color.startswith("#") else (color[1:], 1.0)
        shp.fill.solid(); shp.fill.fore_color.rgb = RGBColor.from_string(hexv)
        self._set_alpha(shp.fill._xPr, alpha if alpha is not None else a)
        shp.line.fill.background()
        shp.shadow.inherit = False
        return shp

    def rule(self, slide, x, y, w, color="rule", thickness=1):
        return self.rect(slide, x, y, w, thickness, color)

    def chrome(self, slide, color=None):
        """Marcas de borda: esquerda e direita, no meio da altura, a 27 px da borda, 6 pt."""
        bg = self._bg.get(slide.slide_id, "nevoa")
        color = color or {"laranja": "on-laranja", "ambar": "grafite", "grafite": "nevoa",
                          "foto": "nevoa"}.get(bg, "ink-muted")
        ch = self.o.get("chrome", {})
        inset = self.o["spacing_px"].get("stage-chrome", 27)
        hgt = 12 * 1.4
        self.text(slide, ch.get("left", "LIVEIDEA AG"), "chrome", x=inset, y=540 - hgt / 2, w=300, h=hgt,
                  color=color)
        if ch.get("right"):
            self.text(slide, ch["right"], "chrome", x=1920 - inset - 300, y=540 - hgt / 2, w=300, h=hgt,
                      color=color, align="right")

    def _render(self, name, args):
        out = self.png_dir / name
        if not out.exists():
            cmd = ["node", str(HERE / "render.js"), "--kit", str(self.kit), "--out", str(out)] + args
            subprocess.run(cmd, check=True)
        return out

    def logo(self, slide, variant, x, y, w):
        """Logo em PNG renderizado do SVG oficial. variant: nevoa, laranja ou grafite."""
        svg = self.kit / "assets" / "Logos" / f"liveidea-{variant}.svg"
        png = self._render(f"logo-{variant}.png", ["--svg", str(svg), "--width", "1600"])
        return slide.shapes.add_picture(str(png), E(x), E(y), width=E(w))

    def ghost(self, slide, markup, size=307):
        """Ghost como PNG transparente do tamanho do slide (regra do README para PowerPoint)."""
        key = re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", markup).lower()).strip("-")[:40]
        png = self._render(f"ghost-{key}-{int(size)}.png", ["--ghost", markup, "--size", str(size)])
        return slide.shapes.add_picture(str(png), 0, 0, width=E(1920), height=E(1080))

    def photo(self, slide, path, x, y, w, h, focus=(0.5, 0.5), veil=None, fade=None):
        """Foto em quadro reto, recorte cover. veil: 'leve' | 'denso'. fade: 'base' (degradê até shade)."""
        from PIL import Image
        iw, ih = Image.open(path).size
        pic = slide.shapes.add_picture(str(path), E(x), E(y), E(w), E(h))
        fr, ir = w / h, iw / ih
        if ir > fr:  # imagem mais larga: corta laterais
            keep = fr / ir; extra = 1 - keep
            pic.crop_left = extra * focus[0]; pic.crop_right = extra * (1 - focus[0])
        else:
            keep = ir / fr; extra = 1 - keep
            pic.crop_top = extra * focus[1]; pic.crop_bottom = extra * (1 - focus[1])
        if veil:
            self.rect(slide, x, y, w, h, "veu-" + veil)
        if fade == "base":
            self._fade(slide, x, y, w, h)
        return pic

    def _fade(self, slide, x, y, w, h):
        shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
        shp.line.fill.background(); shp.shadow.inherit = False
        hexv, a = self.color("shade")
        spPr = shp.fill._xPr
        for el in list(spPr):
            if el.tag in (qn("a:solidFill"), qn("a:noFill"), qn("a:gradFill")):
                spPr.remove(el)
        grad = spPr.makeelement(qn("a:gradFill"), {"rotWithShape": "1"})
        lst = grad.makeelement(qn("a:gsLst"), {})
        for pos, alpha in ((0, 0), (100000, int(a * 100000))):
            gs = lst.makeelement(qn("a:gs"), {"pos": str(pos)})
            clr = gs.makeelement(qn("a:srgbClr"), {"val": hexv})
            clr.append(clr.makeelement(qn("a:alpha"), {"val": str(alpha)}))
            gs.append(clr); lst.append(gs)
        grad.append(lst)
        grad.append(grad.makeelement(qn("a:lin"), {"ang": "5400000", "scaled": "0"}))
        geom = spPr.find(qn("a:prstGeom"))
        geom.addnext(grad)
        return shp

    def eyebrow(self, slide, number, name, x, y, tone=None):
        """01 · INSIGHT. tone: None (ink/grafite) ou 'ambar' (sobre foto e grafite)."""
        label = (f"{int(number):02d} · " if number is not None else "") + name.upper()
        return self.text(slide, label, "eyebrow", x=x, y=y, w=900, color=tone or "ink", wrap=False)

    def stat(self, slide, value, label, x, y, w, size="m", unit=None, note=None, subtitle=None, rule=True):
        """Número (PP Editorial New, âmbar) à direita e rótulo (Aeonik Bold, ink) à esquerda, fio embaixo.
        Estimativas de proposta: passe note='PÚBLICO ESTIMADO'."""
        st = {"m": "stat-m", "l": "stat-l", "xl": "stat-xl"}[size]
        num_px = self.o["styles"][st]["size_px"]
        num = value + (f" <em>{unit}</em>" if unit else "")
        hgt = num_px * 1.1
        self.text(slide, label.upper(), "label", x=x, y=y + hgt - 22, w=w * 0.5, color="ink")
        self.text(slide, num, st, x=x + w * 0.35, y=y, w=w * 0.65, h=hgt, color="accent-number",
                  em_color="accent-number", align="right")
        yy = y + hgt + 8
        if note:
            self.text(slide, note.upper(), "label-s", x=x, y=yy, w=w, color="ink-muted"); yy += 24
        if subtitle:
            self.text(slide, subtitle, "stat-subtitle" if size == "xl" else "stat-subtitle-s", x=x, y=yy, w=w)
            yy += 70
        if rule:
            self.rule(slide, x, yy, w)
        return yy

    # --------------------------------------------------------------- modelos
    def capa_padrao(self):
        """Capa padrão: laranja, logo névoa pequeno no centro, assinatura no Ghost, marcas em névoa."""
        s = self.slide("laranja")
        self.ghost(s, "<b>IDEIAS </b><em>QUE</em> GANHAM <b>VIDA</b>", 280)
        self.logo(s, "nevoa", 866, 517, 187)
        self.chrome(s)
        return s

    def capa_projeto(self, titulo, destaque, ghost, ghost_size=307, cliente_logo=None):
        """Capa do projeto: logo no topo, título em duas vozes (Aeonik Bold névoa + serifa grafite, 108 px),
        conceito no Ghost. A marca do cliente, se entrar, é o arquivo oficial (cliente_logo)."""
        s = self.slide("laranja")
        self.ghost(s, ghost, ghost_size)
        self.logo(s, "nevoa", 866, 250, 187)
        self.text(s, f"{titulo}<br><em>{destaque}</em>", "headline-statement", x=160, y=380, w=1600, h=260,
                  size=108, color="nevoa", em_color="grafite", align="center", uppercase=True)
        if cliente_logo:
            from PIL import Image
            iw, ih = Image.open(cliente_logo).size
            hh = 60; ww = hh * iw / ih
            s.shapes.add_picture(str(cliente_logo), E((1920 - ww) / 2), E(700), height=E(hh))
        self.chrome(s)
        return s

    def abertura(self, titulo, destaque, ghost, ghost_size=361):
        """Abertura de capítulo: laranja, título em duas vozes centralizado, frase do capítulo no Ghost."""
        s = self.slide("laranja")
        self.ghost(s, ghost, ghost_size)
        self.text(s, f"{titulo}<br><em>{destaque}</em>", "headline-statement", x=160, y=330, w=1600, h=260,
                  size=108, color="nevoa", em_color="grafite", align="center", uppercase=True)
        self.chrome(s)
        return s

    def peca(self, path):
        """Página de peça: KV, mockup ou render em página inteira, sem texto e sem marcas de borda."""
        s = self.slide("grafite")
        self.photo(s, path, 0, 0, 1920, 1080)
        return s

    def fechamento(self, palavra):
        """Fechamento: a palavra do conceito em serifa itálica 300 px névoa, logo névoa, assinatura no Ghost."""
        s = self.slide("laranja")
        self.ghost(s, "<b>IDEIAS </b><em>QUE</em> GANHAM <b>VIDA</b>", 280)
        self.text(s, f"<i>{palavra}</i>", "serif-display", x=60, y=274, w=1800, h=300, size=300,
                  color="nevoa", em_color="nevoa", align="center", line_height=0.9)
        self.logo(s, "nevoa", 866, 641, 187)
        self.chrome(s)
        return s

    def save(self, path):
        self.prs.save(path)
        print(f"Apresentação salva em {path} (design system LIVEIDEA v{self.version}, commit {self.o.get('commit')})")
        return path
