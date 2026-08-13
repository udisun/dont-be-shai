import json, re, unicodedata
from collections import Counter
P = "/tmp/claude-0/-home-user-odalin/4caac001-079a-5745-97c0-eae241329351/scratchpad/shai/"
d = json.load(open(P+"songs.json")); songs = d["songs"]
dated = [s for s in songs if s["year"]]
by_year = Counter(s["year"] for s in dated)
years = list(range(1968, 2027))
series = [by_year.get(y,0) for y in years]
cum, acc = [], 0
for c in series:
    acc += c; cum.append(acc)

decades = [("1968–79",5,12),("1980s",4,10),("1990s",24,10),("2000s",45,10),("2010s",63,10),("2020s",46,7)]
dec = [{"label":l,"n":n,"rate":round(n/yr,2)} for l,n,yr in decades]

table = sorted(
    [{"y":s["year"],"a":s["artist"],"t":s["title"],"r":s["releases"],"c":s["recordings"]} for s in songs],
    key=lambda x: (x["y"] is None, x["y"], x["a"].lower()))

canon = [
 (1968,"Orquesta Olivieri","Don't Be Shy","Patient zero. A Latin orchestra opens the campaign."),
 (1970,"Yusuf / Cat Stevens","Don't Be Shy","The anthem. Written for <em>Harold and Maude</em>, a film about a man who needs to get out more."),
 (1981,"Keith Forsey","Don't Be Shy","The producer of “Don’t You (Forget About Me)” tries the direct approach."),
 (1992,"Snap!","Don’t Be Shy","Eurodance escalation. 24 separate releases."),
 (1994,"Jamie Dee","Don't Be Shy","Twelve distinct recordings in one year. Someone was worried."),
 (2000,"Pearl Jam","Don't Be Shy","Grunge covers the Cat Stevens original across the official bootleg series."),
 (2003,"Travis","Don’t Be Shy","Scotland joins the effort."),
 (2004,"The Libertines","Don’t Be Shy","28 releases — the single most re-issued attempt on record."),
 (2017,"Girl's Day","Don't Be Shy","The campaign goes K-pop."),
 (2021,"Tiësto & KAROL G","Don't Be Shy","Global chart hit. Streamed roughly a billion times. Shai remains seated."),
 (2026,"(4 new entries)","Don't Be Shy","The current year is not over."),
]

payload = {
 "years": years, "series": series, "cum": cum, "dec": dec,
 "canon": [{"y":y,"a":a,"t":t,"n":n} for y,a,t,n in canon],
 "table": table,
 "stats": {"songs":len(songs),"artists":149,"span":58,"recordings":286,"releases":436,
           "hours":18.2,"growth":15.8,"peak":11,"peakyears":"2018 & 2019","first":1968,"last":2026,
           "drought":7,"droughtstart":1982,"halfyear":2013,"undated":8,"exact":102}
}
json.dump(payload, open(P+"payload.json","w"), separators=(",",":"), ensure_ascii=False)
print("years",len(years),"max",max(series),"cum",cum[-1],"table",len(table))
print("bytes", len(open(P+"payload.json").read()))
