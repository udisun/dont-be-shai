#!/usr/bin/env python3
"""Builds the Central Declassification Registry: an index plus one page per programme.

Everything on this site is invented except Pale Chorus, whose song data is real and
sourced from MusicBrainz. The colophon on every page says so.
"""
import html, os, pathlib

ROOT = pathlib.Path(__file__).parent
BAND_TOP = "Unclassified // Released in full"
BAND_BOT = "Public reading room"

def esc(s): return html.escape(s, quote=False)

# ---------------------------------------------------------------- programmes
P = [
 dict(slug="amber-vestibule", name="Amber Vestibule",
      office="Office of Vertical Transit Integrity", years="1974-2026", status="Active",
      title="The lift doors that close as you approach",
      deck="A study of door-close timing in relation to approaching foot traffic, and why the "
           "interval shortens when the approach is hurried.",
      kj=["We assess with high confidence that lift doors complete closure at a measurably faster "
          "rate when a person is visibly hurrying toward them. Across observed closures, the "
          "interval contracted whenever the approaching party broke into a jog.",
          "We assess with moderate confidence that the effect is strongest when the approaching "
          "party is carrying something in both hands, and absent entirely when they are early."],
      stats=[("Closures observed","41,208","across 96 buildings"),
             ("Mean interval, walking","4.1s","from first sighting"),
             ("Mean interval, running","1.9s","same distance")],
      chart=("Door-close interval by approach speed, seconds",
             [("Strolling",4.8),("Walking",4.1),("Brisk",3.2),("Hurrying",2.4),("Running",1.9),
              ("Calling out",1.4),("Both hands full",1.1)]),
      bottom="The programme is efficient, well resourced and entirely unaccountable. Occupants "
             "report that the doors reopen readily for anyone who does not need them to."),

 dict(slug="quiet-ledger", name="Quiet Ledger",
      office="Bureau of Conversational Flow", years="2009-2026", status="Active",
      title="The group chat that falls silent after your long message",
      deck="An assessment of message length against subsequent thread activity, and the "
           "reliability of the silence that follows a considered contribution.",
      kj=["We assess with high confidence that thread activity declines sharply following any "
          "message exceeding four lines. The decline is immediate and does not recover within "
          "the same hour.",
          "We assess with high confidence that the thread resumes normal volume within minutes of "
          "an unrelated party posting a single reaction image."],
      stats=[("Threads sampled","6,340","across nine platforms"),
             ("Silence after 4+ lines","83%","within two minutes"),
             ("Median recovery","41 min","or one reaction image")],
      chart=("Replies within ten minutes, by message length in lines",
             [("1 line",9.2),("2 lines",8.1),("3 lines",6.4),("4 lines",3.8),("5 lines",1.6),
              ("6 lines",0.7),("7+ lines",0.3)]),
      bottom="Participants consistently report that the message was fine and that everyone was "
             "simply busy. The programme relies on this explanation and has done so since 2009."),

 dict(slug="tepid-meridian", name="Tepid Meridian",
      office="Directorate of Ambient Comfort", years="1981-2026", status="Active",
      title="The office temperature that satisfies no one",
      deck="A review of shared thermostat settings and the mathematical impossibility of the "
           "consensus they are said to represent.",
      kj=["We assess with high confidence that no shared thermostat setting has ever produced "
          "simultaneous satisfaction in more than two occupants of the same room.",
          "We assess with moderate confidence that the setting drifts toward whichever value "
          "displeases the greatest number, and that no individual has ever been observed "
          "adjusting it."],
      stats=[("Rooms surveyed","2,714","in eleven climates"),
             ("Reported as correct","0.4%","of occupant-days"),
             ("Cardigans present","94%","of surveyed rooms")],
      chart=("Occupants describing the room as correct, by setting in Celsius",
             [("19",0.4),("20",1.1),("21",2.0),("22",2.4),("23",1.7),("24",0.9),("25",0.3)]),
      bottom="The programme has achieved a stable equilibrium in which everyone is slightly wrong. "
             "This office assesses that outcome as deliberate."),

 dict(slug="brief-candle", name="Brief Candle",
      office="Office of Portable Power Assurance", years="2007-2026", status="Active",
      title="The battery that falls from forty percent to nothing",
      deck="An assessment of the non-linear discharge interval and its correlation with the "
           "importance of the call in progress.",
      kj=["We assess with high confidence that the interval between forty percent and shutdown is "
          "not proportional to the interval between one hundred and forty percent, and that the "
          "discrepancy widens when the device is away from a charger.",
          "We assess with moderate confidence that the rate is sensitive to context, accelerating "
          "during navigation, boarding passes and calls the user did not want to take twice."],
      stats=[("Discharge events","18,900","logged"),
             ("100 to 40 percent","6h 12m","median"),
             ("40 percent to zero","19 min","same devices")],
      chart=("Median minutes per ten percent of charge remaining",
             [("100-90",62),("90-80",59),("80-70",57),("70-60",54),("60-50",48),("50-40",41),
              ("40-30",14),("30-20",9),("20-10",5),("10-0",3)]),
      bottom="The programme is most active when the user is furthest from a plug. This office "
             "considers the correlation established and the mechanism unexplained."),

 dict(slug="slow-orchard", name="Slow Orchard",
      office="Bureau of Queue Equity", years="1968-2026", status="Active",
      title="The other queue, which is moving",
      deck="A longitudinal study of relative queue velocity and the reliable underperformance of "
           "the queue actually joined.",
      kj=["We assess with high confidence that the selected queue advances more slowly than at "
          "least one adjacent queue, and that the disparity becomes apparent within ninety "
          "seconds of committing to a choice.",
          "We assess with high confidence that switching queues transfers the property to the new "
          "queue rather than resolving it."],
      stats=[("Queue-hours logged","52,000","retail and transit"),
             ("Chosen queue slower","71%","of observations"),
             ("Switching improved things","8%","of attempts")],
      chart=("Outcome after switching queues, percent of attempts",
             [("Much worse",34),("Worse",29),("No change",21),("Better",8),("Much better",0.4),
              ("Original queue closed",7)]),
      bottom="The programme predates commercial computing and has adapted to self-checkout without "
             "difficulty. No countermeasure has ever been demonstrated."),

 dict(slug="hollow-counsel", name="Hollow Counsel",
      office="Directorate of Meeting Outcomes", years="1994-2026", status="Active",
      title="The circling back that never arrives",
      deck="An assessment of stated intentions to revisit a topic, and the observed frequency "
           "with which the topic is revisited.",
      kj=["We assess with high confidence that the phrase indicating a topic will be revisited is "
          "a terminal event. In the sampled record the topic was not raised again.",
          "We assess with moderate confidence that the topic recurs only when raised by the party "
          "who originally raised it, at which point it is described as a good point and deferred."],
      stats=[("Commitments logged","9,880","across 1,400 meetings"),
             ("Actually revisited","2.1%","within 90 days"),
             ("Described as a good point","97%","at the time")],
      chart=("Days elapsed before a deferred topic was raised again",
             [("Within 7",2.1),("8-30",1.4),("31-90",0.9),("91-365",0.6),("Over a year",0.3),
              ("Never",94.7)]),
      bottom="The programme requires no infrastructure and no funding. It operates entirely on "
             "the good faith of people who mean it at the time."),

 dict(slug="dim-parade", name="Dim Parade",
      office="Office of Signal Coordination", years="1972-2026", status="Active",
      title="The lights that know you are late",
      deck="A review of signal phasing along common commuter routes, indexed against the "
           "declared urgency of the journey.",
      kj=["We assess with high confidence that consecutive red signals cluster on journeys the "
          "traveller has described as urgent, and disperse on journeys with time in hand.",
          "We assess with low confidence in any mechanism. The correlation is robust; the means "
          "by which the network learns the traveller's schedule is not established."],
      stats=[("Journeys instrumented","11,400","in 38 cities"),
             ("Reds when unhurried","31%","of signals"),
             ("Reds when late","78%","same routes")],
      chart=("Consecutive red signals by declared urgency",
             [("No hurry",1.2),("Mild",2.0),("Somewhat late",3.4),("Late",5.1),
              ("Very late",6.8),("Airport",8.3)]),
      bottom="The programme is the only one in this registry with demonstrated predictive access "
             "to the traveller's calendar. This office finds that troubling and has said so."),

 dict(slug="still-water", name="Still Water",
      office="Bureau of Document Reproduction", years="1986-2026", status="Active",
      title="The printer that senses urgency",
      deck="An assessment of device failure rates against the time remaining before the printed "
           "document is required.",
      kj=["We assess with high confidence that mechanical failure rates rise as the deadline "
          "approaches, and that the device operates flawlessly during unscheduled test pages.",
          "We assess with moderate confidence that toner is reported as low at a level "
          "unconnected to the toner remaining."],
      stats=[("Print jobs observed","74,000","office devices"),
             ("Failure, no deadline","3%","of jobs"),
             ("Failure, under 10 min","61%","of jobs")],
      chart=("Jam rate by minutes remaining before the document is needed",
             [("Over 60",3),("31-60",6),("16-30",14),("6-15",38),("2-5",61),("Under 2",74)]),
      bottom="The device performs correctly for the technician every time. This office has "
             "stopped requesting the technician."),

 dict(slug="low-tide", name="Low Tide",
      office="Office of Retail Timing", years="1998-2026", status="Active",
      title="The discount that begins after you buy",
      deck="A study of price movement in the interval immediately following a completed purchase.",
      kj=["We assess with high confidence that the probability of a price reduction rises sharply "
          "in the days following a purchase, and that the reduction exceeds any available return "
          "window by a small and consistent margin.",
          "We assess with moderate confidence that the effect is amplified when the purchase was "
          "deliberated over for more than a week."],
      stats=[("Purchases tracked","23,700","online and in store"),
             ("Price fell within 30 days","64%","of purchases"),
             ("Median days after return window","2","days")],
      chart=("Days after purchase at which the price first fell",
             [("1-7",11),("8-14",17),("15-21",19),("22-28",22),("29-35",24),("36-60",7)]),
      bottom="No participant in this programme has ever successfully claimed the difference. The "
             "programme regards this as its core performance indicator."),
]

