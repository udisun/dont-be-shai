import json, threading
from concurrent.futures import ThreadPoolExecutor

src = open("resolve.py").read().split("songs = json.load")[0]
ns = {}
exec(src, ns)
yt_search, lrc_cue = ns["yt_search"], ns["lrc_cue"]

songs = json.load(open("songs.json"))["songs"]
out = [None] * len(songs)
lock = threading.Lock()
done = [0]

def work(i):
    s = songs[i]
    art, tit = s["artist"], s["title"]
    try: vid, vtitle, score = yt_search(art, tit)
    except Exception: vid, vtitle, score = None, None, 0
    try: cue = lrc_cue(art, tit)
    except Exception: cue = None
    out[i] = {"artist": art, "title": tit, "year": s["year"], "releases": s["releases"],
              "vid": vid, "vtitle": vtitle, "score": score, "cue": cue}
    with lock:
        done[0] += 1
        if done[0] % 10 == 0:
            print(f"{done[0]}/{len(songs)}", flush=True)

with ThreadPoolExecutor(max_workers=6) as ex:
    list(ex.map(work, range(len(songs))))

json.dump(out, open("links.json", "w"), ensure_ascii=False, indent=1)
print("DONE videos:", sum(1 for o in out if o and o["vid"]),
      "cues:", sum(1 for o in out if o and o["cue"] is not None), flush=True)
