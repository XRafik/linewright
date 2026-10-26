# PROTOTYPE: turns a snapshot of the live board (0.6.0 markup) into the
# card-status branch's markup, adds sample lanes so every status shows, and
# writes docs/prototypes/palette/board.html.
import re, sys

src, out = sys.argv[1], sys.argv[2]
h = open(src).read()

ICON = {
    "Failure": '<circle cx="8" cy="8" r="6.75"/><path d="M5.75 5.75l4.5 4.5M10.25 5.75l-4.5 4.5"/>',
    "InProgress": '<circle cx="8" cy="8" r="6.75"/><circle cx="8" cy="8" r="2.5" fill="currentColor"/>',
    "Pending": '<circle cx="8" cy="8" r="6.75" stroke-dasharray="2.5 2"/>',
    "Paused": '<circle cx="8" cy="8" r="6.75"/><path d="M6.5 5.5v5M9.5 5.5v5"/>',
    "Success": '<circle cx="8" cy="8" r="6.75"/><path d="M5 8.25l2 2 4-4.25"/>',
    "Cancelled": '<circle cx="8" cy="8" r="6.75"/><path d="M3.25 12.75l9.5-9.5"/>',
}
VAR = {"Failure": "error", "Pending": "warning", "InProgress": "info", "Paused": "neutral", "Success": "success", "Cancelled": "neutral"}
RANK = ["Failure", "Pending", "InProgress", "Paused"]


def icon(t):
    return ('<svg class="icon size-[1em] shrink-0" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" '
            'fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">'
            + ICON[t] + "</svg>")


def toned(t):
    return f" toned [--tone:var(--color-{VAR[t]})]"


def tone_of(text):
    t = re.sub("<[^>]+>", "", text)
    if re.search(r"handed back|stalled|checks failed|conflicts", t): return "Failure"
    if re.search(r"asked |decision needed|changes requested|review required", t): return "Pending"
    if re.search(r"paused for|^queued", t): return "Paused"
    if re.search(r"checks running|^(#\d+ · )?(triage|design|implementation|update|rework|fix-ci|review) · ", t): return "InProgress"
    return None


def card(title, line, column):
    t = tone_of(line)
    quiet = " opacity-75" if column == "Done" else ""
    return (f'<li class="card card-sm border border-base-300 bg-card shadow-sm{toned(t) if t else ""}{quiet}">\n'
            f'<div class="card-body gap-1">\n<h3 class="card-title line-clamp-2 text-sm">{title}</h3>\n'
            f'<p class="line text-base-content/70">{icon(t) if t else ""}{line}</p>\n</div>\n</li>')


COLUMNS = ["Triage", "Needs a person", "Ready", "Working", "In review", "Done"]


def lane(head, cards):
    cells = "".join(
        f'<ul class="cell flex flex-col gap-2" aria-label="{c}">' + "".join(card(t, l, c) for (cc, t, l) in cards if cc == c) + "</ul>"
        for c in COLUMNS)
    return (f'<section class="lane mt-3 rounded-box border border-base-300 bg-base-200 px-(--lane-padding) pb-(--lane-padding)">'
            f'<h2 class="lane-head"><span class="sticky left-(--lane-inset) inline-block max-w-[calc(100cqw-2*var(--lane-inset))] truncate align-top">{head}</span></h2><div class="grid grid-cols-(--columns) gap-2">{cells}</div></section>')


SAMPLES = [
    lane("#9001: Sample statuses (prototype, not live data)", [
        ("Needs a person", "#9002: Ask about the release note", "asked tibbe · 1h"),
        ("Working", "#9003: Bump the toolchain", "queued"),
        ("Working", "#9004: Rework the runs table", "paused for the usage limit"),
        ("Working", "#9005: Pin the prompts", "implementation · 12m"),
        ("In review", "#9006: Redact header values", "checks failed"),
        ("In review", "#9007: Tidy the glossary", "checks running"),
        ("Done", "#9008: Release 0.6.0", "merged · 2026-10-26 08:00 UTC"),
    ]),
    lane("#9010: Sample lane, paused or queued at most (prototype)", [
        ("Working", "#9011: Read briefs from the default branch", "queued"),
        ("Ready", "#9012: Show the repository's avatar", "blocked by #9011"),
    ]),
    lane("#9020: Sample lane, in flight at most (prototype)", [
        ("Working", "#9021: Record each session's model", "update · 3m"),
    ]),
]

