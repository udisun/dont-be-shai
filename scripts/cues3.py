# Final cue pass. Stores only numeric offsets and a confidence tier.
import json, re, time, unicodedata, urllib.request, urllib.parse, threading
from concurrent.futures import ThreadPoolExecutor
UA="ShaiDontBeShaiReport/1.0 ( udisun@gmail.com )"
PH=re.compile(r"(don'?t|do not)\s+be\s+shy",re.I)
VER=re.compile(r"\b(remix|mix|edit|live|demo|instrumental|version|dub|acoustic|radio|extended|club|remaster)\w*\b",re.I)

def api(path,**kw):
    u="https://lrclib.net/api/"+path+"?"+urllib.parse.urlencode(kw)
    r=urllib.request.Request(u,headers={"User-Agent":UA})
    with urllib.request.urlopen(r,timeout=30) as f: return json.load(f)
def deacc(s): return unicodedata.normalize("NFKD",s).encode("ascii","ignore").decode()
def norm(s):
    s=deacc(s.replace("’","'").replace("ʼ","'")).lower()
    return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9' ]+"," ",s)).strip()
def base(s): return norm(re.sub(r"\s*[\(\[].*?[\)\]]\s*"," ",s))
def vtags(s): return frozenset(m.group(1).lower() for m in VER.finditer(s))
def atoks(s): return {w for w in norm(s).split() if len(w)>2}
def first_cue(sync):
    for line in sync.split("\n"):
        m=re.match(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)",line)
        if m and PH.search(m.group(3)): return int(m.group(1))*60+float(m.group(2))
    return None
def unspell(t): return t.replace("SHAI","SHY").replace("Shai","Shy").replace("shai","shy")

def lookup(artist,title):
    t=unspell(title); ours=vtags(t); bt=base(t)
    a1=artist.split(",")[0].split("&")[0].strip()
    plain=re.sub(r"\s*[\(\[].*?[\)\]]\s*"," ",t).strip()
    cands=[]
    for q in ({"artist_name":artist,"track_name":t},
              {"artist_name":artist,"track_name":plain},
              {"artist_name":a1,"track_name":plain},
              {"track_name":plain}):
        if not q.get("track_name"): continue
        try: res=api("search",**q)
        except Exception: continue
        if isinstance(res,list): cands.extend(res[:10])
        time.sleep(.1)
        if cands: break
    exact=approx=None
    for item in cands:
        s=item.get("syncedLyrics") or ""
        if not s: continue
        if base(item.get("trackName",""))!=bt: continue
        if not (atoks(artist) & atoks(item.get("artistName",""))): continue
        c=first_cue(s)
        if c is None: continue
        if vtags(item.get("trackName",""))==ours:
            exact=c if exact is None else min(exact,c); break
        if approx is None: approx=c
    if exact is not None: return round(exact,1),"exact"
    if approx is not None: return round(approx,1),"approx"
    return None,None

pay=json.load(open("payload.json")); rows=pay["table"]
out=[None]*len(rows); done=[0]; lock=threading.Lock()
def work(i):
    out[i]=lookup(rows[i]["a"],rows[i]["t"])
    with lock:
        done[0]+=1
        if done[0]%40==0: print(done[0],flush=True)
with ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(work,range(len(rows))))
json.dump(out,open("cues3.json","w"))
ex_=sum(1 for c,k in out if k=="exact"); ap=sum(1 for c,k in out if k=="approx")
print(f"exact {ex_} | approx {ap} | total {ex_+ap} / {len(rows)}")
