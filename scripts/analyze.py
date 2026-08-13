import json, re, unicodedata
from collections import Counter, defaultdict

P = "/tmp/claude-0/-home-user-odalin/4caac001-079a-5745-97c0-eae241329351/scratchpad/shai/"
rows = json.load(open(P + "raw.json"))

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").lower()
    s = s.replace("’", "'").replace("ʼ", "'")
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

PHRASES = ("don't be shy", "dont be shy", "do not be shy")
def has_phrase(t):
    n = norm(t)
    return any(p in n for p in PHRASES)

hits = [r for r in rows if has_phrase(r["title"])]
print("rows:", len(rows), "phrase hits:", len(hits))

# earliest year across recording first-release-date + any release date
def year_of(r):
    ys = []
    for d in ([r["first"]] if r["first"] else []) + r["release_dates"]:
        m = re.match(r"(\d{4})", d or "")
        if m:
            y = int(m.group(1))
            if 1900 <= y <= 2026:
                ys.append(y)
    return min(ys) if ys else None

# dedupe distinct songs by (normalized artist, normalized title)
songs = {}
for r in hits:
    key = (norm(r["artist"]), norm(r["title"]))
    y = year_of(r)
    cur = songs.get(key)
    if cur is None:
        songs[key] = {"artist": r["artist"], "title": r["title"], "year": y, "recordings": 1,
                      "releases": r["n_releases"], "lengths": [r["length"]] if r["length"] else []}
    else:
        cur["recordings"] += 1
        cur["releases"] += r["n_releases"]
        if r["length"]: cur["lengths"].append(r["length"])
        if y and (cur["year"] is None or y < cur["year"]):
            cur["year"] = y

songs = list(songs.values())
dated = [s for s in songs if s["year"]]
print("distinct songs:", len(songs), "| dated:", len(dated), "| undated:", len(songs) - len(dated))
print("year range:", min(s["year"] for s in dated), "-", max(s["year"] for s in dated))

by_year = Counter(s["year"] for s in dated)
for y in sorted(by_year):
    print(y, by_year[y], "#" * by_year[y])

# decade
dec = Counter((s["year"] // 10) * 10 for s in dated)
print("\nDECADES:", sorted(dec.items()))

# exact-title vs embedded
exact = [s for s in dated if norm(s["title"]) in ("don't be shy", "dont be shy")]
print("exact title 'Don't Be Shy':", len(exact))

print("\nEARLIEST 12:")
for s in sorted(dated, key=lambda s: s["year"])[:12]:
    print(" ", s["year"], "|", s["artist"][:38], "|", s["title"][:48])

print("\nMOST RECORDED:")
for s in sorted(songs, key=lambda s: -s["recordings"])[:10]:
    print(" ", s["recordings"], "recs |", s["year"], "|", s["artist"][:34], "|", s["title"][:44])

print("\nWEIRDEST TITLES:")
for s in sorted(songs, key=lambda s: -len(s["title"]))[:14]:
    print("  ", s["year"], "|", s["artist"][:30], "|", s["title"][:70])

json.dump({"songs": songs, "by_year": dict(by_year)}, open(P + "songs.json", "w"), indent=1)
