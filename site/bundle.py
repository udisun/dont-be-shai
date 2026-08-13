#!/usr/bin/env python3
"""Flattens the multi-page registry into one self-contained HTML file for previewing.

The published site is site/index.html plus site/programmes/*.html. This bundles them
into a single file with hash routing so it can be opened or shared as one page.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "registry-preview.html"

def sheet(html):
    i = html.index('<div class="sheet">') + len('<div class="sheet">')
    j = html.rindex('</div>', i, html.index('<div class="band">', i))
    return html[i:j]

def styles(html):
    return "\n".join(m.group(1) for m in re.finditer(r"<style>(.*?)</style>", html, re.S))

def scripts(html):
    out = []
    for m in re.finditer(r'<script([^>]*)>(.*?)</script>', html, re.S):
        out.append((m.group(1), m.group(2)))
    return out

pages = [("index", ROOT / "index.html", "Registry")]
for p in sorted((ROOT / "programmes").glob("*.html")):
    if p.stem == "pale-chorus":
        continue
    pages.append((p.stem, p, None))
pages.insert(1, ("pale-chorus", ROOT / "programmes" / "pale-chorus.html", None))

css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
report_html = (ROOT / "programmes" / "pale-chorus.html").read_text(encoding="utf-8")
css += "\n" + styles(report_html)

sections, navlinks = [], []
for slug, path, label in pages:
    h = path.read_text(encoding="utf-8")
    body = sheet(h)
    body = body.replace('href="../index.html"', 'href="#index"')
    body = re.sub(r'href="(?:\./)?programmes/([a-z-]+)\.html"', r'href="#\1"', body)
    body = re.sub(r'href="([a-z-]+)\.html"', r'href="#\1"', body)
    title = label or re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip()
    sections.append(f'<section class="route" id="route-{slug}" data-title="{title}">{body}</section>')
    navlinks.append(f'<a href="#{slug}" data-r="{slug}">{title.replace("Programme ","")}</a>')

extra_css = """
.route{display:none}
.route.on{display:block}
.rv{opacity:1 !important;transform:none !important}
.pnav{position:sticky;top:0;z-index:30;background:var(--surface-2);
  border-bottom:1px solid var(--rule-strong);display:flex;gap:0;overflow-x:auto;
  scrollbar-width:thin}
.pnav a{flex:0 0 auto;font-family:var(--mono);font-size:10.5px;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2);text-decoration:none;
  padding:9px 14px;border-right:1px solid var(--rule);white-space:nowrap}
.pnav a:hover{color:var(--accent);background:var(--accent-wash)}
.pnav a.on{color:var(--surface);background:var(--accent)}
.pnav a:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
"""

body_scripts = "\n".join(
    f"<script{a}>{b}</script>" for a, b in scripts(report_html))

router = """
<script>
(function(){
  var routes=[].slice.call(document.querySelectorAll('.route'));
  var tabs=[].slice.call(document.querySelectorAll('.pnav a'));
  function show(slug){
    var found=false;
    routes.forEach(function(r){
      var on=r.id==='route-'+slug;
      r.classList.toggle('on',on); if(on) found=true;
    });
    if(!found){ document.getElementById('route-index').classList.add('on'); slug='index'; }
    tabs.forEach(function(t){ t.classList.toggle('on', t.dataset.r===slug); });
    if(slug==='pale-chorus'){
      if(window.__growBars) window.__growBars();
      if(window.__drawLine) window.__drawLine();
    }
    window.scrollTo(0,0);
  }
  window.addEventListener('hashchange',function(){ show(location.hash.slice(1)||'index'); });
  show(location.hash.slice(1)||'index');
})();
</script>
"""

OUT.write_text(f"""<title>Central Declassification Registry</title>
<style>
{css}
{extra_css}
</style>
<div class="band top">Unclassified // Released in full // Public reading room</div>
<nav class="pnav">{''.join(navlinks)}</nav>
<div class="sheet">
{''.join(sections)}
</div>
<div class="band">Unclassified // Released in full // Registry updated continuously</div>
{body_scripts}
{router}
""", encoding="utf-8")
print("wrote", OUT, OUT.stat().st_size, "bytes,", len(pages), "routes")
