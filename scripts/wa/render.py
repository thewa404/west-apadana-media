"""Render Jinja2 HTML templates to PNG/JPEG stills with Playwright (Chromium)."""
import pathlib

import jinja2
from markupsafe import Markup, escape
from playwright.sync_api import sync_playwright

from . import brand

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(brand.ROOT / "templates")),
    autoescape=jinja2.select_autoescape(["html", "j2"]),
)


def mark(text):
    """'Make *this* word gold' -> <em> accent span, HTML-escaped."""
    parts = str(escape(text)).split("*")
    return Markup("".join(f"<em>{p}</em>" if i % 2 else p for i, p in enumerate(parts)))


env.filters["mark"] = mark


def context(extra, size):
    base = dict(
        font_css=Markup(brand.font_css()),
        c=brand.BRAND["colors"],
        extra=brand.BRAND["extra_colors"],
        w=size[0],
        h=size[1],
        handle=brand.BRAND["handle"],
        studio=brand.BRAND["name"],
    )
    base.update(extra)
    return base


class Renderer:
    """Context manager holding one Chromium instance for many renders."""

    def __enter__(self):
        self._p = sync_playwright().start()
        self._b = self._p.chromium.launch()
        return self

    def __exit__(self, *exc):
        self._b.close()
        self._p.stop()

    def page(self, size):
        return self._b.new_page(viewport={"width": size[0], "height": size[1]}, device_scale_factor=1)

    def still(self, template, ctx, out, size=(1080, 1350), fmt="png", quality=92):
        out = pathlib.Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        html = env.get_template(template).render(**context(ctx, size))
        hp = out.with_suffix(".tmp.html")
        hp.write_text(html)
        pg = self.page(size)
        try:
            pg.goto(f"file://{hp}")
            pg.evaluate("document.fonts.ready")
            fonts_ok = pg.evaluate("""[...document.fonts].filter(f => f.status === 'error').length === 0 """
                """&& [...document.fonts].some(f => f.family.includes('Inter Display') && f.status === 'loaded')""")
            pg.wait_for_timeout(120)
            kw = {"path": str(out)}
            if fmt == "jpeg":
                kw.update(type="jpeg", quality=quality)
            pg.screenshot(**kw)
        finally:
            pg.close()
            hp.unlink(missing_ok=True)
        return {"out": str(out), "fonts_ok": bool(fonts_ok), "size": list(size)}


def _strip(self, template, ctx, out_prefix, n, size=(1080, 1350), fmt="jpeg", quality=94):
    """Render ONE continuous canvas n slides wide and cut it into n files, so elements can cross slide seams (carousel continuity)."""
    out_prefix = pathlib.Path(out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    wide = (size[0] * n, size[1])
    html = env.get_template(template).render(**context({**ctx, "n": n, "sw": size[0], "sh": size[1]}, size))
    hp = out_prefix.with_name(out_prefix.name + ".tmp.html")
    hp.write_text(html)
    pg = self.page(wide)
    outs = []
    try:
        pg.goto(f"file://{hp}")
        pg.evaluate("window.__ready || document.fonts.ready")
        pg.wait_for_timeout(250)
        for i in range(n):
            out = out_prefix.with_name(f"{out_prefix.name}_{i + 1}.{'jpg' if fmt == 'jpeg' else 'png'}")
            kw = {"path": str(out), "clip": {"x": i * size[0], "y": 0, "width": size[0], "height": size[1]}}
            if fmt == "jpeg":
                kw.update(type="jpeg", quality=quality)
            pg.screenshot(**kw)
            outs.append(str(out))
    finally:
        pg.close()
        hp.unlink(missing_ok=True)
    return outs


Renderer.strip = _strip
