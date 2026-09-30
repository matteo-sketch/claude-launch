#!/usr/bin/env python3
"""Genera il link "▶ Avvia in Claude" per una task Notion.

Il link punta alla pagina ponte su GitHub Pages, che apre
claude://code/new?q=<prompt>&folder=<cartella> nell'app desktop.
Il prompt viaggia compresso (deflate-raw + base64url) dopo il #,
quindi non arriva mai al server e resta sotto il limite di 2000
caratteri delle proprietà URL di Notion.

Uso:
  python3 make_link.py --prompt-file p.txt --model "Opus 5.5" --effort alto --title "Kit votazione"
  echo "prompt" | python3 make_link.py --model "Sonnet 5.5"
"""
import argparse
import base64
import sys
import urllib.parse
import zlib

BASE = "https://matteo-sketch.github.io/claude-launch/"
DEFAULT_FOLDER = "/Users/postella/Documents/ClauDB"
NOTION_URL_LIMIT = 2000


def compress(text: str) -> str:
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    data = c.compress(text.encode("utf-8")) + c.flush()
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def make_link(prompt: str, model: str = "", effort: str = "", title: str = "",
              folder: str = DEFAULT_FOLDER) -> str:
    params = [("t", title), ("m", model), ("e", effort)]
    if folder != DEFAULT_FOLDER:
        params.append(("f", folder))
    params.append(("z", compress(prompt)))
    frag = "&".join(f"{k}={urllib.parse.quote(v, safe='')}" for k, v in params if v)
    return f"{BASE}#{frag}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-file")
    ap.add_argument("--model", default="")
    ap.add_argument("--effort", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--folder", default=DEFAULT_FOLDER)
    a = ap.parse_args()
    prompt = open(a.prompt_file, encoding="utf-8").read() if a.prompt_file else sys.stdin.read()
    link = make_link(prompt.strip(), a.model, a.effort, a.title, a.folder)
    if len(link) > NOTION_URL_LIMIT:
        sys.exit(f"Link di {len(link)} caratteri: oltre il limite Notion di {NOTION_URL_LIMIT}. Accorcia il prompt.")
    print(link)


if __name__ == "__main__":
    main()
