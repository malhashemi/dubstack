# Ledger format

The ledger is the agent-facing record of the interview and the content source of truth for the page. The builder, the interviewer, and downstream stages all read it. Keep it a set of lists, not a document: no narrative and no sections beyond the lists below and those the profile declares. The ledger decides what must be present; the builder decides sections, order, and visuals.

Keep it current, not cumulative. After each round it describes the present state, and the delta is the only part that speaks of the round. Change every entry a decision reaches and leave the rest as they are, so what was copied exactly stays exact.

## Structure and identities

The header records the `profile`, the `round`, the current `phase`, the page path (`artifact`), the `answers-form` (its target and `id`) and `regions` layout as the builder reports them, the `inputs`, the `confidentiality` line (limits on quoting and sharing source material, including publication to the team), and the `honest-state` (decided versus implemented, in one line).

| List | ID | Content |
| --- | --- | --- |
| Language | `T-01` | Project terms and their definitions. |
| Settled | `S-01` | Established facts and decisions, with sources and rationale. |
| Behaviours | `B-01` | Observable outcomes, when the profile declares the list. |
| Constraints | `C-01` | Rules that hold everywhere, when the profile declares the list. |
| Out of scope | `X-01` | Ideas left out of this work, deferred or rejected. |
| Deferred questions | `D-01` | Questions a named later stage decides. |
| Frontier | `r1-q1` | This round's questions. |
| Not yet on the frontier | `N-01` | Open topics, each with what it waits on. |
| Delta | Existing IDs | What changed since the previous round. |

IDs are stable for the life of the interview: retire and add, never renumber, and never reuse an ID for another meaning. An unanswered question keeps its original ID in later rounds while its meaning holds, even though its prefix names an earlier round. When a not-yet topic becomes a question, or an answer becomes settled entries, link the new entry to the one it came from.

Options have identities too: within a question, a letter keeps its meaning for as long as the question lives. Saved answers are keyed by question ID and option letter, so these identities are what keep an earlier answer from landing on a choice the user never made.

A question leaves the frontier in one of three ways, and saved answers follow the difference:

- **Resolved:** its answer became settled entries. The page drops the question; its saved answer has done its job.
- **Dropped:** it left scope, as an Out of scope entry or a deferred question. The page drops it too.
- **Superseded:** its meaning changed. A new question replaces it and records `replaces=<old ID>`, and a saved answer to the old question shows on the new one as needing a new answer. An option whose meaning changes is superseded the same way within its question: it gets a new letter, the old letter is never reused, and a saved answer naming the old letter shows as needing a new answer.

`phase` and `group` values come from the profile. They help agents find entries and give the builder drawing hints; the page's sections need not mirror them.

A profile may declare lists of its own, placed after Settled, each with a heading, an ID prefix, an entry shape, and a page rule. A profile whose lists hold what the interview establishes, as requirements gathering and brainstorming do, uses them in place of Settled. Stable IDs, current state, the delta, and the coverage check apply to these lists too; the profile defines their content and what the page shows.

## Settled entries

Every settled entry names its `source`: an upstream document reference, a codebase fact, the question and option that decided it, or a decision the user explicitly delegated. A decided entry also carries `why`, its rationale in one line; downstream stages read it. A proposal the user has not approved stays with the open question it informs.

`over` records each real contender that lost, one field per option: its letter, its label, and why it lost. Write it when a question resolves. When a later decision replaces a settled entry, add the replaced choice as an `over`. If the user chose against the recommendation, `why` gives their reason (or `user choice, no reason given`) and `over` names the recommendation. `over` explains the present choice, so it stays as long as the entry does.

A fact found during the interview carries `found=r<N>`, the round it was found in, beside its `source`. At handoff these entries are appended to the research artifact. When a decision rests on a finding that is uncertain, say so in the entry.

Terms follow the glossary shape: what the thing is in one or two sentences, then words to avoid. Add an `example:` sentence or `related: <term> <how>` entries when useful. A relation names a seeded term by its glossary `id`, or a new term by its ledger ID.

