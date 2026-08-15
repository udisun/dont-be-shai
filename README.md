# Programme Pale Chorus

A deadpan intelligence assessment of every song that tells Shai not to be shy.
195 of them, 1968 to 2026, and the campaign is accelerating.

Published artifact: https://claude.ai/code/artifact/319720ad-fefc-4e8b-b4d8-06ede6839e83

`report.html` is standalone. The dataset is inlined into it, so it opens with no build step
and no network access.

## Data

195 distinct songs, 1968 to 2026, from MusicBrainz. 286 recordings collapsed by artist and
title so remixes and reissues count once. Each song dated by its earliest known release.

| File | Contents |
| --- | --- |
| `data/raw.json` | 286 raw MusicBrainz recordings |
| `data/songs.json` | deduplicated to 195 songs |
| `data/links.json` | resolved YouTube video ids |
| `data/cues3.json` | cue offsets, seconds, with an exact/approx tier |
| `data/payload.json` | the merged object inlined into `report.html` |

Cue values are numeric offsets only. No lyric text is stored anywhere in this directory.

## Scripts

Run in this order: `fetch.py`, `analyze.py`, `build_payload.py`, `resolve2.py`, `cues3.py`.
`resolve2.py` is the threaded wrapper around the helpers in `resolve.py`.

## Outstanding work: cue backfill

136 of 195 rows have no cue time, and 23 more are approximate (shown with a tilde)
because the timing came from the original release rather than that specific remix.

The fix is `scripts/cues_captions.py`, which reads the caption track of the exact
YouTube video each row links to. A caption cue is exact for that upload, so it both
fills the empty rows and upgrades the approximate ones.

    python3 scripts/cues_captions.py --probe     # is this host blocked?
    python3 scripts/cues_captions.py --dry-run   # resolve and report, write nothing
    python3 scripts/cues_captions.py             # backfill data/payload.json

**Run it from a home connection.** It cannot run from a datacenter IP. Two attempts
from a cloud host were refused with HTTP 429 on 6 of 7 requests, and slowing the pace
to one video every 20 seconds made it worse rather than better, so this is a block on
the address and not a pacing problem. The script stops itself after five consecutive
429s and writes nothing.

Note that the standalone `/api/timedtext` endpoint returns an empty body on its own.
The signed `baseUrl` has to be scraped from the watch page HTML:

    watch page -> "captionTracks":[...] -> baseUrl + "&fmt=json3" -> events[].tStartMs

Coverage will not reach 195 even on a good run: many official music uploads have
captions disabled entirely. Expect improvement, not completion.

After a successful run, re-inject `data/payload.json` into `report.html` and update the
coverage numbers in the Assessment paragraph, the Sourcing paragraph, the Known gaps
list, and the footer line.

## The registry site

`site/` builds a fictional archive, the Central Declassification Registry, with Pale Chorus as
the featured investigation and nine invented sibling programmes about ordinary petty grievances.

    python3 site/build.py        # regenerates index.html and site/programmes/*.html

Everything on the site is invented except Pale Chorus, whose song data is real. A colophon on
every page states exactly that, so the joke never has to be explained and is never mistaken for
a real claim.

### Serving it at a domain, locally

The "this is a real website" effect comes from a domain in the address bar, not from it being
someone else's domain. Point a name you control, or an unregistered one, at your own machine:

    # /etc/hosts
    127.0.0.1   your-chosen-name.org

    sudo python3 site/serve.py   # serves site/ on port 80

Then open `http://your-chosen-name.org`. Remove the hosts line to undo it.

Pick the name carefully. Confirm it is unregistered first, or use a `.test` name, which is
reserved by IANA and can never resolve publicly. Keep it plain HTTP; `.dev` and `.app` are
forced to HTTPS by browsers and will fail without a certificate. Do not point a hosts entry at
a real organisation's domain: that fabricates a page in someone else's name, and the screenshot
outlives the machine it was taken on.

### Publishing it properly

`site/` is a static directory, so GitHub Pages serves it as is. Repository settings, Pages,
deploy from `main` and the `/site` folder. Attach a real domain if you want it to survive
being forwarded.

## Findings

| | |
| --- | --- |
| Distinct songs | 220 |
| Artists | 163 |
| Span | 1968 to 2026 |
| Rate, 1970s | 0.50 per year |
| Rate, 2020s | 6.86 per year |
| Escalation | 13.7x |
| Peak | 13 in 2019 |
| Identical wording | 230 of 251 titles |
| Counter-movement | 8 songs |
| Subjects removed | 0 |

The corpus comes from searching MusicBrainz for the phrase "be shy" and keeping titles
that carry a negated or instructional construction. Searching only the contracted form
misses real entries, and apostrophes must be normalised before the negation test or
curly-quote titles are silently dropped.

Eight further songs argue the opposite position and are tracked separately, outside the
220, in the Countermeasures section of the report.


## Licence

Report text and code: do as you like. The underlying song metadata comes from
MusicBrainz, released under CC0 for the core data.
