# personal-knowledge-vault

An Agent Skill that lets your AI coding agent (Claude Code, Codex, Cursor, Gemini CLI and
others) build and run a personal database in Obsidian, and keep it linked as it grows.

You talk; the agent writes notes, links them into Maps, puts deadlines where a dashboard can
see them, and keeps private material in private folders. Obsidian shows it all as a graph.

## What you get

```
MyVault/
├── Home.md                  ← start here: links to every wing
├── How This Vault Works.md
├── CLAUDE.md, AGENTS.md     ← rules your agent reads every session
├── Deadlines.base           ← every dated note, by urgency
├── Vault Health.base        ← orphans, under-linked notes, stale seeds
├── Templates/  Daily/  Attachments/
└── Life/  Build/  Work/     ← "wings", one per audience (you choose them)
    ├── Life.md              ← the wing's Map
    ├── Maps/  Projects/  Notes/
```

The rules the agent follows:

- **No orphans.** Every note links to at least two others and is listed in a Map. A note no
  Map lists is a note you'll never find again.
- **Titles are claims.** `Receipts Live In One Folder`, not `Receipts`.
- **Unresolved links are your to-do list.** Link ideas before you write them.
- **Wings by audience.** Public, private and strict folders never mix.
- **Real deadlines go in `due:`.** Then `Deadlines.base` can sort them.
- **Chat dies, the vault doesn't.** Tell the agent something durable and it writes it into
  the right note in the same turn.

How the graph comes out:

```
                 Home
       ┌──────────┼──────────┐
     Life       Build       Work        wings
      │           │           │
    Money      Projects     Maps        topic Maps
      │           │
  Tax Return ── Portfolio Site          projects
      │      ╲      │
  Receipts Live In One Folder ── …      notes cross-link
      │
  (Rent Is Due On The First)            hollow = not written yet
```

## Install

You need [Obsidian](https://obsidian.md) and an agent that supports skills.

**Any agent, with the skills CLI** (needs Node.js):

```bash
npx skills add YSMsimon/personal-knowledge-vault -g
```

**Claude Code plugin:**

```
/plugin marketplace add YSMsimon/personal-knowledge-vault
/plugin install personal-knowledge-vault@personal-knowledge-vault
```

**By hand:** copy `skills/personal-knowledge-vault/` to `~/.claude/skills/` (Claude Code) or
your agent's skills folder.

Recommended companion skills, which teach the agent Obsidian's file formats:

```bash
npx skills add kepano/obsidian-skills
```

## Use

Start a new agent session and say something like:

- "Set up a personal database in Obsidian for me. I want separate areas for my health and
  money, my side projects, and my job."
- "Bring my old notes in `~/Downloads/notes-export` into the vault."
- "Write down that my lease renews on March 1."
- "Check my vault for orphans and fix them."

The agent asks a few questions, runs the scaffold, and walks you through opening the vault in
Obsidian.

The two scripts also work on their own:

```bash
python3 skills/personal-knowledge-vault/scripts/scaffold_vault.py --vault "~/Documents/My Vault" \
  --wing "Life|private|Health, money, family" --wing "Build|public|Things I share"
python3 skills/personal-knowledge-vault/scripts/check_vault.py "~/Documents/My Vault"
```

The scaffold never overwrites an existing file. The checker only reads.

## Author

Shimeng (Simon) Yang · [github.com/YSMsimon](https://github.com/YSMsimon)

## Credits

The conventions come from a real vault of 1,100+ notes run by an agent since August 2026.
Obsidian skills by [Steph Ango (kepano)](https://github.com/kepano/obsidian-skills).

## License

MIT