A term seeded from the shared glossary carries `source=glossary/glossary.json` and `id=<glossary id>`; a term from another input names that source. Keep the glossary ID separate from the ledger's `[T-nn]` identity. Mark terms added or changed in the interview with `new` and `since=<round>`, so the page and handoff can distinguish them from seeded terms.

## Out of scope and deferred questions

An Out of scope entry is `deferred` (not in this work; it may return in a later PRD or goal) or `rejected` (not this product). A rejection's `why` is durable: the scope, a constraint, or a decision, never a temporary circumstance.

A Deferred questions entry names the later stage that decides it (`for=`) and the context that raised it. That stage takes it up among its first questions; this interview does not ask it.

## Frontier questions

Consequences are content. For every option, not only the recommended one, write what becomes true if it is chosen, what it costs or risks, and what it rules out. Name an exclusion only when the option genuinely rules something out; options that differ in effort, likelihood, or reversibility say that instead of inventing an absolute. The consequence is what the page draws; the label only names it.

Questions are decisions unless the profile names other kinds. Every question carries its framing and a visual idea (`draw-as`):

- A decision question has options and, by default, a recommendation with its strength (`strong`, `worth exploring`, or `speculative`) and reason. The profile may omit recommendations for particular kinds of question. When one is required but the context cannot support it, say what is missing.
- A discovery question gives the context that prompts it, such as the scenario so far or an example to react to, without options or a recommendation.
- A prompt that opens possibilities invites the user's own ideas.

For comparisons, `compare-on` names the applicable criteria from [comparing options](comparing-options.md). The builder may improve on `draw-as`, but must still show the comparison. `depends-on` and `defers` record dependencies between questions.

Fit the options to the question. Lettered alternatives suit most decisions; a proposed direction open to correction, or an open prompt, suits a question where alternatives would be invented. A question that is ready but held back for a more focused round stays under Not yet with `held=` and the reason, keeping its `depends-on`. It enters the frontier once its prerequisites are settled and the hold is released; if a prerequisite reopens, it waits on that again.

## Exact artifacts

Attach an exact artifact when an entry or option is a shape: a contract, schema, signature, sequence, message, or code sketch. Indent a fenced block under it, and say whether it is a binding contract or an illustrative sketch. Copy it exactly, and write identifiers (types, endpoints, tables, fields, paths) in backticks as the artifact or code spells them. When an option is chosen, its artifact moves unchanged into the settled entry; a later design change edits the artifact here first. If the confidentiality line forbids copying a source's artifact, cite it in `source` instead.

An approved mockup or state demo is a file artifact: `artifact=artifacts/<ID>-<slug>.html`, beside the ledger. Name it when the question resolves; the next revision saves the chosen drawing there. From then on the file is exact: every revision embeds it unchanged, and it freezes with the ledger at handoff. A proposed change to that design is a new question with its own drawing, and the approved file stays as it is until the change is decided.

## Behaviours and constraints

The PRD and design discussion profiles declare these two lists, placed after Settled. Their IDs stay citable through the outline, implementation, and review.

```markdown
## Behaviours
- [B-07] actor=Guest | when: opens an expired share link | sees: "This link has expired. Ask the owner for a new one." | situation=fails | beside=S-12 | source=r3-q2(b)

## Constraints
- [C-02] kind=privacy | Guest email addresses are never stored. | source=legal note in the goal
```

A behaviour names its actor, the moment (`when`), what the actor observes (`sees`), its `situation` (`main`, `empty`, `fails`, `denied`, or `shared` for one that covers every flow), the settled flow or mockup it belongs to (`beside`), and its source. A constraint names its `kind` (`privacy`, `platform`, `accessibility`, or `business`), the rule, and its source. Add a situation or kind when the product needs a distinction these do not express. The profile's page rules say where each list appears on the page.

## Delta

The delta lists only IDs and one-line reasons for what changed since the previous round: `+` added, `~` rewritten, `-` resolved, dropped, superseded, or promoted, `=` carried over unanswered. Rewrite it each round; never append to it.

## Example

