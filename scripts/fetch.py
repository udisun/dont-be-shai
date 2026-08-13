import json, time, urllib.parse, urllib.request

UA = "ShaiDontBeShyReport/1.0 ( udisun@gmail.com )"
BASE = "https://musicbrainz.org/ws/2/recording"

def get(query, offset):
    url = BASE + "?" + urllib.parse.urlencode({"query": query, "fmt": "json", "limit": 100, "offset": offset})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            print("  retry", attempt, e)
            time.sleep(2 ** attempt)
    raise SystemExit("failed: " + url)

def harvest(query, tag):
    out, offset = [], 0
    while True:
        d = get(query, offset)
        total = d["count"]
        recs = d.get("recordings", [])
        if not recs:
            break
        for r in recs:
            out.append({
                "tag": tag,
                "id": r["id"],
                "title": r.get("title", ""),
                "score": r.get("score"),
                "artist": ", ".join(a.get("name", "") for a in r.get("artist-credit", [])),
                "first": r.get("first-release-date"),
                "length": r.get("length"),
                "video": r.get("video"),
                "release_dates": [rel.get("date") for rel in r.get("releases", []) if rel.get("date")],
                "n_releases": len(r.get("releases", [])),
            })
        offset += len(recs)
        print(f"  {tag}: {offset}/{total}")
        if offset >= total:
            break
        time.sleep(1.1)
    return out

queries = [
    ('recording:"don\'t be shy"', "dont-be-shy"),
    ('recording:"do not be shy"', "do-not-be-shy"),
    ('recording:"dont be shy"',   "dont-be-shy-noapos"),
]

all_rows = []
for q, tag in queries:
    print(q)
    all_rows += harvest(q, tag)
    time.sleep(1.1)

with open("/tmp/claude-0/-home-user-odalin/4caac001-079a-5745-97c0-eae241329351/scratchpad/shai/raw.json", "w") as f:
    json.dump(all_rows, f, indent=1)
print("total rows:", len(all_rows))
