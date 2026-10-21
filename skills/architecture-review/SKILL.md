---
name: architecture-review
description: Review a codebase for architectural friction and opportunities to deepen modules. Only use when the user invokes this skill by name.
---

# Architecture Review

Find where the codebase's structure makes it harder for people and agents to change, test, and navigate than it should be, and propose **deepening**: changes that give callers more behaviour through a smaller interface and concentrate change and verification in one place. The user decides which candidates are worth doing. Each one taken up becomes a goal through basecamp, whose design stage shapes the interface, so the review proposes directions and leaves interfaces to that stage.

A pass is project-level work, not a goal. It runs before features or between them, over an area the user names or the parts of the code that change most. Its findings and every candidate it raises stay in the project's Dossier tree, so later passes build on earlier ones and the team can follow what was found and decided.

The code is the only account of the system as it is. Read [the lens](references/lens.md) before exploring: it gives the words the findings use and the friction worth noting.

## Inputs

Find the tree, local copy, and publication commands in the project's `AGENTS.md` entry, and follow its synchronization instructions before reading the local copy. If the project has no home, use `project-home` to create and review it in this session before continuing.

- Read `glossary/glossary.json` and use its current terms. The glossary names the domain; the lens names the structure.
- Read `architecture-review/candidates.json` when it exists: every candidate earlier passes raised, with its status and the user's reasons.
- Read `architecture/` for the reasons behind past decisions. It was frozen when the architecture was delivered, so it explains why the code took its shape but does not describe the code as it is now.

## Choose the scope

Take the area or pain point the user names. Otherwise, look where change happens, since deepening pays off by making future changes easier: read a good stretch of git history, start from the areas that keep changing, and widen the net when the changes are scattered with no clear hot spot.

Work in `architecture-review/<YYYY-MM-DD>-<area>/` in the local copy, naming the area in a word or two. Reuse the folder when continuing a pass; give a new pass a unique suffix if that path is already taken.

Identify the repository, checkout, and commit being reviewed, including any uncommitted changes in scope. Give explorers the same inspection basis and record where their evidence differs from the commit. If the code changes during the pass, reconcile affected findings before judging them together.

## Explore

How to explore is yours to choose, following your standing guidance on models and delegation. Match the effort to the scope: one explorer for one area, one for each area in parallel when the scope spans several, and a quick locating pass first when the codebase is large or the hot spots are unclear.

Start each explorer in a fresh context with the full paths of [the explorer brief](references/explorer-brief.md), the lens, and the glossary, its area, the repository checkout and inspection basis, and the path of its report in `reports/`.

## Judge the candidates

Read the reports and check the evidence each candidate would rest on. A candidate names a deepening: the modules it would change, the friction the code shows, and the direction. A list of smells is not a candidate. Apply the deletion test to every module a candidate calls shallow and give each candidate a strength as the lens describes. Recommend the strongest candidate when the evidence supports taking it up; otherwise say what remains unproven. A pass may find no candidates.

Account for every earlier candidate in scope by checking it against the code. Carry its ID, decisions, and work links forward while its friction remains; another pass does not reset its status. Mark it gone only when evidence establishes that the friction has gone, and record an unresolved check as a limitation. Keep a rejected candidate out while its reason holds; when the friction has grown beyond what the reason covers, reopen it with that reason and the new evidence shown. If friction returns for a gone candidate, reopen the same ID and explain what returned.

When a direction goes against a decision recorded in `architecture/`, show that decision and its reason with the candidate; the candidate still rests on the code's evidence. When a direction needs a term the glossary lacks, propose it in the candidate for the goal's design stage to settle, and leave the glossary unchanged.

Before writing `findings.md` beside the reports or updating `candidates.json`, read [findings and the register](references/findings.md) for their shared format, revision identities, and decision history. Link a candidate to the work that explicitly cites its ID; the reference covers goals and basecamp's route without a goal record.

