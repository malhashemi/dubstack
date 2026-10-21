# Research document

`research.md` is the account later stages read. Each investigator's report holds its area in full; the account connects the areas and carries what a reader needs to decide, with each report one link away. With one area the account may be most of what there is; with many, it is the map through them, and it restates no report.

Keep every section below, and write "None." under a section that has nothing.

````markdown
# <What was researched>: Research

as of: <date> · <commit> on <branch> · <repository>
goal: <path of the goal record, or none>
plan: plan.md · reports: reports/

Research is dated evidence, not a ruling. Each finding says where it came from and when, so whoever uses it can judge how far to trust it. Where a finding and its source disagree, the source is right.

## Summary

<Two to four paragraphs: how the researched area works, and what matters most in it.>

## Findings

### <A takeaway, stated as what is true>

<How it works and what it connects to in other areas, with the key sources woven in: `path:12-40` for code, the link, version, and date for documentation, and what ran and when for an observation. Add a diagram, a call or file tree, a signature, or pseudocode where it shows structure faster than prose. Link the report that holds the detail.>

**Tested by:** <where and how this area is tested today, or that it is not>

## Reports

- [reports/<area>.md](reports/<area>.md) · <the area> · <what it answers, in a line>

## Sources

<The files, directories, documents, and systems the findings rest on, grouped by area, saying where a list is complete and where it names only the main ones.>

## Open questions

- <A question the research could not settle> · <what or who could answer it>
````

## Writing the account

- **Headers state the takeaway.** "Sessions are written to Postgres before the daemon acknowledges them", not a topic ("Sessions") or the question restated ("How are sessions stored?"). A reader skimming the headers alone learns how the system works.
- **Connect, don't restate.** A finding carries its takeaway, what it connects to elsewhere, and the sources a reader needs to judge it; the detail stays in its report.
- **Concept first, location second.** Say what something does, then where it lives, with citations in the prose. Use a range for adjacent lines.
- **Keep each picture beside the prose it explains**, never piled at the end.
- **Describe; do not recommend.** A gap or a limit is a finding when it is a fact, such as an area with no tests or an API's rate limit. What to do about it belongs to the stages that follow.
