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

136 of 195 rows have no timing. Current source is LRCLIB, which covers chart releases well
and the long tail badly.

The better source is the caption track on the specific YouTube video already linked in each
row, which would be exact for that upload and would also retire the 23 approximate cues. It
needs the signed `baseUrl` scraped from the watch page, because the standalone
`/api/timedtext` endpoint returns nothing on its own:

    watch page HTML -> "captionTracks":[...] -> baseUrl + "&fmt=json3" -> events[].tStartMs

Blocked when last attempted: YouTube returned HTTP 429 to this host after the 195 title
searches. Retry from an unthrottled address, pace it at a few seconds per video, and keep
only the integer offset. Then rebuild `payload.json` and republish to the artifact URL above.

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
| Distinct songs | 195 |
| Artists | 149 |
| Span | 1968 to 2026 |
| Rate, 1970s | 0.42 per year |
| Rate, 2020s | 6.57 per year |
| Escalation | 15.8x |
| Subjects removed | 0 |

## Licence

Report text and code: do as you like. The underlying song metadata comes from
MusicBrainz, released under CC0 for the core data.
