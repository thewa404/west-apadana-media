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
