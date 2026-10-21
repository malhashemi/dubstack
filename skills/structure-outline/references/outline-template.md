# Outline template

The outline is one Markdown file with two kinds of content:

- **The plan** is everything the user approves: the summary, Desired End State, Owner Setup, Decisions Made While Outlining, each phase's text, Plan Verification, and Revisions. After approval it changes only through a revision.
- **The progress** is what implementation records against the plan: checkbox state, the front matter's `status` after approval, each phase's `### Progress` block, the Plan Verification `### Progress` block, and entries appended to Owner Checks. Implementation writes it and never rewrites plan wording.

The front matter identifies the outline's inputs and view: `design` lists the input paths, `view` is the local HTML path, and `link` is the published URL returned by the renderer. The outlining agent records these fields; implementation updates `status` as progress is recorded.

Keep every section below. Write "None." under a section that has nothing, so a reader can tell empty from forgotten.

Phases keep their numbers once the user has seen the outline, because Owner Setup, Connects lines, comments in the view, and progress reports all refer to phases by number. A phase added later takes a number never used in this outline, such as `2a` for one inserted after Phase 2, so a removed phase's number is never reused. The order of the phase sections is the recommended route. Depends on states the prerequisites and any user-required ordering; the implementing agent can adapt execution within those bounds without renumbering phases.

````markdown
---
status: draft | approved <YYYY-MM-DD> | implementing | implemented
design:
  - <path of each frozen design ledger and other input>
view: <path of the HTML view>
link: <the view's Dossier link>
---

# <What this work delivers>: Structure Outline

<Two or three sentences: what lands for users and in the code, and why.>

## Desired End State

- <What is true for users and in the code once every phase has landed.>

## Owner Setup (before implementation)

- [ ] <What the owner provides> · needed by Phase <N> · <where it goes: env var name, config key, or account; never the secret itself> · <why the agent cannot do it>

## Implementation Overview

- [ ] Phase 1: <the result it lands>
- [ ] Phase 2: <the result it lands>

## Decisions Made While Outlining

- <The mismatch or open question> → <the decision> · design: <entry ID> · <why> · local | decided by the user <date>

---

## Phase 1: <the result this phase lands>

<What lands and why this position is recommended.>

**Delivers:** <design behaviour and constraint IDs this phase makes true, and the approved mockup or state demo file each surface it builds must match>

**Depends on:** <the results or contracts this phase needs before its work can proceed, and why; any ordering the user requires; None when independent>

**Connects:** <where the new code is called from and what it calls, in the existing code and in other phases>

### Change Outline

<The change told in code sketches, in the order that makes it easiest to follow: files first when ownership explains it, a table or contract first when that explains the rest. Short prose between sketches says why the next one matters.>

```diff
 src/share/
 ├── links.ts               ~ resolves expiry before returning a link
+└── expired-page.tsx       + shows the expired-link message
```

### Contracts

```ts
<The full signature of every exported symbol this phase adds or changes. Declare a shared type here if this phase introduces it; later phases reference it by name.>
```

### Verification

<Checks specific to this phase's result. Put whole-tree checks and journeys across phases in Plan Verification.>

- [ ] `<command>` · proves <what>
- [ ] Agent check: <what the agent does in the browser, computer use, a CLI, or an API> · expect <the observable result>

### Progress

Not started.

---

## Phase 2: <the result this phase lands>

<Same shape as Phase 1.>

---

## Plan Verification

<Checks on the final integrated state: the repository's required full checks and journeys across phases. Name an earlier checkpoint and its reason only where one is required.>

- [ ] `<command or agent check>` · proves <the whole-plan result and design IDs it covers>

### Progress

Not started.

## Owner Checks (after implementation)

- [ ] <A check only a person can make> · proves <design IDs> · Phase <N> · <why an agent cannot make it>

## Revisions

- <YYYY-MM-DD> · <what changed in the approved plan> · <why> · approved by the user
````

## Drawing the change

- Draw a `diff` when the shape exists and the point is what changes: `+` for added and changed lines, `-` for removed ones, a space for unchanged context, and `~` after the path to note a change inside a file. Keep only enough context to place the change.
- Draw the whole target shape when most of it is new or when omitted context would hide ownership or order.
- Use tree glyphs (`├──`, `└──`, `│`) for file trees, and keep trees small enough to scan.
- Pick the sketch by the shape: a file tree for ownership, a call tree for control flow, a component tree for UI structure, the schema in the project's own form for persisted data, and pseudocode for logic worth showing.
