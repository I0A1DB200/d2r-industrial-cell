#!/usr/bin/env python3
"""Render the versioned engineering brief Markdown as a self-contained reader page."""

import argparse
import html
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/engineering/00-BRIEF-CLIENTE.md"
OUTPUT = ROOT / "docs/engineering/00-BRIEF-CLIENTE.html"
GITHUB_SOURCE = "https://github.com/I0A1DB200/d2r-industrial-cell/blob/feature/d2r-engineering-mode/docs/engineering/00-BRIEF-CLIENTE.md"


def slug(text):
    plain = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", plain).strip("-") or "section"


def inline(text):
    escaped = html.escape(text, quote=False)

    def link(match):
        label = match.group(1)
        href = html.escape(html.unescape(match.group(2)), quote=True)
        return f'<a href="{href}">{label}</a>'

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def cells(line):
    return [item.strip() for item in line.strip().strip("|").split("|")]


def render_markdown(source):
    lines = source.splitlines()
    blocks = []
    toc = []
    title = "Brief del cliente y requisitos iniciales"
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2)
            if level == 1:
                title = text
                blocks.append(f'<h1 id="brief-title">{inline(text)}</h1>')
            else:
                anchor = f"section-{slug(text)}"
                blocks.append(f'<h{level} id="{anchor}">{inline(text)}</h{level}>')
                if level == 2:
                    toc.append((anchor, text))
            i += 1
            continue
        if line.startswith("> "):
            quote = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote.append(lines[i].strip()[2:])
                i += 1
            blocks.append(f'<blockquote><p>{inline(" ".join(quote))}</p></blockquote>')
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{3,}", lines[i + 1].strip()):
            headers = cells(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            head = "".join(f"<th scope=\"col\">{inline(value)}</th>" for value in headers)
            body_rows = []
            for row in rows:
                rendered_cells = []
                for column, value in enumerate(row):
                    label = headers[column] if column < len(headers) else "Dato"
                    rendered_cells.append(f'<td data-label="{html.escape(label, quote=True)}">{inline(value)}</td>')
                body_rows.append("<tr>" + "".join(rendered_cells) + "</tr>")
            body = "".join(body_rows)
            blocks.append(f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
            continue
        list_match = re.match(r"^(-|\d+\.)\s+(.+)$", line)
        if list_match:
            ordered = list_match.group(1) != "-"
            tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines):
                current = re.match(r"^\s*(-|\d+\.)\s+(.+)$", lines[i].strip())
                if not current or (current.group(1) != "-" and not ordered) or (current.group(1) == "-" and ordered):
                    break
                items.append(f"<li>{inline(current.group(2))}</li>")
                i += 1
            blocks.append(f'<{tag} class="doc-list">{"".join(items)}</{tag}>')
            continue

        paragraph = [line]
        i += 1
        while i < len(lines):
            current = lines[i].strip()
            if not current or re.match(r"^#{1,3}\s+", current) or current.startswith("> ") or current.startswith("|") or re.match(r"^(-|\d+\.)\s+", current):
                break
            paragraph.append(current)
            i += 1
        blocks.append(f'<p>{inline(" ".join(paragraph))}</p>')

    return title, toc, "\n".join(blocks)


def build(source):
    title, toc, body = render_markdown(source)
    nav = "\n".join(f'<a href="#{anchor}">{inline(text)}</a>' for anchor, text in toc)
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#101923">
<title>{html.escape(title)} · D2R</title>
<script>if(new URLSearchParams(location.search).get('embedded')==='1')document.documentElement.classList.add('embedded')</script>
<style>
:root{{--ink:#172536;--muted:#66788b;--line:#d7e0e8;--accent:#e87928;--paper:#fff;--canvas:#eef2f5;--blue:#24384c}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--canvas);color:var(--ink);font:16px/1.68 Inter,"Segoe UI",Arial,sans-serif}}
a{{color:#165d91;text-decoration-thickness:1px;text-underline-offset:3px}}a:hover{{color:#b45112}}
.topbar{{background:#101923;color:#eaf0f6;border-bottom:3px solid var(--accent);padding:14px max(22px,calc((100vw - 1200px)/2));display:flex;align-items:center;justify-content:space-between;gap:18px}}
.brand{{color:#f5f7fa;text-decoration:none;font-weight:800;letter-spacing:.02em}}.brand small{{display:block;color:#9badbf;font-size:10px;font-weight:600;letter-spacing:.16em}}
.tools{{display:flex;align-items:center;gap:9px}}.tools a,.tools button{{font:inherit;font-size:12px;font-weight:700;line-height:1.2;color:#f5f7fa;text-decoration:none;border:1px solid #53687c;border-radius:7px;background:#1c2b3a;padding:10px 13px;cursor:pointer}}.tools a:hover,.tools button:hover{{background:#30475d;color:#fff}}
.layout{{max-width:1200px;margin:34px auto;padding:0 22px;display:grid;grid-template-columns:240px minmax(0,1fr);gap:26px;align-items:start}}
.toc{{position:sticky;top:20px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:17px;box-shadow:0 5px 20px #1a2a3910}}
.toc strong{{display:block;color:var(--muted);font-size:10px;letter-spacing:.12em;margin-bottom:10px}}.toc a{{display:block;color:#30475d;text-decoration:none;font-size:12px;line-height:1.4;padding:7px 8px;border-left:2px solid #dbe4eb}}.toc a:hover{{color:#b45112;border-color:var(--accent);background:#fff8f2}}
article{{min-width:0;background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:clamp(24px,5vw,58px);box-shadow:0 8px 28px #1a2a3910}}
h1{{font-size:clamp(30px,4vw,42px);line-height:1.15;letter-spacing:-.03em;margin:0 0 24px;color:#142337}}h2{{font-size:23px;line-height:1.3;margin:42px 0 14px;padding-top:20px;border-top:1px solid #e6ebef;color:#1a3046}}h3{{font-size:18px;margin:30px 0 10px}}p{{margin:0 0 16px}}p strong{{color:#263b50}}
blockquote{{margin:22px 0;padding:15px 18px;border-left:4px solid var(--accent);border-radius:0 8px 8px 0;background:#fff6ef;color:#536679}}blockquote p{{margin:0}}
code{{font: .88em ui-monospace,SFMono-Regular,Consolas,monospace;background:#edf1f4;border-radius:4px;padding:2px 5px;white-space:nowrap}}
.doc-list{{padding-left:24px;margin:8px 0 20px}}.doc-list li{{padding:3px 0 3px 4px}}.table-wrap{{overflow-x:auto;margin:15px 0 22px}}table{{width:100%;border-collapse:collapse;font-size:13px;line-height:1.5}}th{{text-align:left;background:#21364a;color:white;padding:11px 12px;font-size:11px;letter-spacing:.025em}}td{{padding:10px 12px;border-bottom:1px solid #e0e7ed;vertical-align:top}}tbody tr:nth-child(even){{background:#f5f8fa}}
.footer{{max-width:1200px;margin:-12px auto 34px;padding:0 22px;color:var(--muted);font-size:12px;display:flex;justify-content:space-between;gap:14px}}
.embedded .topbar{{display:none}}.embedded .layout{{margin:0 auto;padding:18px 22px}}.embedded .footer{{padding:0 22px}}
@media(max-width:760px){{.topbar{{padding:10px 12px;display:grid;grid-template-columns:1fr;gap:7px}}.brand{{display:flex;align-items:baseline;gap:8px}}.brand small{{font-size:8px;white-space:nowrap}}.tools{{gap:6px;justify-content:flex-end}}.tools a,.tools button{{padding:8px 10px;font-size:11px;white-space:nowrap}}.layout{{display:block;margin:16px auto;padding:0 12px}}.toc{{position:static;display:flex;gap:4px;overflow:auto;white-space:nowrap;margin-bottom:12px;padding:10px}}.toc strong{{display:none}}.toc a{{border-left:0;border-bottom:2px solid #dbe4eb;padding:7px 9px}}article{{padding:23px 19px}}h2{{font-size:20px;margin-top:32px}}.table-wrap{{overflow:visible}}table,tbody{{display:block}}thead{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}tbody{{display:grid;gap:9px}}tbody tr{{display:block;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#fff!important}}td{{display:grid;grid-template-columns:minmax(82px,30%) minmax(0,1fr);gap:8px;padding:9px 10px}}td::before{{content:attr(data-label);font-size:10px;font-weight:800;line-height:1.4;color:#536a7e}}.footer{{padding:0 14px;display:block}}.footer a{{display:inline-block;margin-top:6px}}}}
@media print{{@page{{size:A4;margin:17mm}}:root{{--ink:#111;--muted:#333}}html{{scroll-behavior:auto}}body{{background:#fff;color:#111;font:11pt/1.48 Georgia,"Times New Roman",serif}}.topbar{{background:#fff;color:#111;border-bottom:2px solid #333;padding:0 0 10px}}.brand,.brand small{{color:#111}}.tools,.toc{{display:none!important}}.layout{{display:block;max-width:none;margin:0;padding:0}}article{{border:0;border-radius:0;box-shadow:none;padding:12mm 0}}h1{{font-size:26pt}}h2{{font-size:16pt;break-after:avoid;margin-top:24pt}}h3{{break-after:avoid}}p,li{{orphans:3;widows:3}}blockquote{{background:#fff;border:1px solid #aaa;border-left:4px solid #555;break-inside:avoid}}table{{font-size:9pt;break-inside:auto}}tr{{break-inside:avoid}}th{{background:#eee!important;color:#111;border:1px solid #888}}td{{border:1px solid #aaa}}a{{color:#111;text-decoration:none}}.footer{{max-width:none;padding:0;margin:0;color:#333;font-size:9pt}}}}
</style>
</head>
<body>
<header class="topbar"><a class="brand" href="../../index.html">D2R <small>DOCUMENTACIÓN DE INGENIERÍA</small></a><div class="tools"><a href="../../index.html" aria-label="Volver al simulador">← SIMULADOR</a><button class="print-button" type="button" onclick="window.print()">Imprimir / Guardar PDF</button></div></header>
<main class="layout"><nav class="toc" aria-label="Índice del documento"><strong>EN ESTE DOCUMENTO</strong>{nav}</nav><article aria-labelledby="brief-title">{body}</article></main>
<footer class="footer"><span>D2R Inspection Cell · Documento didáctico en revisión</span><a href="{GITHUB_SOURCE}" target="_blank" rel="noopener">Ver fuente Markdown versionada</a></footer>
</body>
</html>
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if the generated HTML is stale")
    parser.add_argument("--output", type=Path, help="write another copy, for deployment packaging")
    args = parser.parse_args()
    source = SOURCE.read_text(encoding="utf-8")
    output = args.output or OUTPUT
    rendered = build(source)
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Generated brief is stale: {output}")
        print(f"OK: {output} matches {SOURCE.relative_to(ROOT)}")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"Generated {output}")


if __name__ == "__main__":
    main()
