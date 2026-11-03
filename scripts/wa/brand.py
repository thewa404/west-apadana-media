"""Brand config, font CSS and contrast helpers."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load(name):
    return json.loads((ROOT / "config" / f"{name}.json").read_text())


BRAND = load("brand")


def font_css():
    faces = []
    for spec in BRAND["fonts"].values():
        for weight, fname in spec["files"].items():
            p = ROOT / "fonts" / fname
            if not p.exists():
                raise FileNotFoundError(f"missing font file {p}")
            fmt = "opentype" if fname.endswith(".otf") else "truetype"
            style = "italic" if weight.endswith("i") else "normal"  # key "400i" = weight 400, italic face
            faces.append(
                f"@font-face{{font-family:'{spec['family']}';font-weight:{weight.rstrip('i')};font-style:{style};"
                f"src:url('file://{p}') format('{fmt}');}}"
            )
    return "\n".join(faces)


def _lin(v):
    v /= 255
    return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4


def luminance(hexcolor):
    h = hexcolor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def check_palette():
    """Contrast ratio for every approved text/background pair."""
    colors = {**BRAND["colors"], **BRAND["extra_colors"]}
    out = []
    for fg, bg in BRAND["approved_text_pairs"]:
        ratio = contrast(colors[fg], colors[bg])
        out.append({"fg": fg, "bg": bg, "ratio": round(ratio, 2), "ok": ratio >= BRAND["min_text_contrast"]})
    return out
