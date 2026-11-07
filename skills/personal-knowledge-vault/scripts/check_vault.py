#!/usr/bin/env python3
"""Read-only health report for an Obsidian personal-knowledge vault.

    python3 check_vault.py "~/Documents/My Vault"            # Markdown report
    python3 check_vault.py "~/Documents/My Vault" --json     # machine-readable

Reports: duplicate file names, orphans (no backlinks), notes not reachable from the home
note, notes with fewer than 2 links out, missing or unknown frontmatter values, untitled
files, overdue and upcoming `due:` dates, and unresolved links (the backlog, not errors).

It writes nothing. Link resolution follows Obsidian's basic rules (case-insensitive file
name, or a path suffix), so it can differ from Obsidian in edge cases; when it disagrees with
Vault Health.base, trust the Base.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

TYPES = {"map", "project", "note", "source", "daily"}
STATUSES = {"seed", "active", "done", "parked", "shipped"}
REQUIRED = ("type", "status", "tags", "created")
AGENT_FILES = {"claude.md", "agents.md", "gemini.md", "readme.md"}  # instructions, not notes
UNTITLED = re.compile(r"^(untitled|未命名|无标题|sin título|sans titre)(\s*\d+)?$", re.I)
WIKILINK = re.compile(r"(!?)\[\[([^\]\|#\^]*)(?:[#\^][^\]\|]*)?(?:\|[^\]]*)?\]\]")
MDLINK = re.compile(r"\]\(([^)\s]+?\.md)(?:#[^)]*)?\)")
FENCE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def read_settings(root: Path, name: str) -> dict:
    p = root / ".obsidian" / name
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    fm: dict = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip("'\"")
        elif line.strip().startswith("- ") and fm:
            last = list(fm)[-1]
            fm[last] = (fm[last] + " " + line.strip()[2:]).strip()
    return fm, text[end + 4:]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("vault")
    ap.add_argument("--home", default=None, help='home note name (default: "Home" if present)')
    ap.add_argument("--templates", default=None, help="templates folder (default: from .obsidian/templates.json or Templates)")
    ap.add_argument("--daily", default=None, help="daily notes folder (default: from .obsidian/daily-notes.json or Daily)")
    ap.add_argument("--exclude", action="append", default=[], help="extra folder to skip (repeatable)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--limit", type=int, default=40, help="max items listed per section")
    args = ap.parse_args()

    root = Path(args.vault).expanduser().resolve()
    if not root.is_dir():
        sys.exit(f"Not a folder: {root}")
    templates = (args.templates or read_settings(root, "templates.json").get("folder") or "Templates").strip("/")
    daily = (args.daily or read_settings(root, "daily-notes.json").get("folder") or "Daily").strip("/")
    skip = {templates, "Archive", ".trash", *[e.strip("/") for e in args.exclude]}

    def skipped(rel: str) -> bool:
        parts = rel.split("/")
        return any(p.startswith(".") for p in parts) or any(rel == s or rel.startswith(s + "/") for s in skip)

    noise = {"node_modules", "__pycache__", "venv", ".venv"}
    all_files = [p for p in root.rglob("*") if p.is_file()
                 and not any(part.startswith(".") or part in noise for part in p.relative_to(root).parts[:-1])]
    notes = {}
    for p in all_files:
        rel = p.relative_to(root).as_posix()
        if p.suffix.lower() == ".md" and not skipped(rel) and not ("/" not in rel and p.name.lower() in AGENT_FILES):
            notes[rel] = p
    by_name = defaultdict(list)          # lower-case basename (no .md) -> [rel]
    other_names = set()                  # non-note files, for links like [[Deadlines.base]]
    for p in all_files:
        rel = p.relative_to(root).as_posix()
        if rel.split("/")[0].startswith("."):
            continue
        if p.suffix.lower() == ".md":
            by_name[p.stem.lower()].append(rel)
        else:
            other_names.add(p.name.lower())

    def closest(cands: list[str], source: str) -> str:
        """Among same-named files, prefer the one sharing the longest folder path with the linking note."""
        src = source.split("/")[:-1]
        def shared(c: str) -> int:
            n = 0
            for a, b in zip(src, c.split("/")[:-1]):
                if a != b:
                    break
                n += 1
            return n
        return sorted(cands, key=lambda c: (-shared(c), len(c), c))[0]

    def resolve(target: str, source: str = "") -> str | None | bool:
        t = target.strip()
        if not t:
            return False
        low = t.lower()
        if low.endswith(".md"):
            low = low[:-3]
        if "/" in low:
            for rel in notes:
                if rel.lower()[:-3].endswith(low):
                    return rel
            cands = by_name.get(low.rsplit("/", 1)[1], [])
            return cands[0] if cands else None
        cands = by_name.get(low)
        if cands:
            in_scope = [c for c in cands if c in notes]
            return closest(in_scope or cands, source)
        if low in other_names or t.lower() in other_names:
            return True  # an existing attachment or .base file
        return None

    home_name = args.home or ("Home" if "home" in by_name else None)
    home = resolve(home_name) if home_name else None

    out_links = defaultdict(set)
    backlinks = defaultdict(set)
    unresolved = defaultdict(set)
    fm_of = {}
    for rel, p in notes.items():
        text = p.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_frontmatter(text)
        fm_of[rel] = fm
        body = INLINE_CODE.sub("", FENCE.sub("", body))
        targets = [m.group(2) for m in WIKILINK.finditer(body)]
        targets += [Path(m.group(1)).stem for m in MDLINK.finditer(body) if "://" not in m.group(1)]
        for t in targets:
            r = resolve(t, rel)
            if r is None:
                unresolved[t.strip()].add(rel)
            elif isinstance(r, str) and r != rel:
                out_links[rel].add(r)
                backlinks[r].add(rel)

    def is_daily(rel: str) -> bool:
        return rel.startswith(daily + "/") or fm_of[rel].get("type") == "daily"

    def is_map(rel: str) -> bool:
        return fm_of[rel].get("type") == "map"

    # Reachability from home along outgoing links
    reachable = set()
    if isinstance(home, str):
        stack = [home]
        while stack:
            n = stack.pop()
            if n in reachable:
                continue
            reachable.add(n)
            stack.extend(out_links.get(n, ()))

    today = datetime.date.today()
    dupes = {k: [x for x in v if x in notes] for k, v in by_name.items()}
    dupes = {k: v for k, v in dupes.items() if len(v) > 1}
    orphans = sorted(r for r in notes if not backlinks[r] and r != home and not is_daily(r))
    unreachable = sorted(r for r in notes if isinstance(home, str) and r not in reachable and not is_daily(r))
    under = sorted((r, len(out_links[r])) for r in notes
                   if len(out_links[r]) < 2 and not is_map(r) and not is_daily(r))
    missing_fm, bad_values = [], []
    for r in sorted(notes):
        fm = fm_of[r]
        miss = [k for k in REQUIRED if not fm.get(k)]
        if miss:
            missing_fm.append((r, miss))
        if fm.get("type") and fm["type"] not in TYPES:
            bad_values.append((r, "type", fm["type"]))
        if fm.get("status") and fm["status"] not in STATUSES:
            bad_values.append((r, "status", fm["status"]))
    untitled = sorted(r for r in notes if UNTITLED.match(Path(r).stem.strip()))
    due_over, due_soon = [], []
    for r in sorted(notes):
        d = fm_of[r].get("due")
        if not d:
            continue
        try:
            dd = datetime.date.fromisoformat(d[:10])
        except ValueError:
            bad_values.append((r, "due", d))
            continue
        days = (dd - today).days
        if days < 0 and fm_of[r].get("status") not in ("done", "parked"):
            due_over.append((r, d, days))
        elif 0 <= days <= 14:
            due_soon.append((r, d, days))

    report = {
        "vault": str(root), "notes_checked": len(notes), "home": home if isinstance(home, str) else None,
        "duplicate_names": {k: v for k, v in sorted(dupes.items())},
        "orphans": orphans, "unreachable_from_home": unreachable,
        "under_linked": [{"note": r, "links_out": n} for r, n in under],
        "missing_frontmatter": [{"note": r, "missing": m} for r, m in missing_fm],
        "unknown_values": [{"note": r, "field": f, "value": v} for r, f, v in bad_values],
        "untitled": untitled,
        "overdue": [{"note": r, "due": d, "days": n} for r, d, n in due_over],
        "due_next_14_days": [{"note": r, "due": d, "days": n} for r, d, n in due_soon],
        "unresolved_links": {t: sorted(s) for t, s in sorted(unresolved.items(), key=lambda kv: -len(kv[1]))},
    }
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    L = args.limit

    def section(title: str, items: list[str], hint: str = "") -> None:
        print(f"\n## {title}: {len(items)}")
        if hint:
            print(hint)
        for line in items[:L]:
            print(f"- {line}")
        if len(items) > L:
            print(f"- … and {len(items) - L} more (use --json for all)")

    print(f"# Vault health: {root.name}\n")
    print(f"{len(notes)} notes checked (skipping {', '.join(sorted(skip))} and hidden folders). "
          f"Home note: {report['home'] or 'not found (pass --home)'}. Daily folder: {daily}.")
    section("Duplicate file names", [f"{k}: {', '.join(v)}" for k, v in report["duplicate_names"].items()],
            "Fix these first: links to a duplicated name are ambiguous, so every other count can be off.")
    section("Orphans (nothing links here)", orphans, "Add each to its parent Map.")
    if isinstance(home, str):
        section("Not reachable from Home", unreachable,
                "Linked from somewhere, but no chain of links leads here from Home. Usually a Map is missing a link.")
    section("Under-linked (fewer than 2 links out)", [f"{r} ({n})" for r, n in under])
    section("Missing frontmatter", [f"{r}: {', '.join(m)}" for r, m in missing_fm])
    section("Unknown frontmatter values", [f"{r}: {f} = {v!r}" for r, f, v in bad_values],
            "Fine if the owner added a new type on purpose (then add a graph colour group for it).")
    section("Untitled files", untitled, "Rename to a claim or a real name, then fix links.")
    section("Overdue", [f"{r}: due {d} ({-n} days ago)" for r, d, n in due_over])
    section("Due in the next 14 days", [f"{r}: due {d} (in {n} days)" for r, d, n in due_soon])
    section("Unresolved links (the backlog, not errors)",
            [f"[[{t}]] from {len(s)} note(s)" for t, s in report["unresolved_links"].items()])


if __name__ == "__main__":
    main()
