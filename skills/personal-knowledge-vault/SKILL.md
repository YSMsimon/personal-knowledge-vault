---
name: personal-knowledge-vault
description: Build and run a personal database ("second brain") as an Obsidian vault that an AI agent keeps linked and tidy - wings separated by audience (public, private, strict), Maps of Content, a frontmatter contract, a no-orphan link rule, graph colours, Bases dashboards for vault health and deadlines, note templates, and a memory rule so facts said in chat land in the right note. Use this skill whenever someone wants to set up, organise, migrate into, audit or work inside an Obsidian vault or personal knowledge base, says "write this down" or "remember this" about their notes, mentions a second brain, Zettelkasten, PKM, Maps of Content, orphan notes or the Obsidian graph, or wants their agent to manage notes like a database - even if they never say "Obsidian".
---

# Personal knowledge vault

This skill turns a folder of Markdown files into a personal database that stays useful after
it gets too big to remember. Obsidian renders it; the agent (you) keeps it linked. The design
comes from a vault that grew past 1,000 notes across three areas of one person's life while an
agent did nearly all the writing. Each rule below exists because something broke without it.

## What you build

```
MyVault/
├── Home.md                  ← top Map: links to every wing's entry note
├── How This Vault Works.md  ← the rules, for the human
├── CLAUDE.md / AGENTS.md    ← the same rules, loaded by agents every session
├── Deadlines.base           ← every note with a `due:` date, by urgency
├── Vault Health.base        ← orphans, under-linked notes, stale seeds
├── Templates/               ← note templates (never linked from a Map)
├── Daily/                   ← daily notes (link outward only)
├── Attachments/
└── <Wing>/                  ← one folder per audience, e.g. Life/, Build/, Work/
    ├── <Wing>.md            ← the wing's entry note (a Map)
    ├── Maps/                ← topic Maps, added as topics grow
    ├── Projects/            ← one note per thing being built or done
    └── Notes/               ← atomic notes, one idea each
```

## The ideas behind the rules

Explain these to the person when you set the vault up. They are what make the rules feel
reasonable rather than fussy.

1. **Maps, not folders.** Folders are storage; Maps are meaning. A Map is a note whose job is
   to list and explain other notes. Every note is reachable from `Home` through Maps, so
   nothing is lost when the folder tree gets deep.
2. **A note no Map lists does not exist.** Orphans are the main way a vault dies: they are
   never found again, so nobody updates them, so they go stale. Hence the no-orphan rule:
   every note links out to at least two notes and is listed in its parent Map.
3. **Titles are claims.** `Sleep Debt Compounds.md` can be linked mid-sentence;
   `Sleep.md` is a junk drawer. Atomic notes get claim-shaped titles so that writing a sentence
   naturally produces a link. Projects and people keep plain names.
4. **Unresolved links are the to-do list.** Writing `[[Some Idea]]` before the note exists is
   correct. The graph shows it as a hollow node, which is a free backlog. Never delete a link
   just to silence a warning.
5. **Wings by audience.** Notes split first by who may see them, not by topic: a public wing
   (things you share), private wings (health, money, job search), and optionally a strict wing
   (an employer's or client's material). Leaks happen when audiences mix in one folder.
6. **Dates that matter live in frontmatter.** A hard external deadline goes in `due:`, where
   `Deadlines.base` can sort it. A date that lives only in a sentence rots silently.
7. **Chat dies, the vault doesn't.** When the person tells you something durable, write it into
   the right note in the same turn and say where. This is the habit that makes the vault worth
   keeping.

## Workflow 1: set up a new vault

**1. Ask a few questions, then propose defaults.** Keep it short; a good default beats a long
interview.
- Where should the vault live, and what is it called? (Default: `~/Documents/<Name> Vault`.)
- Which areas of life or work should it hold, and who may see each? Turn the answers into
  wings. Suggest two or three, for example `Life|private`, `Build|public`, `Work|strict`.
  Avoid naming a wing `Projects`, `Notes` or `Maps`: each wing already has folders with those names.
  One wing is fine for someone unsure; more can be added later.
- What do they want to track first? (Projects, deadlines, reading, health, money…) This seeds
  the first Maps and notes.
- Do they already have notes somewhere? If yes, plan a migration (Workflow 4) after setup.

**2. Scaffold the vault.** The script creates the folders, `Home`, the wing entry notes, the
agent rules (`CLAUDE.md` and `AGENTS.md`), the two Bases, the templates and the Obsidian
settings for templates, daily notes and graph colours. It never overwrites an existing file,
so it is safe to run on a folder that already has notes.

```bash
python3 <skill-dir>/scripts/scaffold_vault.py \
  --vault "~/Documents/My Vault" --name "My Vault" \
  --wing "Life|private|Health, money, family, admin" \
  --wing "Build|public|Things I build and share" \
  --wing "Work|strict|Employer material, never leaves this wing unabstracted"
```

