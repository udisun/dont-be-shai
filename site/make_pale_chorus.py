#!/usr/bin/env python3
"""Derives site/programmes/pale-chorus.html from the standalone report.html.

The standalone report is the source of truth. This adds only what the site version
needs: a breadcrumb back to the registry and the shared colophon.
"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "report.html").read_text(encoding="utf-8")

CSS = """
/* ---------- registry integration ---------- */
.crumb{font-family:var(--mono);font-size:12px;letter-spacing:.02em;
  padding:18px 0 0;color:var(--muted);display:flex;gap:10px;flex-wrap:wrap}
.crumb a{color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule-strong)}
.crumb a:hover{color:var(--accent);border-bottom-color:var(--accent)}
.crumb span::before{content:"/ "}
.colophon{border-top:2px solid var(--ink);padding:22px 0 40px;font-size:13.5px;
  color:var(--muted);line-height:1.6;max-width:64ch}
.colophon strong{color:var(--ink-2)}
.colophon .src{font-family:var(--mono);font-size:12px;margin:0}
@media print{.crumb{display:none}}
"""
out = src.replace("</style>", CSS + "</style>", 1)
out = out.replace('<div class="sheet">\n\n  <!-- ============ COVER ============ -->',
"""<div class="sheet">

  <div class="pad">
    <nav class="crumb"><a href="../index.html">Central Declassification Registry</a>
      <span>Programme Pale Chorus</span></nav>
  </div>

  <!-- ============ COVER ============ -->""", 1)

foot = """      This assessment contains no information damaging to national security and quite a lot damaging to Shai.
    </div>"""
out = out.replace(foot, foot + """
    <div class="colophon">
      <p><strong>About this registry.</strong> The Central Declassification Registry is a work of
      fiction. The offices do not exist and the other programmes do not exist.</p>
      <p>This page is the exception. The songs below are real, collected from MusicBrainz and
      linked to their recordings. The conclusions drawn from them are not.</p>
      <p class="src">Source and build scripts: <a href="https://github.com/udisun/dont-be-shai">github.com/udisun/dont-be-shai</a></p>
    </div>""", 1)

(ROOT / "site" / "programmes" / "pale-chorus.html").write_text(out, encoding="utf-8")
print("wrote site/programmes/pale-chorus.html", len(out), "bytes")
