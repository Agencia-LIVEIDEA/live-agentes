#!/usr/bin/env python3
"""Monta o kit de aplicação do design system LIVEIDEA a partir de design-system/ (tokens.json,
fontes e assets). Tudo é derivado dos arquivos da versão baixada: nada de valor fixo aqui.

Saída em --out:
  manifest.json      versão, commit, origem e data de geração do kit
  tokens.css         variáveis CSS (temas Claro e Grafite) + classes .ts-<estilo> de tipografia
  fonts.css          @font-face apontando para fonts/ (HTML com arquivos ao lado)
  fonts-inline.css   @font-face com as fontes embutidas em base64 (HTML de arquivo único)
  fonts/             as .woff2 da versão
  fonts-ttf/         as mesmas fontes em .ttf/.otf (precisa de fontTools + brotli) para instalar
  office.json        cores em hex, estilos em pt (PowerPoint e Word), nomes de fonte do Office, grid
  assets/            Logos e Icones copiados (fotos e capas ficam em design-system/assets)
  components/        bundle.js, bundle.css, index.d.ts

Uso:
  python3 build_kit.py --ds <repo>/design-system --out <kit> [--commit X] [--source Y]
  python3 build_kit.py --install-fonts --out <kit>   # instala fonts-ttf no usuário (fc-cache)
"""
import argparse, base64, datetime, json, os, re, shutil, subprocess, sys
from pathlib import Path

SNAPSHOT = Path(__file__).resolve().parent.parent / "snapshot"  # cópia do design system que vem no ZIP da skill
BUNDLED_FONTS = SNAPSHOT / "design-system" / "fonts"
PX_PER_PT = 2.0          # palco 1920 px = slide 16:9 de 960 pt  ->  2 px = 1 pt (regra do README)
PX_PER_IN = 144.0        # 1920 px = 13,333 in


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def resolve(value, base, theme):
    """Resolve referências {nome} e valores por tema para um valor CSS concreto."""
    if isinstance(value, dict):
        value = value.get(theme, value.get("light"))
    m = re.fullmatch(r"\{([\w-]+)\}", str(value))
    if m:
        return resolve(base[m.group(1)], base, theme)
    return value


def css_color_to_office(v):
    v = v.strip()
    if v.startswith("#"):
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return {"hex": h[:6].upper(), "alpha": 1.0}
    m = re.fullmatch(r"rgba?\(([^)]+)\)", v)
    if m:
        parts = [p.strip() for p in m.group(1).split(",")]
        r, g, b = (int(float(x)) for x in parts[:3])
        a = float(parts[3]) if len(parts) > 3 else 1.0
        return {"hex": f"{r:02X}{g:02X}{b:02X}", "alpha": a}
    return {"css": v}


def px(v):
    return float(str(v).replace("px", "")) if v not in (None, "") else None


def em(v):
    s = str(v)
    return float(s.replace("em", "")) if s.endswith("em") else (0.0 if s in ("0", "") else float(s))


def font_path(ds, f):
    """Arquivo da fonte: o da versão baixada; se faltar (ex.: conector que só lê texto), o do pacote da skill."""
    p = ds / f["file"]
    if p.exists():
        return p
    b = BUNDLED_FONTS / Path(f["file"]).name
    return b if b.exists() else p


def office_font_names(ds, fonts):
    """Lê na tabela 'name' de cada fonte o nome de família que o Office usa (name ID 1) e se o
    arquivo é o par Bold/Italic dessa família. Sem fontTools, usa a convenção da Adobe."""
    out = {}
    try:
        from fontTools.ttLib import TTFont  # noqa
        have_ft = True
    except Exception:
        have_ft = False
    for f in fonts:
        key = f"{f['family']}|{f['weight']}|{f['style']}"
        path = font_path(ds, f)
        if have_ft and path.exists():
            try:
                t = TTFont(str(path))
                n = t["name"]
                fam = n.getDebugName(1)
                sub = (n.getDebugName(2) or "Regular").lower()
                out[key] = {"name": fam, "bold": "bold" in sub, "italic": "italic" in sub,
                            "file": f["file"], "postscript": n.getDebugName(6)}
                continue
            except Exception:
                pass
        out[key] = {"name": f["family"], "bold": str(f["weight"]).startswith("7"),
                    "italic": f["style"] == "italic", "file": f["file"], "guess": True}
    return out, have_ft


def pick_font(font_map, family, weight, style):
    """Escolhe o arquivo mais próximo do peso/estilo pedido dentro da família."""
    best, score = None, None
    for key, info in font_map.items():
        fam, w, st = key.split("|")
        if fam != family:
            continue
        ws = [int(x) for x in w.split()]
        d = min(abs(int(weight) - x) for x in ws) + (0 if st == style else 1000)
        if score is None or d < score:
            best, score = info, d
    return best