Audience values: `public`, `private` (adds the `private` tag to that wing's notes), `strict`
(private, and material leaves only after it is abstracted to the technique). Run with
`--dry-run` first if the folder already holds files, and show the person what will be created.

**3. Offer the companion skills.** Steph Ango's `kepano/obsidian-skills` teach an agent
Obsidian-flavoured Markdown, Bases syntax, JSON Canvas and the Obsidian CLI. Installing them
downloads code, so ask first. Then, from inside the vault:

```bash
npx skills add kepano/obsidian-skills
```

Details, manual install paths and the Obsidian CLI are in `references/companion-skills.md`.

**4. Hand over to Obsidian.** Tell the person to open Obsidian → *Open folder as vault* → pick
the folder; to check that the *Bases* core plugin is on (Settings → Core plugins); and to open
the graph view. If Obsidian was already open on this folder, it may need a reload to pick up
the new graph colours.

**5. Seed real content.** Write the first few notes from what they told you in step 1: one
project note, one note per deadline (with `due:`), a topic Map if a topic already has several
notes. Link each into its Map. Then run the health check (Workflow 3) so they see a clean
report.

## Workflow 2: everyday work inside a vault

Read `CLAUDE.md` (or `AGENTS.md`) at the vault root first; it may hold rules the person added.
Then read the entry note of the wing you are about to touch. For any note you create or change:

1. **Search first.** Update the existing note rather than create a second one with a similar
   name. Two files with the same name make links ambiguous.
2. **Choose the wing and type.** Wing by audience, type by role (`map`, `project`, `note`,
   `source`, `daily`). If unsure about the wing, pick the more private one.
3. **Write it** with the frontmatter contract and a real title, and link at least two notes in
   the body, ideally mid-sentence where the connection is real.
4. **Link it back:** add `[[Its Title]]` with a one-line description to its parent Map.
5. **Dates:** a real external deadline goes in `due:` as well as in the text.
6. **Say what you did:** name the notes you created or changed, so the person can check.

When the person says "write that down", "remember this" or states a decision, that is a memory
event: put it in the most relevant existing note (create one only if none fits) in the same
turn. Daily notes (`Daily/YYYY-MM-DD.md`) log what was touched that day and link to those notes;
nothing needs to link to a daily note.

Full contract, title guidance, when to start a new Map, and examples: `references/conventions.md`.

## Workflow 3: health check

Run the checker; it reads the whole vault and writes nothing:

```bash
python3 <skill-dir>/scripts/check_vault.py "~/Documents/My Vault"
```

It reports orphans, notes with fewer than two links out, notes not reachable from `Home`,
missing or invalid frontmatter, untitled files, duplicate file names, overdue and upcoming
`due:` dates, and unresolved links (as the backlog, not as errors). Fix in this order: duplicate
names (they corrupt everything else), orphans, unreachable notes, under-linked notes, then
frontmatter. Leave unresolved links alone unless the person wants to write those notes.

Inside Obsidian, `Vault Health.base` shows the same problems from Obsidian's own link index.
When the script and the Base disagree, trust the Base: Obsidian resolves links the same way the
person sees them, and a script keyed on file names can be fooled (a duplicate name once
produced twenty false orphans in the original vault).

## Workflow 4: bring existing notes in

Messy notes ("Untitled 7", a Downloads pile, an old Notion export) move in small batches:
inventory, triage (keep, merge, archive), rename to claims, add frontmatter, link into Maps,
re-check. Never delete anything; archive instead. Scan for passwords, keys and ID numbers on the
way in and tell the person, rather than copying them deeper into the vault. Step-by-step:
`references/migrating-notes.md`.

## How the graph comes out

Links, not folders, shape Obsidian's graph. With these rules the graph has a clear spine:
`Home` → wing entry notes → topic Maps → projects and notes, with notes cross-linking each
other, daily notes hanging off the side, and hollow nodes for ideas not yet written. Colour
groups key off the `type` property, plus the `private` tag. An island floating away from the
spine is an under-linked cluster: find the Map it belongs to. Diagram, colour settings and the
two Bases explained: `references/graph-and-bases.md`.

## Privacy and safety

- Keep wings separate. Nothing from a private wing goes into a public note unless the person
  says so plainly; strict-wing material leaves only after abstracting away names, links, IDs
  and identifying numbers.
- Never put passwords, API keys, card numbers or government ID numbers in the vault, even if
  asked to "save it in my notes". Suggest a password manager instead.
- Never delete notes. Set `status: parked`, or move the note to an `Archive/` folder and keep
  its Map entry pointing at the new place.
- If the vault syncs to a public place (a published site, a public repo), check which wings
  are included before writing private material.

## Reference files

- `references/conventions.md`: frontmatter contract, types and statuses, titles, Maps, daily
  notes, templates, worked examples. Read when writing or reorganising notes.
- `references/graph-and-bases.md`: graph shape, colour groups, the two Bases, embedding Base
  views, Obsidian CLI checks. Read when setting up or debugging the graph or dashboards.
- `references/migrating-notes.md`: importing an existing pile of notes safely.
- `references/companion-skills.md`: installing kepano/obsidian-skills and this skill for
  different agents, plus the Obsidian CLI.
- `scripts/scaffold_vault.py`: creates the vault (never overwrites). `--help` for options.
- `scripts/check_vault.py`: read-only health report. `--json` for machine output.
- `assets/`: the templates, Bases and agent rules the scaffold copies; edit them to change
  the defaults.
