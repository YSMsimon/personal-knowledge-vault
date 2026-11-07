# Conventions

How notes are written, named and linked. The vault's own `CLAUDE.md` / `AGENTS.md` wins over
this file if the owner changed a rule there.

## Contents
1. Frontmatter contract
2. Types and when to use each
3. Titles
4. Links
5. Maps: when and how
6. Daily notes
7. Templates
8. Worked examples

## 1. Frontmatter contract

```yaml
---
type: map | project | note | source | daily
status: seed | active | done | parked
tags: [topic, private]
created: YYYY-MM-DD
due: YYYY-MM-DD   # optional
---
```

- **type** is the role a note plays, not its topic. It drives the graph colours and the Bases.
  Adding a type is allowed (an owner may want `person` or `recipe`), but add a colour group in
  `.obsidian/graph.json` at the same time, or the new notes render grey.
- **status**: `seed` = started, thin; `active` = in use or in progress; `done` = finished, kept
  for reference; `parked` = paused or superseded (instead of deleting).
- **tags** are for cross-cutting facets (`money`, `health`, `reading`). Don't mirror the folder
  in a tag. Every note in a private or strict wing gets `private`, so the graph can colour it
  and any publishing step can exclude it.
- **created** is the date the note was made, ISO format.
- **due** only for a date imposed from outside: a tax deadline, a visa expiry, an application
  window, an exam, a renewal. Put the date in the sentence too, but the property is what
  `Deadlines.base` sorts. "I want to finish by Friday" is not `due`.

Extra properties are fine when they earn their place (`link:` on a source, `amount:` on a bill,
`people:` on a meeting). Keep names lowercase and consistent across notes, because Bases filter
on them.

## 2. Types

| type | Is | Lives in | Typical links |
|---|---|---|---|
| `map` | An index note that lists and explains other notes | `Home.md`, `<Wing>/<Wing>.md`, `<Wing>/Maps/` | Down to its notes; up to its parent Map |
| `project` | One thing being built or done, with a state and a next step | `<Wing>/Projects/` | Its notes, sources, people, deadlines |
| `note` | One idea, fact or decision | `<Wing>/Notes/` | 2+ related notes and the project it serves |
| `source` | Something read, watched or heard, in your words | `<Wing>/Notes/` (or a `Sources/` folder if many) | The notes that use it |
| `daily` | The day's log | `Daily/` | Everything touched that day |

## 3. Titles

- **Atomic notes get claims**: `Receipts Live In One Folder`, `Morning Runs Fix My Sleep`,
  `Rent Is Due On The First`. A claim can be dropped mid-sentence as a link and still read.
- **Projects, people, places, sources keep names**: `Tax Return 2026`, `Dr Lee`,
  `Atomic Habits`.
- **Maps are topics**: `Money`, `Health`, `Reading`.
- Never `Untitled`, never a date alone (except daily notes), never a vague bucket like `Misc`.
- Avoid characters Obsidian can't use in links: `# ^ [ ] |` and `\ / :` in file names.
- File names must be unique across the vault. Before creating, search for the name; if a
  similar note exists, extend it.

## 4. Links

- Link where the connection is real, inside a sentence: "Filing is easier because
  [[Receipts Live In One Folder]]." A bare list of links at the bottom is weaker but acceptable
  for Maps.
- Two links out is a floor, not a goal. A note that can't find two honest links is usually
  either too thin (merge it) or missing its Map.
- Use aliases when the sentence needs different words: `[[Tax Return 2026|this year's return]]`.
- Link to a heading with `[[Note#Heading]]`; embed with `![[Note]]` or `![[image.png]]`.
- Unresolved links are fine and intended. They are the backlog of notes worth writing.
- When renaming a note, do it in Obsidian (it updates links) or update every link yourself.

## 5. Maps

- `Home` lists the wings. Each wing's entry note lists its topic Maps, active projects and
  loose notes.
- Start a topic Map when a topic has roughly six or more notes, or when the entry note's list
  for that topic gets long. Move the links into the new Map and leave one line in the entry
  note pointing to it.
- A Map line is a link plus a few words on why it matters:
  `- [[Rent Is Due On The First]]: autopay set on the 28th`.
- A Map can have sections (`## Active`, `## Reference`, `## Parked`). It's fine for a note to
  appear in two Maps.
- Every note should be reachable from `Home` in a few hops. If it isn't, a Map is missing a
  link.

## 6. Daily notes

`Daily/YYYY-MM-DD.md`, made from the daily template. Log what was done and decided, and link
every note touched. Daily notes are leaves: nothing has to link to them and they are excluded
from the orphan check. Durable facts don't stay in a daily note; they go into the note they
belong to, and the daily links there.

## 7. Templates

`Templates/` holds Note, Project, Map, Source and Daily templates. Obsidian's core Templates
plugin fills `{{title}}` and `{{date:YYYY-MM-DD}}`. When writing a file directly as an agent,
copy the template's structure and fill those values yourself. Templates are never linked from
a Map and are excluded from all checks.

## 8. Worked examples

**The owner says:** "My passport expires March 3 2027, I need to renew it."

Write `Life/Projects/Passport Renewal.md`:

```markdown
---
type: project
status: active
tags: [project, private, admin]
created: 2026-11-06
due: 2027-03-03
---

# Passport Renewal

The passport expires on 2027-03-03. Renewal takes several weeks, so start by January.
Photos and the form go in [[Admin Documents Live In One Folder]]; travel this spring depends
on it, see [[Spring Trip]].

## Next step
Book a passport photo.
```

Then add `- [[Passport Renewal]]: expires 2027-03-03, start by January` to the Life wing entry
note (or its `Admin` Map), and tell the owner both files changed. `Spring Trip` and
`Admin Documents Live In One Folder` may not exist yet; that is fine.

**The owner says:** "Write down that I decided to stop using the budgeting app."

Find the existing money note or project (search "budget"). Add a dated line under a
`## Decisions` heading there, for example
`- 2026-11-06: stopped using the budgeting app; tracking in [[Monthly Budget]] instead.`
Don't create a new note for a single decision that belongs to an existing one.