def chrome_text(ds):
    """Textos das marcas de borda, lidos do componente Chrome (o ano muda todo ano)."""
    js = ds / "components" / "bundle.js"
    left, right = "LIVEIDEA AG", None
    if js.exists():
        src = js.read_text(encoding="utf-8")
        m = re.search(r"p\.left == null \? '([^']*)'", src)
        n = re.search(r"p\.right == null \? '([^']*)'", src)
        left = m.group(1) if m else left
        right = n.group(1) if n else None
    return {"left": left, "right": right}


def _bundled_version():
    v = SNAPSHOT / "VERSION"
    return v.read_text(encoding="utf-8").strip() if v.exists() else "versão não registrada"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds")
    ap.add_argument("--out", required=True)
    ap.add_argument("--commit", default="desconhecido")
    ap.add_argument("--source", default="desconhecida")
    ap.add_argument("--install-fonts", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)

    if a.install_fonts:
        src = out / "fonts-ttf"
        if not src.is_dir() or not any(src.iterdir()):
            sys.exit("fonts-ttf/ vazio: rode o build com fontTools e brotli instalados (pip install fonttools brotli).")
        dest = Path.home() / ".local/share/fonts/liveidea"
        dest.mkdir(parents=True, exist_ok=True)
        for f in src.iterdir():
            shutil.copy2(f, dest / f.name)
        subprocess.run(["fc-cache", "-f", str(dest)], check=False, capture_output=True)
        print(f"Fontes instaladas em {dest}")
        return

    ds = Path(a.ds)
    tokens = load(ds / "tokens.json")
    meta = tokens.get("meta", {})
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # ---------- cores ----------
    ctoks = tokens["color"]["tokens"]
    base = {t["name"]: t["value"] for t in ctoks}
    themes = [t["id"] for t in tokens["color"].get("themes", [{"id": "light"}])]
    colors = {th: {n: resolve(v, base, th) for n, v in base.items()} for th in themes}

    # ---------- tipografia ----------
    fams = tokens["type"]["families"]
    fonts = tokens["type"]["fonts"]
    role_family = {}
    for role, stack in fams.items():
        first = re.split(r",", stack)[0].strip().strip('"')
        role_family[role] = first
    font_map, have_ft = office_font_names(ds, fonts)

    styles = {}
    for g in tokens["type"]["groups"]:
        role = g.get("family")
        for s in g.get("tokens", g.get("styles", [])):
            fam_role = s.get("family", role)
            weight = int(s.get("fontWeight", 400))
            style = s.get("fontStyle", "normal")
            size = px(s.get("fontSize"))
            office = pick_font(font_map, role_family.get(fam_role, ""), weight, style) or {}
            styles[s["name"]] = {
                "group": g.get("name"), "role": fam_role, "family": role_family.get(fam_role),
                "css_stack": fams.get(fam_role), "size_px": size,
                "size_pt": round(size / PX_PER_PT, 2) if size else None,
                "line_height": s.get("lineHeight"), "letter_spacing_em": em(s.get("letterSpacing", "0")),
                "weight": weight, "style": style,
                "office_font": office.get("name"), "office_bold": office.get("bold", False),
                "office_italic": office.get("italic", style == "italic"),
                "usage": s.get("usage", ""), "sample": s.get("sample", ""),
            }

    def tok_list(group):
        return {t["name"]: t["value"] for t in tokens.get(group, {}).get("tokens", [])}
    spacing, radius, shadow, opacity = (tok_list(k) for k in ("spacing", "radius", "shadow", "opacity"))

    # ---------- tokens.css ----------
    def var_block(th):
        lines = [f"  --{n}: {v};" for n, v in colors[th].items()]
        return "\n".join(lines)
    css = [f"/* LIVEIDEA design system v{meta.get('release','?')} · commit {a.commit} · gerado de tokens.json. Não edite: rode sync_ds.sh. */",
           ":root {", "  color-scheme: light;", var_block("light")]
    for role, stack in fams.items():
        css.append(f"  --font-{role}: {stack};")
    for grp in (spacing, radius, shadow, opacity):
        for n, v in grp.items():
            css.append(f"  --{n}: {v};")
    css.append("}")
    if "dark" in colors:
        css += ['[data-theme="dark"], .li-theme-dark {', "  color-scheme: dark;", var_block("dark"), "}"]
    css.append("/* Estilos de texto: .ts-<nome do token> */")
    for n, s in styles.items():
        decl = [f"font-family: var(--font-{s['role']})", f"font-size: {s['size_px']:g}px",
                f"line-height: {s['line_height']}", f"letter-spacing: {s['letter_spacing_em']:g}em",
                f"font-weight: {s['weight']}", f"font-style: {s['style']}"]
        if s["role"] == "display":
            decl.append("text-transform: uppercase")
        css.append(f".ts-{n} {{ {'; '.join(decl)}; }}")
    (out / "tokens.css").write_text("\n".join(css) + "\n", encoding="utf-8")

    # ---------- fontes ----------
    (out / "fonts").mkdir()
    face, face_inline = [], []
    missing = [f["file"] for f in fonts if not font_path(ds, f).exists()]
    from_skill = [f["file"] for f in fonts if not (ds / f["file"]).exists() and font_path(ds, f).exists()]
    if from_skill:
        print(f"Aviso: {len(from_skill)} fonte(s) ausentes na versão baixada; usando as do pacote da skill "
              f"({_bundled_version()}).", file=sys.stderr)
    if missing:
        print(f"Aviso: {len(missing)} arquivo(s) de fonte ausentes ({', '.join(missing[:3])}...). "
              "HTML e PNG vão cair nas fontes de reserva.", file=sys.stderr)
    fonts_present = [f for f in fonts if font_path(ds, f).exists()]
    for f in fonts_present:
        src = font_path(ds, f)
        shutil.copy2(src, out / "fonts" / src.name)
        common = (f"font-family: \"{f['family']}\"; font-weight: {f['weight']}; "
                  f"font-style: {f['style']}; font-display: swap;")
        face.append(f"@font-face {{ {common} src: url(\"fonts/{src.name}\") format(\"woff2\"); }}")
        b64 = base64.b64encode(src.read_bytes()).decode()
        face_inline.append(f"@font-face {{ {common} src: url(data:font/woff2;base64,{b64}) format(\"woff2\"); }}")
    (out / "fonts.css").write_text("\n".join(face) + "\n", encoding="utf-8")
    (out / "fonts-inline.css").write_text("\n".join(face_inline) + "\n", encoding="utf-8")

    ttf_dir = out / "fonts-ttf"
    ttf_dir.mkdir()
    ttf_ok = False
    if have_ft:
        try:
            from fontTools.ttLib import TTFont
            for f in fonts_present:
                t = TTFont(str(font_path(ds, f)))
                t.flavor = None
                ext = ".otf" if "CFF " in t or "CFF2" in t else ".ttf"
                t.save(str(ttf_dir / (Path(f["file"]).stem + ext)))
            ttf_ok = True
        except Exception as e:  # brotli ausente, por exemplo
            print(f"Aviso: não converti as fontes para TTF/OTF ({e}). pip install fonttools brotli", file=sys.stderr)

    # ---------- assets e componentes ----------
    for grp in ("Logos", "Icones"):
        if (ds / "assets" / grp).is_dir():
            shutil.copytree(ds / "assets" / grp, out / "assets" / grp)
    if (ds / "components").is_dir():
        (out / "components").mkdir()
        for n in ("bundle.js", "bundle.css", "index.d.ts"):
            if (ds / "components" / n).exists():
                shutil.copy2(ds / "components" / n, out / "components" / n)

    # ---------- office.json ----------
    office = {
        "version": meta.get("release"), "commit": a.commit,
        "slide": {"width_in": 13.333, "height_in": 7.5, "stage_px": [1920, 1080],
                  "px_per_pt": PX_PER_PT, "px_per_in": PX_PER_IN},
        "colors": {th: {n: css_color_to_office(str(v)) for n, v in cs.items()} for th, cs in colors.items()},
        "styles": styles,
        "fonts": font_map,
        "spacing_px": {n: px(v) for n, v in spacing.items()},
        "radius": radius, "opacity": {n: float(v) for n, v in opacity.items()},
        "font_names_from_files": have_ft,
        "chrome": chrome_text(ds),
    }
    (out / "office.json").write_text(json.dumps(office, ensure_ascii=False, indent=2), encoding="utf-8")

    manifest = {"version": meta.get("release"), "commit": a.commit, "source": a.source,
                "tokens_revised": meta.get("revised"),
                "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                "ds_dir": str(ds.resolve()), "fonts_ttf": ttf_ok,
                "fonts_from_skill_package": from_skill, "fonts_missing": missing}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Kit LIVEIDEA v{manifest['version']} ({a.commit}) em {out}"
          + ("" if have_ft else " · nomes de fonte do Office estimados (instale fonttools)"))


if __name__ == "__main__":
    main()
