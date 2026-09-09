#!/usr/bin/env python3
"""Regenerate llms-full.txt (Markdown mirror of index.html for LLM crawlers). Run by build.py; can be run alone."""
import re, html as H
s = open("index.html").read()
def text(x):
    x = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', lambda m: f'[{m.group(2)}]({m.group(1)})', x, flags=re.S)
    return H.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', x))).strip()
def section(sid):
    i = s.index(f'<section id="{sid}">'); return s[i:s.index('</section>', i)]
def paras(sec): return [text(p) for p in re.findall(r'<p(?: class="note")?>(.*?)</p>', sec, re.S)]
def items(sec):
    return [f"- {yr + ': ' if yr else ''}{text(body)}" for yr, body in re.findall(r'<li><span class="yr">(.*?)</span><div>(.*?)</div></li>', sec, re.S)]
def pubs():
    blk = s[s.index('<!-- PUBS -->'):s.index('<!-- /PUBS -->')]; out = []
    for m in re.finditer(r'<h3 class="year">(\d+)</h3>|<article class="pub"><a href="([^"]+)"[^>]*>(.*?)</a><div class="meta">(.*?)</div><div class="venue">(.*?)</div></article>', blk, re.S):
        out.append(f"\n### {m.group(1)}\n" if m.group(1) else f"- [{H.unescape(m.group(3))}]({m.group(2)}). {text(m.group(4))}. {H.unescape(m.group(5))}")
    return "\n".join(out).strip()
contact = "\n".join(f"- {text(k)}: {v}" for k, v in re.findall(r'<div><span>(.*?)</span><a href="([^"]+)"', section('contact')))
NL = "\n"
md = f"""# Mike Basios — full profile

{text(re.search(r'<p class="tag">(.*?)</p>', s, re.S).group(1))}. Canonical page: https://mike-turintech.github.io/ (short version: https://mike-turintech.github.io/llms.txt)

## About
{NL.join(NL + p for p in paras(section('about')))}

## Awards and recognition

{NL.join(items(section('awards')))}

## Publications

{paras(section('publications'))[0]}

{pubs()}

## Talks and media

{NL.join(items(section('talks')))}

## Writing

{NL.join(items(section('writing')))}

## Contact

{contact}
"""
open("llms-full.txt", "w").write(md)
print("llms-full.txt written")
