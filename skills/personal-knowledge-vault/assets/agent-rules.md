# {{VAULT_NAME}}: operating rules for AI agents

This folder is an Obsidian vault: a personal database of Markdown notes joined by
`[[wikilinks]]`. Read this file before writing anything here. The entry point is
[[Home]]; the rules for the human are in [[How This Vault Works]].

## Wings

{{WING_TABLE}}

Keep wings separate; a note lives in exactly one. Nothing from a private wing goes into
a public note unless the owner says so in plain words. Strict-wing material leaves only
after it is abstracted to the technique: no names, links, IDs or identifying numbers.
Read a wing's entry note before working in that wing.

## Never create an orphan

Every note you create or edit must:

1. **Link out**: at least 2 `[[wikilinks]]` in the body to other notes.
2. **Be linked back**: listed as a `[[link]]` in its parent Map, which is the wing's entry
   note or a Map in `<Wing>/Maps/`. A note no Map lists does not exist.
3. **Have frontmatter** (contract below).
4. **Have a real title**: a claim for atomic notes (`Sleep Debt Compounds.md`), a plain name
   for projects and people. Never `Untitled 3.md`.

If a linked note doesn't exist yet, write the link anyway: an unresolved link is a to-do the
graph shows for free. Never delete a link to silence a warning.

Exceptions: `Templates/` is never linked from a Map; `Daily/` notes link outward only.

## Frontmatter contract

```yaml
---
type: map | project | note | source | daily
status: seed | active | done | parked
tags: [topic]
created: YYYY-MM-DD
due: YYYY-MM-DD   # optional: only for a real, external deadline
---
```

- `type` drives the graph colour (`.obsidian/graph.json`). Adding a new type means adding a
  colour group for it too.
- `due` is for dates imposed from outside: a bill, an application window, an exam, a contract
  date. `Deadlines.base` reads it, and it is the only view that stays correct as dates
  approach. Self-imposed targets and "soon" are not `due`.
- Notes in a private or strict wing carry the tag `private`.

## Folders

| Folder | Holds | Rule |
|---|---|---|
| `<Wing>/<Wing>.md` | The wing's entry note | Linked from [[Home]] |
| `<Wing>/Maps/` | Topic Maps | Every note is reachable from a Map |
| `<Wing>/Projects/` | One note per thing being built or done | Links to its notes and sources |
| `<Wing>/Notes/` | Atomic ideas, one per file | Title is a claim, not a topic |
| `Daily/` | Daily log | Links what was touched that day |
| `Templates/` | Note templates | Never linked from a Map |
| `Attachments/` | Images, PDFs | Embedded in the note they belong to |

## Memory rule

When the owner tells you something durable (a decision, a fact about a project, a constraint,
a date), write it into the relevant note in the same turn and say which note. Chat context
disappears; the vault does not. "Yes, do that" and "I decided X" are memory events too.

## Working rules

- Search before creating. Update the existing note instead of making a near-duplicate; two
  files with the same name make links ambiguous.
- Never delete a note. Set `status: parked`, or move it to `Archive/` and update its Map entry.
- Never store passwords, API keys, card numbers or government ID numbers in the vault.
- Check health with `Vault Health.base` in Obsidian, or the `check_vault.py` script from the
  personal-knowledge-vault skill. When they disagree, trust Obsidian's own link index.
- After any change, tell the owner which notes you created or edited.
