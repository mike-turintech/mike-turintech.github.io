#!/usr/bin/env python3
"""Refresh the publications section of index.html from DBLP.
usage: python3 build.py            (fetches DBLP, rewrites the block between the PUBS markers)
"""
import json, re, html, urllib.request, sys
Q = "https://dblp.org/search/publ/api?q=Michail%20Basios&h=100&format=json"
raw = urllib.request.urlopen(Q, timeout=30).read().decode()
open("dblp.json", "w").write(raw)
hits = [h["info"] for h in json.loads(raw)["result"]["hits"].get("hit", [])]
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
by = {}
for i in hits:
    k = norm(i["title"])
    if k not in by or (by[k].get("venue") == "CoRR" and i.get("venue") != "CoRR"):
        by[k] = i
pubs = sorted(by.values(), key=lambda i: (-int(i["year"]), i["title"]))
VEN = {"ESEC/SIGSOFT FSE": "ESEC/FSE", "CoRR": "arXiv", "IEEE Trans. Artif. Intell.": "IEEE Transactions on Artificial Intelligence", "ACM SIGSOFT Softw. Eng. Notes": "ACM SIGSOFT Software Engineering Notes"}
def authors(i):
    a = i.get("authors", {}).get("author", []); a = [a] if isinstance(a, dict) else a
    out = []
    for x in a:
        n = re.sub(r"\s0\d{3}$", "", x["text"])
        out.append(f"<strong>{html.escape(n)}</strong>" if n in ("Michail Basios", "Mike Basios") else html.escape(n))
    return ", ".join(out)
rows, year = [], None
for i in pubs:
    if i["year"] != year:
        rows.append(f'<h3 class="year">{i["year"]}</h3>'); year = i["year"]
    v = i.get("venue") or ("PhD thesis, University College London" if "Darwinian code optimisation" in i["title"] else "")
    v = VEN.get(v, v)
    link = i.get("ee") or i.get("url")
    rows.append(f'<article class="pub"><a href="{html.escape(link)}" rel="noopener">{html.escape(i["title"].rstrip("."))}</a><div class="meta">{authors(i)}</div><div class="venue">{html.escape(v)}</div></article>')
block = "\n".join(rows)
idx = block.find('<h3 class="year">2013</h3>')
if idx > 0:
    block = block[:idx] + '<details class="older"><summary>Earlier work (2012–2013)</summary>\n' + block[idx:] + "\n</details>"
page = open("index.html").read()
new = re.sub(r"(<!-- PUBS -->).*?(<!-- /PUBS -->)", lambda m: m.group(1) + "\n" + block + "\n" + m.group(2), page, flags=re.S)
if new == page:
    sys.exit("PUBS markers not found in index.html")
open("index.html", "w").write(new)
print(f"{len(pubs)} publications written")