# Cards: the branch's classes, edge, icon and fading.
def recard(m):
    block, column = m.group(0), m.group(1)
    def one(cm):
        li = cm.group(0)
        line = re.search(r'<p class="line[^"]*">(.*?)</p>', li, re.S)
        t = tone_of(line.group(1)) if line else None
        quiet = " opacity-75" if column == "Done" else ""
        li = li.replace('<li class="card card-sm bg-base-100">',
                        f'<li class="card card-sm border border-base-300 bg-card shadow-sm{toned(t) if t else ""}{quiet}">')
        if t:
            li = li.replace('<p class="line text-base-content/70">', '<p class="line text-base-content/70">' + icon(t), 1)
        return li
    return re.sub(r'<li class="card.*?</li>', one, block, flags=re.S)

h = re.sub(r'<ul class="cell[^>]*aria-label="([^"]+)">.*?</ul>', recard, h, flags=re.S)

# Lane heads: the most pressing card's status, washed, with its line.
def relane(m):
    sec = m.group(0)
    best = None
    for li in re.findall(r'<li class="card.*?</li>', sec, re.S):
        line = re.search(r'<p class="line[^"]*">(.*?)</p>', li, re.S)
        t = tone_of(line.group(1)) if line else None
        if t and (best is None or RANK.index(t) < RANK.index(best[0])):
            num = re.search(r">#(\d+):", li).group(1)
            best = (t, num, re.sub(r"<svg.*?</svg>", "", line.group(1), flags=re.S))
    if best:
        t, num, line = best
        sec = re.sub(r'<(h2|summary) class="lane-head', lambda x: f'<{x.group(1)} class="lane-head{toned(t)}', sec, count=1)
        sec = re.sub(r'(class="lane-head[^"]*">\s*<span[^>]*>.*?)(</span>)', lambda x: x.group(1) + f" — {icon(t)}#{num} · {line}" + x.group(2), sec, count=1, flags=re.S)
    return sec

h = re.sub(r'<(section|details) class="lane .*?</\1>', relane, h, flags=re.S)

# The samples go first, after the column heads.
first = h.find('<section class="lane')
h = h[:first] + "".join(re.sub(r'<(section|details) class="lane .*?</\1>', relane, x, flags=re.S) for x in SAMPLES) + h[first:]

# Static: the branch's stylesheet, no live scripts, the palette and theme from the URL.
h = re.sub(r'<link rel="stylesheet"[^>]*>', '<link rel="stylesheet" href="../../../assets/linewright.css"><link rel="stylesheet" href="palette.css">', h)
h = re.sub(r'<script[^>]*></script>\n?', "", h)
h = h.replace('hx-sse:connect="/events/"', "")
h = h.replace("<head>", """<head>
<script>
const q = new URLSearchParams(location.search);
document.documentElement.dataset.theme = q.get("theme") || "light";
document.documentElement.dataset.palette = q.get("palette") || "daisyui";
</script>""", 1)
open(out, "w").write(h)

PARTS = """
<div class="row"><button class="btn btn-sm">Button</button><button class="btn btn-sm btn-primary">Primary</button><input class="input input-sm w-auto" value="input"><select class="select select-sm w-auto"><option>select</option></select></div>
<div class="row"><span class="badge badge-error">failed</span><span class="badge badge-warning">waiting</span><span class="badge badge-info">in flight</span><span class="badge badge-success">done</span><span class="badge badge-neutral">cancelled</span><code>code</code></div>
<div class="row"><div role="alert" class="alert">usage limit (plain alert)</div><div role="alert" class="alert alert-warning">drain</div></div>
<div class="row"><table class="table table-pin-rows w-auto"><thead><tr><th>Run</th><th>Outcome</th></tr></thead><tbody><tr><td>#12</td><td>merged</td></tr></tbody></table>
<ul class="menu w-auto p-0"><li><a aria-current="page">Board (current)</a></li><li><a>Runs</a></li></ul>
<span class="tooltip tooltip-open tooltip-top mt-8" data-tip="a tooltip">hover</span></div>
"""
FILLS = ('<div id="parts">'
  '<div class="surface rounded-box"><h4>On the Page</h4>' + PARTS + '</div>'
  '<div class="surface rounded-box border border-base-300 bg-base-200"><h4>On a Lane</h4>' + PARTS + '</div>'
  '<div class="surface rounded-box border border-base-300 bg-card shadow-sm"><h4>On a Card</h4>' + PARTS + '</div></div>')
h = open(out).read()
h = h.replace('<section id="board"', FILLS + '<section id="board"', 1)
h = h.replace('document.documentElement.dataset.palette = q.get("palette") || "daisyui";',
  'for (const k of ["status", "surfaces"]) document.documentElement.dataset[k] = q.get(k) || {status: "daisyui", surfaces: "lifted"}[k];')
open(out, "w").write(h)
