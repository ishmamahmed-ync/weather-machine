"""Inline the design system into a page at build time.

Every page in this project is one self-contained HTML file that must work from
file:// (CLAUDE.md), so pages never <link> to wm.css. A template marks where the
system goes, and its build script calls inline() before writing the page:

    <style>/*__WM_CSS__*/ ... page styles ... </style>     wm.css goes here
    <script>/*__WM_JS__*/</script>                          wm.js goes here

    import sys; sys.path.insert(0, str(ROOT / "design-system"))
    from inline import inline
    page = inline(page)

Give the page's <body> the class "wm" to get the base styles.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKENS = {"/*__WM_CSS__*/": HERE / "wm.css", "/*__WM_JS__*/": HERE / "wm.js"}


def inline(page: str) -> str:
    for token, path in TOKENS.items():
        if token in page:
            page = page.replace(token, path.read_text())
    return page
