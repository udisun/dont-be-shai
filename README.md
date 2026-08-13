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