## Build the page

Give a rendering subagent [the page brief](references/page-brief.md), the pass folder's path, and whether the register page exists yet. Choose its model using your guidance for visual design work. It builds the pass page, and the register page when there is none, publishes the local copy, and returns the links and a coverage report.

Check that every candidate and every earlier candidate in scope appears, each candidate with its evidence, drawing, strength, and choices, and that the links work. Resolve reported merge conflicts using the `AGENTS.md` instructions, reconcile any changed findings or register entries, then have the renderer refresh and publish. Open the pass page for the user and share its link with the recommendation or no-candidate result in a sentence, and wait for choices when there are candidates to consider.

## Fold in the choices

The user decides on the pass page and returns its handoff block, or decides in conversation. When they ask, read the page's answers and comments with `dossier read`. Only the user's choices decide; teammates' choices and comments are input to bring to the user, with who gave them.

Answer a question or challenge in a comment by checking the code. When it shows the candidate was wrong, revise its account and have the page refreshed. Fold in new choices against the candidate revision the user saw, preserving earlier decisions as the register reference describes. If the direction or its justification changed materially, show the change and get a current choice before handing it off. Record the decision's date and any reason the user gave in their own words; an omitted reason stays absent. Publish the register; both pages read it live. Candidates the user leaves alone retain their status, and new undecided candidates remain open.

<important if="resuming a pass to handle feedback or hand off its choices">
Continue from its findings, register, reports, and saved feedback. Reuse evidence that still applies and recheck affected claims when the relevant modules, callers, tests, or dependencies have changed since inspection. Include uncommitted changes in that check. Complete any outstanding publication or verification without repeating the whole exploration. A newly requested review is a new pass.
</important>

## Hand off

End with a message the user can use to start basecamp, shown in a Markdown code block so it can be copied whole: "Use the `basecamp` skill to take in the architecture work taken up from <pass page link>: <the ID, revision, and title of each candidate>. Their findings are in <findings path>, with the explorers' reports in <reports path>. Keep each candidate's ID in its goal's context, or its issue or pull request on the 'Do it now' route. <For each candidate, the decisions it leaves to the user.>" Take those decisions from each candidate's account: the review proposed directions only, so every candidate leaves at least its interface to the user. Stating them lets basecamp record them as open, so the design stage settles them with the user rather than an outline settling them alone. basecamp decides how many goals they become and routes each.

Include taken-up work that still needs a handoff. Check whether existing linked work covers the chosen revision; if it does not, give basecamp the link and the changed direction so it can update or reassess that work. Preserve the earlier link without treating it as delivery of the new scope.

When the user takes up nothing, there is no message.

## Completion

A pass is complete when:

- `findings.md` records the scope, why it was chosen, the code inspected, and any limits on what was established.
- Every candidate rests on evidence in the code, every claim that a module is shallow carries the deletion test's result, and no candidate proposes an interface.
- Every earlier candidate in scope has been checked against the code and accounted for: carried forward, gone, or kept out by its rejection reason. If evidence needed for that check is unavailable, publish the partial account with the check outstanding.
- The pass is listed even when it found no candidates. Its findings, register, and pages agree on candidate identities and revisions; the register supplies current decisions while earlier passes retain their dated evidence.
- The pages cover the account and are published and verified, including feedback persistence and links. Report any check that could not be completed as outstanding.

The choices are complete when every new decision is recorded against the revision reviewed with any reason supplied, untouched decisions are preserved, and every taken-up candidate in this pass is either covered by existing work at the chosen revision or included in the handoff.

<important if="Dossier is unreachable">
Keep the pass locally, give its paths for review, and report publication and any dependent verification as outstanding. Retry those steps when access returns or the pass resumes; publication does not depend on the user making a choice.
</important>

Summarize what the pass found, the recommendation, and any choices made or still awaited. Give the links to the pass page and the register page, and state anything that remains unpublished or unverified.