FLAG = dict(slug="pale-chorus", name="Pale Chorus",
            office="Office of Nominative Integrity", years="1968-2026", status="Active",
            title="The coordinated global effort to remove Shai from existence",
            deck="A fifty-eight-year campaign to eliminate persons designated Shai, conducted "
                 "through commercially released popular music.",
            stat=("195","songs catalogued"))

# ---------------------------------------------------------------- templates
def band(text, top=False):
    return f'<div class="band{" top" if top else ""}">{esc(text)}</div>'

def colophon(depth=0):
    up = "../" * depth
    return f"""  <div class="pad">
    <div class="colophon">
      <p><strong>About this registry.</strong> The Central Declassification Registry is a work of
      fiction, written as a joke. The offices do not exist, the programmes do not exist, and every
      figure on this page was invented for comic effect.</p>
      <p>One exception. The song data in <a href="{up}programmes/pale-chorus.html">Pale Chorus</a>
      is real: 195 songs, 149 artists, 1968 to 2026, collected from MusicBrainz and linked to their
      recordings. The conclusions drawn from it are not.</p>
      <p class="src">Source and build scripts: <a href="https://github.com/udisun/dont-be-shai">github.com/udisun/dont-be-shai</a></p>
    </div>
  </div>"""

def page(title, body, depth=0, desc=""):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="{up}assets/site.css">
</head>
<body>
{band(BAND_TOP, top=True)}
<div class="sheet">
{body}
{colophon(depth)}
</div>
{band(BAND_BOT)}
</body>
</html>
"""

def chart_svg(caption, rows):
    W, rowH, L, R, T, B = 1000, 40, 210, 96, 8, 8
    H = T + B + len(rows) * rowH
    mx = max(v for _, v in rows) or 1
    iw = W - L - R
    out = [f'<figure class="fig"><figcaption class="fig-c">{esc(caption)}</figcaption>',
           f'<div class="plot"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(caption)}. '
           + "; ".join(f"{esc(k)}, {v}" for k, v in rows) + '.">',
           f'<line x1="{L}" x2="{L}" y1="{T}" y2="{H-B}" stroke="var(--axis)" stroke-width="1"/>']
    for i, (k, v) in enumerate(rows):
        cy = T + i * rowH + rowH / 2
        w = max((v / mx) * iw, 2)
        out.append(f'<text x="{L-13}" y="{cy+4}" text-anchor="end" fill="var(--ink-2)" '
                   f'font-family="var(--sans)" font-size="13">{esc(k)}</text>')
        out.append(f'<rect x="{L}" y="{cy-11}" width="{w:.1f}" height="22" rx="4" fill="var(--accent)"/>')
        out.append(f'<rect x="{L}" y="{cy-11}" width="{min(6,w):.1f}" height="22" fill="var(--accent)"/>')
        out.append(f'<text x="{L+w+12:.1f}" y="{cy+4}" fill="var(--ink)" font-family="var(--sans)" '
                   f'font-size="13" font-weight="650">{v}</text>')
    out.append('</svg></div></figure>')
    return "\n".join(out)

def dossier(p):
    kj = "\n".join(f'<li><div><p>{esc(t)}</p></div></li>' for t in p["kj"])
    stats = "\n".join(
        f'<div class="stat"><div class="stat-l">{esc(l)}</div>'
        f'<div class="stat-v">{esc(v)}</div><div class="stat-s">{esc(s)}</div></div>'
        for l, v, s in p["stats"])
    body = f"""  <div class="pad">
    <nav class="crumb"><a href="../index.html">Central Declassification Registry</a>
      <span>Programme {esc(p["name"])}</span></nav>
    <header class="dcover">
      <div>
        <div class="orig">{esc(p["office"])}</div>
        <h1>{esc(p["title"])}</h1>
        <p class="sub">{esc(p["deck"])}</p>
      </div>
      <div class="dc">
        <div class="dc-h">Document control</div>
        <div class="dc-b"><dl>
          <div class="dc-r"><dt>Programme</dt><dd>{esc(p["name"])}</dd></div>
          <div class="dc-r"><dt>Coverage</dt><dd>{esc(p["years"])}</dd></div>
          <div class="dc-r"><dt>Status</dt><dd>{esc(p["status"])}</dd></div>
          <div class="dc-r"><dt>Countermeasure</dt><dd>None</dd></div>
        </dl></div>
      </div>
    </header>
  </div>
  <div class="pad"><section>
    <h2><span class="mark">(U)</span>Key judgments</h2>
    <ol class="kj">
{kj}
    </ol>
  </section></div>
  <div class="pad"><div class="stats">
{stats}
  </div></div>
  <div class="pad"><section>
    <h2><span class="mark">(U)</span>Observations</h2>
{chart_svg(*p["chart"])}
    <div class="assess">
      <div class="assess-l">Bottom line</div>
      <p>{esc(p["bottom"])}</p>
    </div>
  </section></div>"""
    return page(f"Programme {p['name']}", body, depth=1, desc=p["deck"])

def index():
    cards = "\n".join(f"""      <a class="row" href="programmes/{p['slug']}.html">
        <span class="r-name">{esc(p['name'])}</span>
        <span class="r-title">{esc(p['title'])}</span>
        <span class="r-office">{esc(p['office'])}</span>
        <span class="r-years">{esc(p['years'])}</span>
      </a>""" for p in P)
    body = f"""  <div class="pad">
    <header class="mast">
      <h1>Central Declassification Registry</h1>
      <p class="sub">Ten programmes, released in full. Each was run for decades against a
      population that never filed a complaint, because none of them could prove anything.</p>
    </header>
  </div>

  <div class="pad">
    <a class="feature" href="programmes/{FLAG['slug']}.html">
      <div class="f-l">Featured investigation</div>
      <div class="f-grid">
        <div class="f-num">{FLAG['stat'][0]}</div>
        <div>
          <h2 class="f-title">{esc(FLAG['title'])}</h2>
          <div class="f-prog">Programme {esc(FLAG['name'])}, {esc(FLAG['office'])}</div>
          <p class="f-deck">{esc(FLAG['deck'])} {esc(FLAG['stat'][1].capitalize())}, 1968 to 2026,
            and the campaign is accelerating.</p>
          <span class="f-cta">Read the assessment</span>
        </div>
      </div>
    </a>
  </div>

  <div class="pad">
    <section>
      <h2><span class="mark">(U)</span>Further programmes</h2>
      <div class="rows">
{cards}
      </div>
    </section>
  </div>"""
    return page("Central Declassification Registry", body, depth=0,
                desc="Ten declassified programme assessments, one of them real.")

# ---------------------------------------------------------------- write
(ROOT / "index.html").write_text(index(), encoding="utf-8")
for p in P:
    (ROOT / "programmes" / f"{p['slug']}.html").write_text(dossier(p), encoding="utf-8")
print(f"wrote index.html and {len(P)} programme pages")
