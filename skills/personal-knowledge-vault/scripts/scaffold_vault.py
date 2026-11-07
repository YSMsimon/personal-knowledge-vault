#!/usr/bin/env python3
"""Scaffold an Obsidian personal-knowledge vault.

    python3 scaffold_vault.py --vault "~/Documents/My Vault" --name "My Vault" \
        --wing "Life|private|Health, money, family" \
        --wing "Build|public|Things I build and share"

Each --wing is "Name|audience|description", audience one of public, private, strict.
Creates folders, Home.md, one entry note per wing, How This Vault Works.md, CLAUDE.md and
AGENTS.md (agent rules), Deadlines.base, Vault Health.base, Templates/, and Obsidian settings
for templates, daily notes and graph colours.

Safe on an existing folder: it never overwrites a file. Existing .obsidian JSON settings are
merged (only missing keys or colour groups are added). Use --dry-run to preview.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
AUDIENCES = {
    "public": "Shareable. Can become posts, talks or a published site.",
    "private": "Only for you. Never copied into a public note without your say-so.",
    "strict": "Someone else's material (employer, client). Leaves only after abstracting away "
              "names, links, IDs and identifying numbers.",
}
# Graph colour groups: Obsidian stores colours as 24-bit integers.
COLOUR_GROUPS = [
    ("[type:map]", 0xFFB454),      # gold
    ("[type:project]", 0x4CAF50),  # green
    ("[type:note]", 0x5B8DEF),     # blue
    ("[type:source]", 0xB48EAD),   # purple
    ("[type:daily]", 0x8A8A8A),    # grey
    ("tag:#private", 0xE06C75),    # red: anything in a private or strict wing
]


class Plan:
    def __init__(self, root: Path, dry: bool):
        self.root, self.dry = root, dry
        self.created: list[str] = []
        self.skipped: list[str] = []
        self.merged: list[str] = []

    def rel(self, p: Path) -> str:
        return str(p.relative_to(self.root)) if p != self.root else "."

    def mkdir(self, p: Path) -> None:
        if not p.exists():
            self.created.append(self.rel(p) + "/")
            if not self.dry:
                p.mkdir(parents=True, exist_ok=True)

    def write(self, p: Path, text: str) -> None:
        if p.exists():
            self.skipped.append(self.rel(p))
            return
        self.created.append(self.rel(p))
        if not self.dry:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")

    def merge_json(self, p: Path, add: dict, list_key: str | None = None, match: str | None = None) -> None:
        """Add missing keys to a JSON settings file; for list_key, append items whose
        `match` field is not present yet. Never changes an existing value."""
        if not p.exists():
            self.write(p, json.dumps(add, indent=2) + "\n")
            return
        try:
            cur = json.loads(p.read_text(encoding="utf-8") or "{}")
        except json.JSONDecodeError:
            self.skipped.append(self.rel(p) + " (unreadable JSON, left alone)")
            return
        changed = False
        for k, v in add.items():
            if k == list_key and isinstance(cur.get(k), list):
                have = {item.get(match) for item in cur[k] if isinstance(item, dict)}
                for item in v:
                    if item.get(match) not in have:
                        cur[k].append(item)
                        changed = True
            elif k not in cur:
                cur[k] = v
                changed = True
        if changed:
            self.merged.append(self.rel(p))
            if not self.dry:
                p.write_text(json.dumps(cur, indent=2) + "\n", encoding="utf-8")
        else:
            self.skipped.append(self.rel(p))


def parse_wing(spec: str) -> dict:
    parts = [s.strip() for s in spec.split("|")]
    name = parts[0]
    if not name or re.search(r'[\\/:*?"<>|#^\[\]]', name):
        sys.exit(f"Bad wing name {name!r}: avoid / \\ : * ? \" < > | # ^ [ ]")
    audience = (parts[1] if len(parts) > 1 and parts[1] else "private").lower()
    if audience not in AUDIENCES:
        sys.exit(f"Wing {name!r}: audience must be one of {', '.join(AUDIENCES)}")
    desc = parts[2] if len(parts) > 2 else ""
    return {"name": name, "audience": audience, "desc": desc}


def wing_formula(wings: list[dict]) -> str:
    """Nested if(file.inFolder(...)) giving each note its wing name in the Bases."""
    expr = '"Other"'
    for w in reversed(wings):
        expr = f'if(file.inFolder("{w["name"]}"), "{w["name"]}", {expr})'
    return expr.replace("'", "''")  # the Base templates wrap it in single quotes


def frontmatter(type_: str, status: str, tags: list[str], today: str) -> str:
    return f"---\ntype: {type_}\nstatus: {status}\ntags: [{', '.join(tags)}]\ncreated: {today}\n---\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vault", required=True, help="vault folder (created if missing)")
    ap.add_argument("--name", help="vault name used in the rules file (default: folder name)")
    ap.add_argument("--wing", action="append", default=[],
                    help='"Name|audience|description"; repeat for each wing (default: one private wing "Life")')
    ap.add_argument("--dry-run", action="store_true", help="show what would be created, write nothing")
    args = ap.parse_args()

    root = Path(args.vault).expanduser().resolve()
    name = args.name or root.name
    wings = [parse_wing(w) for w in args.wing] or [parse_wing("Life|private|Everything, for now")]
    reserved = {"templates", "daily", "attachments", "archive", "maps", "projects", "notes"}
    for w in wings:
        if w["name"].lower() in reserved:
            sys.exit(f"Wing name {w['name']!r} clashes with a built-in folder; pick another (e.g. Build, Life, Work).")
    if len({w["name"].lower() for w in wings}) != len(wings):
        sys.exit("Wing names must be unique.")
    today = datetime.date.today().isoformat()
    plan = Plan(root, args.dry_run)
    plan.mkdir(root)

    # Folders
    for d in ("Templates", "Daily", "Attachments"):
        plan.mkdir(root / d)
    for w in wings:
        for sub in ("Maps", "Projects", "Notes"):
            plan.mkdir(root / w["name"] / sub)

    # Home
    wing_lines = "\n".join(
        f"- [[{w['name']}]]: {w['desc'] or w['audience'] + ' wing'} ({w['audience']})" for w in wings)
    plan.write(root / "Home.md", frontmatter("map", "active", ["map"], today) + f"""