````markdown
# Ledger: <subject>
profile: tdd-target.md
round: 2
phase: system
artifact: <goal directory>/<profile>-interview/index.html
answers-form: <target and id, as reported by the builder>
regions: <layout as reported by the builder, one line per region>
inputs: <upstream documents, one path each>
confidentiality: <limits on quoting and sharing source material, including publication to the team>
honest-state: <decided vs implemented, one line>

## Language
- [T-01] Capsule | A small TypeScript app that a publisher pushes to an installation. | avoid: app, project, site | source=glossary/glossary.json | id=core.capsule
- [T-02] Deployment | One capsule's stable identity across code versions. | avoid: deploy, instance | new since=r2

## Settled
- [S-01] phase=system group=components | Capsules run on separate browser origins from the dashboard. | source=SRS AUTH-03 | why=browser storage isolation is the only enforcement a capsule cannot bypass | since=r0
- [S-09] phase=system group=delta | Milestone one: install, admin bootstrap, invite, CLI login, publish a data-free hello capsule, visit on its own origin, list and inspect. | source=r1-q1(a) | why=crosses every package without the transaction design | since=r1
- [S-10] phase=system group=contracts | The CLI signs in through a device-code flow on `POST /api/cli/device-code` and `POST /api/cli/token`. | source=r1-q3(b) | why=user: the CLI runs on headless build hosts | over=(a) localhost redirect: needs a browser on the same machine; was the recommendation | since=r1
  ```text
  POST /api/cli/device-code                -> { deviceCode, userCode, verificationUrl, interval }
  POST /api/cli/token  { deviceCode }      -> { accessToken, expiresAt } | { error: "authorization_pending" }
  ```

## Out of scope
- [X-01] deferred | Capsule sign-in in milestone one | source=r1-q1(a) | why=waits on the Google consent-audience question
- [X-02] rejected | Capsules sharing the dashboard's origin | source=S-01 | why=browser storage isolation is the only enforcement a capsule cannot bypass

## Deferred questions
- [D-01] for=outline | Which milestone-one slice lands first | source=r2-q1 | context=every slice needs the Worker creation path

## Frontier (round 2)
- [r2-q1] Capsule Worker creation
  phase: system
  framing: how the platform creates and talks to a capsule's Worker
  draw-as: one control-flow sketch per option, platform on the left, capsule on the right
  (a) strong | Platform calls the Cloudflare API to create a Worker per capsule; talks to it over a service binding. | true: per-capsule isolation; costs: a Cloudflare API credential in every environment; rules out: running this path locally without credentials
    ```ts
    createCapsuleWorker(capsule: CapsuleId, version: VersionId): Promise<WorkerBinding>
    ```
  (b) | Platform hosts all capsules in one Worker behind a dispatcher. | true: single deploy; risks: one faulty capsule affects every capsule; rules out: separate origins without extra routing
  why: (a) keeps the origin invariant with the least routing machinery
  compare-on: seam placement, locality of the routing logic
  defers: N-04
  depends-on: S-09
- [r1-q6] Where the CLI stores its token
  phase: system
  framing: where the CLI keeps its access token between runs
  (a) worth exploring | OS credential store | true: token kept out of plain files; costs: a separate code path for each platform
  (b) | Permission-restricted file in the user's config directory | true: one code path, easy to inspect; risks: any process running as the user can read the token
  why: (a) matches how the CLI already stores its telemetry opt-out
  depends-on: S-10

## Not yet on the frontier
- [N-04] Custom domain attachment | depends-on=r2-q1
- [N-05] Docs-site scope for milestone one | depends-on=S-09
- [N-06] Capsule deletion and data retention | depends-on=S-01 | held=its own round; it sets retention for every capsule's data

## Delta since round 1
+ S-09..S-16 added from r1 answers
+ T-02 proposed
+ X-01 recorded
+ N-06 added, held for its own round
~ S-03 rewritten: hostname strategy now lives in the domains module
- r1-q1..r1-q3, r1-q5, r1-q7, r1-q8 resolved into S-09..S-16
- r1-q4 superseded by r2-q3: S-09 changed what it asks
= r1-q6 carried over unanswered
- N-01, N-02 promoted to r2-q1, r2-q2
````
