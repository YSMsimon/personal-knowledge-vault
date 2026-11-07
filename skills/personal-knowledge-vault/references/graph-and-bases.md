# Graph and Bases

## Contents
1. The shape of the graph
2. Colour groups
3. Reading the graph
4. The two Bases
5. Embedding a Base view
6. Checking links from the command line

## 1. The shape of the graph

Links, not folders, make the graph. With the no-orphan rule the vault grows a spine:

```
                         Home  (map)
            ┌─────────────┼──────────────┐
          Life          Build          Work          ← wing entry notes (maps)
        (private)      (public)       (strict)
        ┌───┴────┐        │              │
     Money    Health   Projects…      Maps…          ← topic Maps
       │         │        │
  Tax Return  Sleep Log  Portfolio Site               ← projects
     │   ╲        │        ╱   │
     │  Receipts Live In One Folder  ── Morning Runs Fix My Sleep   ← atomic notes cross-link
     │
  (Rent Is Due On The First)                          ← hollow node = not written yet
                                      Daily/2026-11-06 ──→ (links out only)
```

- Edges point from the note that contains the link. Maps point down; notes point sideways and
  up (each note's two links often include its project or Map).
- Cross-links between notes in different Maps are what make the graph a web instead of a tree.
  They are also how the owner rediscovers things.
- Links across wings are allowed (a private money note can link a public project) but content
  doesn't move across wings. The link only says the two are related.

## 2. Colour groups

`.obsidian/graph.json` → `colorGroups`. The scaffold writes:

| Query | Colour | Shows |
|---|---|---|
| `[type:map]` | gold | Home, wing entry notes, topic Maps |
| `[type:project]` | green | projects |
| `[type:note]` | blue | atomic notes |
| `[type:source]` | purple | sources |
| `[type:daily]` | grey | daily notes |
| `tag:#private` | red | private notes that have no `type` (see below) |

Obsidian colours a node with the **first** group in the list that matches it, so with this order the
type colours win and `tag:#private` only catches untyped private notes. To see wings instead of types,
drag `tag:#private` to the top in the graph settings.

The scaffold also sets the graph filter to `-path:Templates -file:CLAUDE -file:AGENTS`, so templates and
the agent rules files don't clutter the graph. Queries use Obsidian's search syntax:
`[property:value]` matches frontmatter, `tag:#x` a tag, `path:"Folder"` a folder. If a property
query doesn't colour anything in an older Obsidian version, switch to `path:` queries
(`path:"Maps"`, `path:"Projects"`, `path:"Notes"`, `path:"Daily"`).

Colours are 24-bit integers (`0xFFB454` = 16757844). Change them in Obsidian's graph settings
panel; it writes the file for you. When adding a new `type`, add a group for it.

## 3. Reading the graph

- **Hollow nodes** are unresolved links: the backlog. Big hollow nodes (linked from many notes)
  are the most valuable notes to write next.
- **Islands** (clusters not connected to the spine) are under-linked. Find the Map they belong
  to and add a link; often one link reconnects a whole cluster.
- **A lone dot** is an orphan. Turn on *Orphans* in graph filters to see them.
- **A note with dozens of links that isn't a Map** probably wants to become one.
- The local graph (one note's neighbourhood) is the best view while writing.

## 4. The two Bases

Bases are Obsidian's built-in database views over notes (core plugin *Bases*). Each `.base`
file is YAML: global `filters`, computed `formulas`, display `properties`, and `views`.
The `kepano/obsidian-skills` `obsidian-bases` skill documents the full syntax.

**`Vault Health.base`** reads Obsidian's own link index, which is the authority on what links
where. Views:
- *Orphans*: `file.backlinks.isEmpty()`, excluding Home.
- *Under-linked*: `file.links.length < 2`, excluding Maps.
- *Missing frontmatter*: empty `type`, `status` or `created`.
- *Seeds*: `status == "seed"`, grouped by wing, with days since last edit.
- *Everything by wing* and *Recently touched*.

**`Deadlines.base`** filters to notes that have `due`, computes `days_left` and an urgency
bucket (overdue / this fortnight / next 6 weeks / later), and shows *What's next*, *Overdue*,
*Next 6 weeks* and *By wing*.

Both use a `wing` formula, a nested
`if(file.inFolder("Life"), "Life", if(file.inFolder("Build"), "Build", "Other"))`. When the owner
adds a wing, add a branch to that formula in both files.

## 5. Embedding a Base view

Any note can show a Base inline: `![[Deadlines.base]]`, or one view with
`![[Deadlines.base#What's next]]`. Putting *What's next* on `Home` gives the owner a dashboard
the moment the vault opens.

## 6. Checking links from the command line

- `python3 <skill-dir>/scripts/check_vault.py <vault>` gives a full report without Obsidian
  running. `--home`, `--templates`, `--daily` and `--exclude` adapt it to a vault that wasn't
  scaffolded by this skill. `--json` gives machine-readable output.
- Recent Obsidian versions include a command-line interface that talks to the running app
  (search, backlinks, read, append). The `obsidian-cli` skill from `kepano/obsidian-skills`
  covers it. On macOS it may need a symlink onto your PATH; its index lags file writes by a few
  seconds, so an empty search right after writing a file is not a failure.
- When the script, the CLI and the Base disagree, trust the Base or the CLI. They use
  Obsidian's resolver; the script approximates it.