# Home

Entry point of {name}. Every note is reachable from here through Maps.

## Wings

{wing_lines}

## Dashboards

- [[Deadlines.base|Deadlines]]: every note with a `due:` date, by urgency
- [[Vault Health.base|Vault Health]]: orphans, under-linked notes, stale seeds

## How to use this vault

Read [[How This Vault Works]]. The one rule: no orphan notes. Every new page gets linked
from a Map, or it may as well not exist.
""")

    # Wing entry notes
    for w in wings:
        tags = ["map"] + (["private"] if w["audience"] in ("private", "strict") else [])
        others = [f"[[{o['name']}]]" for o in wings if o is not w]
        plan.write(root / w["name"] / f"{w['name']}.md", frontmatter("map", "active", tags, today) + f"""
# {w['name']}

{w['desc'] or 'One wing of this vault.'}

**Audience: {w['audience']}.** {AUDIENCES[w['audience']]}

## Maps

(Add a topic Map in `{w['name']}/Maps/` once a topic has more than a handful of notes, and
list it here.)

## Projects

(List each project note in `{w['name']}/Projects/` here with a one-line status.)

## Notes

(Atomic notes not yet under a topic Map go here.)

Up: [[Home]]{(' · Other wings: ' + ', '.join(others)) if others else ''}
""")

    # How This Vault Works, agent rules
    how = (ASSETS / "how-this-vault-works.md").read_text(encoding="utf-8")
    plan.write(root / "How This Vault Works.md",
               how.replace("{{TODAY}}", today).replace(
                   "{{WING_LIST}}", "\n".join(f"- [[{w['name']}]] ({w['audience']}): {w['desc']}".rstrip(": ")
                                               for w in wings)))
    table = "| Wing | Audience | Holds |\n|---|---|---|\n" + "\n".join(
        f"| `{w['name']}/` | {w['audience']} | {w['desc'] or '-'} |" for w in wings)
    rules = (ASSETS / "agent-rules.md").read_text(encoding="utf-8")
    rules = rules.replace("{{VAULT_NAME}}", name).replace("{{WING_TABLE}}", table)
    plan.write(root / "CLAUDE.md", rules)
    plan.write(root / "AGENTS.md", rules)

    # Bases
    formula = wing_formula(wings)
    for base in ("Vault Health.base", "Deadlines.base"):
        plan.write(root / base, (ASSETS / "bases" / base).read_text(encoding="utf-8").replace("{{WING_FORMULA}}", formula))

    # Templates
    for t in sorted((ASSETS / "templates").glob("*.md")):
        plan.write(root / "Templates" / t.name, t.read_text(encoding="utf-8"))

    # Obsidian settings (merged, never overwritten)
    obs = root / ".obsidian"
    plan.mkdir(obs)
    plan.merge_json(obs / "templates.json", {"folder": "Templates"})
    plan.merge_json(obs / "daily-notes.json",
                    {"folder": "Daily", "format": "YYYY-MM-DD", "template": "Templates/Daily Template"})
    plan.merge_json(obs / "app.json", {"attachmentFolderPath": "Attachments", "newLinkFormat": "shortest",
                                       "useMarkdownLinks": False})
    plan.merge_json(obs / "graph.json",
                    {"colorGroups": [{"query": q, "color": {"a": 1, "rgb": c}} for q, c in COLOUR_GROUPS],
                     "showOrphans": True},
                    list_key="colorGroups", match="query")

    verb = "Would create" if args.dry_run else "Created"
    print(f"{verb} in {root}:")
    for c in plan.created:
        print(f"  + {c}")
    if plan.merged:
        print("Added missing settings to:")
        for m in plan.merged:
            print(f"  ~ {m}")
    if plan.skipped:
        print("Left untouched (already there):")
        for s in plan.skipped:
            print(f"  = {s}")
    if not args.dry_run:
        print("\nNext: open the folder in Obsidian (Open folder as vault), check Settings > Core "
              "plugins > Bases is on, then open the graph view. Reload Obsidian if it was already "
              "open on this folder.")


if __name__ == "__main__":
    main()
