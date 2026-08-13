# Recovers, per song, the first moment the phrase is sung. Only numeric offsets are kept.
import json, re, time, urllib.request, urllib.parse, threading
from concurrent.futures import ThreadPoolExecutor

UA="ShaiDontBeShaiReport/1.0 ( udisun@gmail.com )"
PH=re.compile(r"(don'?t|do not)\s+be\s+shy",re.I)
VER=re.compile(r"\b(remix|mix|edit|live|demo|instrumental|version|dub|acoustic|karaoke|radio|extended|club|bonus|remaster)\w*\b",re.I)

def api(path,**kw):
    u="https://lrclib.net/api/"+path+"?"+urllib.parse.urlencode(kw)
    r=urllib.request.Request(u,headers={"User-Agent":UA})
    with urllib.request.urlopen(r,timeout=30) as f: return json.load(f)

def norm(s):
    s=s.replace("’","'").replace("ʼ","'").lower()
    return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9' ]+"," ",s)).strip()
def base(s): return norm(re.sub(r"\s*[\(\[].*?[\)\]]\s*"," ",s))
def vtags(s): return set(m.group(0).lower() for m in VER.finditer(s))

def first_cue(sync):
    """First timestamp whose line contains the phrase. Returns seconds (float) or None."""
    for line in sync.split("\n"):
        m=re.match(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)",line)
        if m and PH.search(m.group(3)):
            return int(m.group(1))*60+float(m.group(2))
    return None

def lookup(artist,title):
    ours_v=vtags(title)
    queries=[{"artist_name":artist,"track_name":title},
             {"artist_name":artist,"track_name":re.sub(r"\s*[\(\[].*?[\)\]]\s*"," ",title).strip()},
             {"artist_name":artist.split(",")[0].split("&")[0].strip(),
              "track_name":re.sub(r"\s*[\(\[].*?[\)\]]\s*"," ",title).strip()}]
    seen=set()
    for q in queries:
        if not q.get("track_name"): continue
        key=tuple(sorted(q.items()))
        if key in seen: continue
        seen.add(key)
        try: res=api("search",**q)
        except Exception: continue
        if not isinstance(res,list): continue
        for item in res[:8]:
            s=item.get("syncedLyrics") or ""
            if not s: continue
            if norm(item.get("artistName","")).split()[:1] and \
               not (set(norm(artist).split()) & set(norm(item.get("artistName","")).split())):
                continue
            tn=item.get("trackName","")
            if base(tn)!=base(title): continue
            # do not transfer a base-version timing onto a remix/edit, timelines differ
            if vtags(tn)!=ours_v: continue
            c=first_cue(s)
            if c is not None: return round(c,1)
        time.sleep(.12)
    return None

pay=json.load(open("payload.json"))
rows=pay["table"]; out=[None]*len(rows); done=[0]; lock=threading.Lock()
def unspell(t):
    return t.replace("SHAI","SHY").replace("Shai","Shy").replace("shai","shy")

def work(i):
    r=rows[i]
    out[i]=lookup(r["a"], unspell(r["t"]))
    with lock:
        done[0]+=1
        if done[0]%25==0: print(done[0],"/",len(rows),flush=True)
with ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(work,range(len(rows))))

json.dump(out,open("cues2.json","w"))
got=[c for c in out if c is not None]
print("cues:",len(got),"/",len(rows))
print("under 2s:",sum(1 for c in got if c<2))
