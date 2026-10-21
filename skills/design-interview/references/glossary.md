# Glossary

The project's shared vocabulary lives in `glossary/glossary.json` in its local copy. This skill settles new and changed terms with the user. Other stages read and use those terms and never add to the glossary; basecamp marks a goal's proposals current when the goal completes.

During the interview, the ledger's Language list is the working copy. At handoff, write its new and changed terms into `glossary.json`, leaving repository glossary files unchanged. A term keeps its `id` through a rename. Within a context, one name identifies one concept.

## What belongs

Terms specific to this project's domain, whose names or boundaries matter to the work. General programming concepts (timeout, retry, cache) and design vocabulary (module, seam, adapter) stay out even when the project uses them heavily, unless the project gives one a meaning of its own.

One term per concept. When several words name the same thing, choose the clearest and list the others under _Avoid_, with the reason when a near-synonym means something else.

A definition says what the thing is, in one or two sentences, with enough context to tell it apart from related concepts. What it does and how it is built belong in the design.

## Reading it at the start

Read `glossary/glossary.json` and seed the Language list from the contexts the work touches, with the vocabulary in effect for this goal:

- Start with the `current` terms, keeping their definitions as written.
- Include this goal's own `proposed` terms from earlier design stages. A proposal replaces the matching current term in the Language list or adds a term the glossary does not yet have as current. These terms are agreed for this goal, though not yet current for the project.
- Use other goals' proposals as context where they bear on the work; they do not settle this interview's vocabulary. If another goal already proposes a change to a term you need to change, name that goal to the user and leave the term unchanged until the goals' owners agree.

Keep each seeded term's glossary `id` on its ledger entry (`id=`), so the term keeps its identity through a rename.

Also read the Language list of any earlier design stage supplied as input, such as a PRD for a TDD. Carry forward its agreed terms that the glossary does not yet hold. If the repository keeps additional vocabulary in a file such as `CONTEXT.md`, seed from it too and tell the user, leaving the file unchanged. When sources disagree on a definition, surface the difference for the user rather than silently replacing the shared glossary's definition.

For an interview within a goal, read comments on that goal's proposed terms each round. Use `dossier read --json` on the glossary page's `index.comments/` and identify the threads by their term `id` anchors. Fold them in as you would comments on the interview's terms, then resolve the threads you folded in.

A seeded definition is settled. Changing what a term means is a decision for the user: raise it as a question rather than rewriting the entry. A term the interview adds is different: it is a proposal the user reviews on the page, recorded at once and agreed unless the user comments on it.

## Writing the changes at handoff

Write only terms added or changed by this interview or an earlier design stage whose ledger you used.

Each glossary entry holds `id`, `term`, `definition`, an optional `example`, `avoid`, optional `related`, `context`, `status`, `goal` for a proposal, and `since` (the date); the file's existing entries show the shape. `node glossary/_check.mjs` in the local copy checks the file against the rules, and the project's `AGENTS.md` publish commands run it. Map each Language entry to an entry, retaining its glossary `id` and omitting its ledger ID. Give new terms a unique `<context id>.<slug>` ID derived from their name. A rename keeps the ID and adds the previous name to `avoid`. Resolve each relation's ledger reference to a glossary ID for its `to` field. Keep optional examples and relations unless the interview changes them.

- **For a goal,** write new and changed terms as `proposed`, with the goal's slug. Keep the current entry with the same `id` until the goal completes. Update this goal's earlier proposal when one exists, subject to the ownership rule above.
- **Without a goal,** as for the Solution Architecture and Glossary profiles, the user has agreed the terms for the whole project: add each new term as `current`, and replace the current entry of each changed one.

Preserve unrelated entries and other goals' proposals, and add new contexts to `contexts`. Follow the project's `AGENTS.md` commands for checking and publishing the glossary and resolving merge conflicts. Independent term changes can coexist; competing definitions of the same entry need the user's decision.

When the project has no `glossary.json`, keep the terms in the frozen ledger's Language list.

## Examples and relations

Add an `example` when one sentence using the term helps distinguish it from similar terms. Record an agreed relationship in the source term's `related` list: `{ "to": "<term id>", "how": "<short verb phrase>" }`. Read it as a sentence, such as "Order *leads to* Invoice". Relations can cross contexts and describe how those contexts connect. A relation change follows the same proposal rules as any other change to a term.

## Several contexts

Most projects have one context. When the same word means different things in different parts of the project (a platform's language and its users', for example), split by context: each context is an entry in `contexts`, with its `id`, its `name`, and what it is (`about`). Each term names its context, and relations between terms record how the contexts connect. Give each meaning its own entry in its own context; merging conflicting meanings into one entry loses the distinction the split exists for. Many terms in a single context do not call for a split.

In a project with several contexts, each ledger term names its context, as in `[T-03] Invoice | ... | avoid: bill | context=billing`. Infer the context from the topic; when it is unclear, ask in the round.
