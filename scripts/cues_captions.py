#!/usr/bin/env python3
"""Backfill cue times from the caption track of each linked YouTube video.

Run this from a normal home connection. It fails from datacenter IPs, which
YouTube blocks with HTTP 429 (that is why it is not already applied).

    python3 scripts/cues_captions.py            # backfill and rewrite data/payload.json
    python3 scripts/cues_captions.py --probe    # just check whether this host is blocked
    python3 scripts/cues_captions.py --dry-run  # resolve cues, report, write nothing

A caption cue is exact for the specific upload the row links to, so it both fills
empty rows and upgrades the approximate (tilde) ones. Existing LRCLIB cues are kept
wherever captions yield nothing.

Only the integer second offset is ever stored. Caption and lyric text is read to
locate the line, then discarded; nothing in this repo contains lyrics.
"""
import argparse, json, pathlib, re, sys, time, urllib.error, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAYLOAD = ROOT / "data" / "payload.json"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/122 Safari/537.36")
PHRASE = re.compile(r"(don'?t|do not)\s+be\s+shy", re.I)
PACE = 3.0          # seconds between videos
MAX_429 = 5         # consecutive 429s before giving up


def fetch(url, cap=None, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return (r.read(cap) if cap else r.read()).decode("utf-8", "ignore")


def caption_cue(vid):
    """Return (seconds, status). seconds is None when no cue could be found."""
    try:
        page = fetch(f"https://www.youtube.com/watch?v={vid}", cap=3_000_000)
    except urllib.error.HTTPError as e:
        return None, f"http{e.code}"
    except Exception as e:
        return None, type(e).__name__

    m = re.search(r'"captionTracks":(\[.*?\])', page)
    if not m:
        return None, "no-captions"
    try:
        tracks = json.loads(m.group(1).replace("\\u0026", "&"))
    except json.JSONDecodeError:
        return None, "bad-tracks"

    # Prefer a real English track over an auto-generated one, but take what exists.
    tracks.sort(key=lambda t: (t.get("kind") == "asr",
                               not str(t.get("languageCode", "")).startswith("en")))
    for t in tracks[:2]:
        url = t.get("baseUrl", "").replace("\\u0026", "&")
        if not url:
            continue
        try:
            data = json.loads(fetch(url + "&fmt=json3"))
        except Exception:
            continue
        for ev in data.get("events", []):
            text = "".join(s.get("utf8", "") for s in (ev.get("segs") or []))
            if PHRASE.search(text):
                return int(ev.get("tStartMs", 0)) // 1000, "ok"   # offset only
        return None, "phrase-absent"
    return None, "no-usable-track"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true", help="test 3 videos and exit")
    ap.add_argument("--dry-run", action="store_true", help="resolve but do not write")
    args = ap.parse_args()

    payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    rows = payload["table"]
    targets = [r for r in rows if r.get("yt")]

    if args.probe:
        blocked = 0
        for r in targets[:3]:
            _, status = caption_cue(r["yt"])
            print(f"  {r['yt']}: {status}")
            blocked += status == "http429"
            time.sleep(PACE)
        print("BLOCKED: run this from a home connection" if blocked >= 2
              else "reachable: safe to run the full backfill")
        return

    before_cues = sum(1 for r in rows if "cue" in r)
    before_exact = sum(1 for r in rows if r.get("ck") == 1)

    filled = upgraded = 0
    streak = 0
    for i, r in enumerate(targets, 1):
        secs, status = caption_cue(r["yt"])
        if status == "http429":
            streak += 1
            if streak >= MAX_429:
                print(f"\nStopped after {MAX_429} consecutive 429s at row {i}. "
                      f"Nothing written.", file=sys.stderr)
                return 1
        else:
            streak = 0
        if secs is not None:
            if "cue" not in r:
                filled += 1
            elif r.get("ck") != 1:
                upgraded += 1
            r["cue"] = secs
            r["ck"] = 1                      # caption cues are exact for this upload
        if i % 20 == 0:
            print(f"  {i}/{len(targets)} filled={filled} upgraded={upgraded}", flush=True)
        time.sleep(PACE)

    after_cues = sum(1 for r in rows if "cue" in r)
    after_exact = sum(1 for r in rows if r.get("ck") == 1)
    cues = sorted(r["cue"] for r in rows if "cue" in r)
    payload["stats"].update({
        "cues": after_cues, "cuex": after_exact, "cuea": after_cues - after_exact,
        "medcue": cues[len(cues) // 2] if cues else 0, "nocue": len(rows) - after_cues,
    })

    print(f"\ncues   {before_cues} -> {after_cues}   (+{filled} newly filled)")
    print(f"exact  {before_exact} -> {after_exact}   (+{upgraded} upgraded from approximate)")
    print(f"median {payload['stats']['medcue']}s")

    if args.dry_run:
        print("dry run: data/payload.json not written")
        return 0

    PAYLOAD.write_text(json.dumps(payload, separators=(",", ":"), ensure_ascii=False),
                       encoding="utf-8")
    print(f"wrote {PAYLOAD}")
    print("Next: re-inject the payload into report.html and update the coverage "
          "numbers in the Assessment, Sourcing, Known gaps and footer copy.")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
