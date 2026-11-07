# Companion skills and installing

## kepano/obsidian-skills

Written by Steph Ango (Obsidian's CEO). They teach an agent the file formats this skill builds
on. This skill says *what* to build and keep tidy; those skills say *how* the syntax works.

| Skill | Teaches |
|---|---|
| `obsidian-markdown` | Wikilinks, embeds, callouts, properties: Obsidian-flavoured Markdown |
| `obsidian-bases` | `.base` files: filters, formulas, views, summaries |
| `json-canvas` | `.canvas` files for visual boards and mind maps |
| `obsidian-cli` | Driving a running Obsidian from the terminal: search, backlinks, read, append |
| `defuddle` | Reading web pages as clean Markdown (fewer tokens than raw HTML) |

Install them for the vault (run inside the vault folder). This downloads code from GitHub, so
ask the owner first:

```bash
npx skills add kepano/obsidian-skills
```

The `skills` CLI puts them in `.agents/skills/`, links them for the agents it detects
(Claude Code reads `.claude/skills/`), and writes `skills-lock.json` with a hash of each file so
later updates are visible. Add `-g` to install for the user instead of one vault. If `npx` isn't
available, install Node.js first, or clone the repository and copy each skill folder by hand
(below).

## Installing this skill

**Any agent that supports Agent Skills, via the skills CLI:**

```bash
npx skills add YSMsimon/personal-knowledge-vault        # this vault or project
npx skills add YSMsimon/personal-knowledge-vault -g     # every project, for this user
```

**Claude Code, as a plugin:**

```
/plugin marketplace add YSMsimon/personal-knowledge-vault
/plugin install personal-knowledge-vault@personal-knowledge-vault
```

**By hand:** copy the folder `skills/personal-knowledge-vault/` into the agent's skills
directory:
- Claude Code, one user: `~/.claude/skills/personal-knowledge-vault/`
- Claude Code, one vault: `<vault>/.claude/skills/personal-knowledge-vault/`
- Other agents: their skills folder (many read `.agents/skills/`), or let `npx skills add`
  find it.

Then start a new session and ask something like "set up a personal database in Obsidian for
me". The skill should load on its own; if it doesn't, name it.

## The agent rules file

The scaffold writes the same rules twice: `CLAUDE.md` (read by Claude Code) and `AGENTS.md`
(read by Codex, Cursor, Gemini CLI and others). If the owner edits one, copy the change to the
other, or replace one with a single line pointing at the other.

## Obsidian itself

- Download from obsidian.md. It is free for personal use.
- *Open folder as vault* on the scaffolded folder.
- Settings → Core plugins: make sure *Bases*, *Templates*, *Daily notes*, *Graph view* and
  *Backlinks* are on. The scaffold already pointed Templates and Daily notes at the right
  folders.
- Obsidian Sync or a Git repository keeps a backup. If the vault goes into a public repo or a
  published site, exclude private and strict wings first.
