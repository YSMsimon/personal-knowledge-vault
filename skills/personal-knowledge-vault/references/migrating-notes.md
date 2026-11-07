# Bringing existing notes in

For a pile of old notes: an Obsidian folder full of "Untitled", a Notes app export, a Notion or
Evernote export, a Downloads folder of Markdown. The aim is a linked vault without losing
anything and without moving secrets deeper in.

## 1. Agree the scope

Ask where the notes are, roughly how many, and whether any are someone else's material (an
employer's, a client's). Those go to a strict wing or stay out. Agree that nothing gets deleted:
notes are merged, archived or parked.

## 2. Park the pile

Move (don't copy) the old notes into one folder inside the vault, for example `Inbox/Legacy/`,
so they are in Obsidian but clearly unprocessed. Keep their original names for now. Tell the
owner `Inbox/` is temporary. The health check skips it if passed `--exclude Inbox`.

## 3. Inventory

List every file with its size, first line and last-modified date. For more than about 50
files, write the inventory to a scratch file outside the vault, not into a note. Group by
apparent topic.

## 4. Screen for secrets

Search for things that should never live in a notes app: passwords, API keys and tokens
(`sk-`, `ghp_`, `AKIA`), card numbers, government ID numbers, recovery phrases. Don't copy them
into new notes. List the files to the owner and suggest a password manager. Leave the files
where they are until the owner decides.

## 5. Triage in batches of 10–20

For each note decide:
- **Keep**: worth its own note. Rename to a claim or a real name, add frontmatter (`created`
  from the file date if known), move it to the right wing and folder, add two honest links,
  list it in a Map.
- **Merge**: a fragment of something larger. Append it under a heading in the target note,
  then move the original to `Archive/`.
- **Archive**: obsolete but kept. Move it to `Archive/` with `status: parked`.

After each batch, run the health check and fix what the batch broke. Show the owner the batch
summary (kept, merged, archived) before starting the next one; small batches keep mistakes
cheap.

## 6. Rename safely

Renaming inside Obsidian updates links automatically. Renaming files directly does not: search
for `[[Old Name` and `[[Old Name|` across the vault and update each link, or the note becomes an
orphan and a hollow node appears for the old name.

## 7. Finish

When `Inbox/Legacy/` is empty, delete nothing; remove the empty folder, run the checker, and
read the report with the owner: orphans, duplicates and untitled files should all be zero.
Unresolved links can stay; they are now a list of notes worth writing.
