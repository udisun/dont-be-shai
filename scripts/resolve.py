# Resolves, per song: a real YouTube video id, and the cue time (seconds) at which
# the phrase is first sung, taken from LRCLIB synced-lyric timings.
# Only the numeric timestamp is retained. Lyric text is never stored or emitted.
import json, re, time, urllib.request, urllib.parse, sys

UA_BROWSER = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"
UA_API = "ShaiDontBeShaiReport/1.0 ( udisun@gmail.com )"
PHRASE = re.compile(r"(don'?t|do not)\s+be\s+shy", re.I)

def get(url, ua, timeout=45, cap=None):
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read(cap) if cap else r.read()
    return raw.decode("utf-8", "ignore")

def strip_paren(t):
    return re.sub(r"\s*[\(\[].*?[\)\]]\s*", " ", t).strip()

def yt_search(artist, title):
    q = urllib.parse.quote(f"{artist} {title}")
    try:
        h = get(f"https://www.youtube.com/results?search_query={q}", UA_BROWSER, cap=900_000)
    except Exception:
        return None, None, 0
    blocks = re.findall(r'"videoId":"([\w-]{11})".{0,600?}', h)
    ids, titles = [], {}
    for m in re.finditer(r'"videoId":"([\w-]{11})".{0,1200}?"title":\{"runs":\[\{"text":"(.*?)"\}\]', h, re.S):
        vid, t = m.group(1), m.group(2)
        if vid not in titles:
            try: titles[vid] = json.loads('"' + t + '"')
            except Exception: titles[vid] = t
            ids.append(vid)
    if not ids:
        ids = re.findall(r'"videoId":"([\w-]{11})"', h)
        if not ids: return None, None, 0
        return ids[0], None, 1

    atoks = [w.lower() for w in re.findall(r"[A-Za-zÀ-ɏ]{3,}", artist)][:2]
    best, bestscore = None, -1
    for vid in ids[:12]:
        t = titles[vid]; tl = t.lower()
        s = 0
        if re.search(r"\bsh[yai]{1,2}\b", tl) or "shy" in tl or "shai" in tl: s += 3
        for a in atoks:
            if a in tl: s += 2
        if "official" in tl: s += 1
        if any(w in tl for w in ("cover", "karaoke", "reaction", "lyrics video by")): s -= 2
        if s > bestscore: best, bestscore = vid, s
    return best, titles.get(best), bestscore

def lrc_cue(artist, title):
    """Return first cue time in seconds, or None. Lyric text is discarded."""
    for a, t in ((artist, title), (artist, strip_paren(title)),
                 (artist.split(",")[0].split("&")[0].strip(), strip_paren(title))):
        try:
            u = ("https://lrclib.net/api/search?" +
                 urllib.parse.urlencode({"artist_name": a, "track_name": t}))
            arr = json.loads(get(u, UA_API, timeout=30))
        except Exception:
            continue
        if not isinstance(arr, list): continue
        for item in arr[:6]:
            s = item.get("syncedLyrics") or ""
            if not s: continue
            for line in s.split("\n"):
                m = re.match(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)", line)
                if not m: continue
                if PHRASE.search(m.group(3)):
                    return int(int(m.group(1)) * 60 + float(m.group(2)))   # seconds only
        time.sleep(.15)
    return None

songs = json.load(open("songs.json"))["songs"]
out = []
for i, s in enumerate(songs):
    art, tit = s["artist"], s["title"]
    vid, vtitle, score = yt_search(art, tit)
    cue = lrc_cue(art, tit)
    out.append({"artist": art, "title": tit, "year": s["year"], "releases": s["releases"],
                "vid": vid, "vtitle": vtitle, "score": score, "cue": cue})
    print(f"{i+1:3d}/{len(songs)} {art[:24]:24} | vid={vid or '-':11} | cue={cue if cue is not None else '-'}", flush=True)
    json.dump(out, open("links.partial.json", "w"), ensure_ascii=False)
    time.sleep(.35)

json.dump(out, open("links.json", "w"), ensure_ascii=False, indent=1)
print("DONE", sum(1 for o in out if o["vid"]), "videos,", sum(1 for o in out if o["cue"] is not None), "cues")
