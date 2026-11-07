---
type: note
status: active
tags: [meta]
created: {{TODAY}}
---

# How This Vault Works

A vault gets useful at the point where you can't remember what's in it. That only works if
the links are real. A few habits do all the work. Start from [[Home]].

## 1. Maps, not folders

Folders hold files; [[Home]] and the Maps hold meaning. When you make a note, add it to a Map
the same minute. Folders are storage, Maps are the index.

## 2. Titles are claims

`Sleep Debt Compounds.md` is a note you can link mid-sentence. `Sleep.md` is a junk drawer.
Atomic notes get claim-shaped titles so that writing a sentence naturally produces a link.

## 3. Unresolved links are the to-do list

Writing `[[Some Idea]]` before the note exists is correct. The graph shows it as a hollow
node: your backlog, generated for free. Don't delete them.

## 4. Wings keep audiences apart

Each top folder is a wing for one audience:

{{WING_LIST}}

Private material stays private unless you decide otherwise.

## 5. Deadlines live in `due:`

A hard date from outside (a bill, an exam, an application window) goes in the note's `due:`
property. `Deadlines.base` lists them by urgency; `Vault Health.base` lists orphans and
under-linked notes.

## Working with an AI agent here

`CLAUDE.md` and `AGENTS.md` at the vault root carry these rules, so an agent loads them every
session. Say "write that down" and it lands in the right note with the right links, not in a
new untitled file.

## Reading the graph

Colours come from the `type` property, configured in `.obsidian/graph.json`: Maps, projects,
notes, sources and dailies. Templates and the agent rules files are hidden from the graph. A cluster floating alone is
under-linked; fix it by finding the Map it belongs to.
