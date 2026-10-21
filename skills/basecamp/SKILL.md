---
name: basecamp
description: Clarify a goal, choose its next step, and maintain its record and page across stages. Only use when the user invokes this skill by name or an earlier stage's handoff names it.
---

# Basecamp

Start with what the user wants, from a precise one-line change to a loose set of ideas. Identify what stands between that goal and working code, then choose the next step. For work that spans sessions, maintain the goal's record and page as each stage finishes so the user can see its progress and next steps.

Choose the route by what remains unresolved, not by the goal's size: the user's intent, missing facts, or decisions that require the user. Use the "Do it now" route when the work is ready for the current session; otherwise, select the stages needed to resolve those gaps.

## Taking in a goal

Keep goals in the project's Dossier tree so the team can follow them alongside the project home. Find the tree, local copy, and publication commands in the project's `AGENTS.md` entry. If the project has no home, use `project-home` to create and review it in this session before continuing. Follow the entry's synchronization instructions before editing the local copy.

Use the user's request, supplied material, and repository to understand the goal. Inspect enough of the repository to choose a route: whether the capability already exists, where the change belongs, and what it affects. Leave deeper investigation to the research stage when needed. Read `glossary/glossary.json` in the local copy so the goal uses terms that later stages can recognize.

Keep what the user supplies apart from the goal itself. What they require, such as a platform, a library, or a limit, becomes scope; everything else they point to, such as documentation, reference files, or earlier research, is context for later stages to consult. Later stages start in fresh sessions, so keep in `context/` in the goal's directory whatever material from the conversation they will need, such as pasted text or a screenshot.

Ask the user only what would change what the goal is, its scope, or the next step. Put every such question in one message, each with your recommendation. Facts are yours to find. A question about how the result should work or look is a decision for the design stage; record it under Open rather than asking it now.

Phrase the goal so the stages after it read it in the project's language: where the user describes something the glossary already names, use its term, and describe plainly a concept it lacks. When your wording or your reading goes beyond the user's words, as it does for a changed term or a loose or wide-ranging request, state the goal as you understand it: the outcome, for whom, why, what done looks like, and what you set aside. Let the user correct it before you choose the next step. A precise request in the project's terms needs no read-back.

Requests given together stay one goal unless they are really separate goals; then propose the split.

## Choosing the next step

Choose from the stages below by what the goal still lacks, explain the choice in a sentence, and let the user override it. The route is chosen after intake and again after research. The other stages have a fixed next step, which you change only when what a stage found calls for a different route.

| Step | Skill | Choose it when | Then |
|---|---|---|---|
| Do it now | the session that chose it | the intent is clear, the facts can be found while working, nothing is left for the user to decide, and the work fits one session | Pull request, for a code change |
| Research | `research` | the next decision waits on facts too large to find along the way, or on facts best found without the goal steering them | Choose again |
| Design discussion | `design-interview`, design discussion profile | decisions remain for the user, and the product and technical choices are entangled in one piece of work | Structure outline |
| PRD | `design-interview`, PRD profile | the product framing itself is open, or the product and technical design are large enough to settle separately | TDD |
| TDD | `design-interview`, TDD profile | a PRD has been approved | Structure outline |
| Structure outline | `structure-outline` | a design has been approved, or nothing is left for the user to decide but the work needs several phases | Implementation, once the user approves the outline |
| Implementation | `implement-outline` | an outline has been approved | Pull request |
| Pull request | `describe-pr`, then `babysit-pr` | the change is committed on its branch | Done once merged |
| Split | the session that chose it | the goal is really several goals, or too large and unclear to design in one stage | Take in each part as its own goal |

A new kind of stage joins the route as a row here: what it is, its skill, when it is the right next step, and what follows it.

## Starting the goal

Open a GitHub issue for each goal. Give it a title that names the goal and describe the goal and scope for repository readers, omitting local paths. If the repository has no GitHub remote, report that and continue without an issue.

For goals with pages, begin the issue body with one line of Dossier links, starting with the goal page. Apply a `stage:<stage>` label for the current stage, creating the label if needed.

Give every goal a directory at `goals/<slug>/` in the project's local copy. Choose a short, unique slug. Stages store their artifacts there for publication with the tree; keep unpublished material in a `private/` folder.

<important if="the next step is to do it now">
Make the change in this session on a separate branch named by the repository's conventions. Verify it with appropriate tools, such as a browser for a visible change. When users can see or do something new, capture a demo during verification and save it in the goal's `demos/` directory. Examples include before and after screenshots, a short video, or a terminal transcript. Keep each file under Dossier's 50 MiB limit, compressing videos as needed. Commit the change and hand off to the pull request stage.

This route needs no goal record, goal page, or entry in `goals/goals.json`. Share its demos through the pull request.
</important>

For other goals, read [the goal record](references/goal-record.md) and write `GOAL.md` in the goal's directory. Add an entry to the `goals` list in `goals/goals.json` with `slug`, `title`, `link`, `opened` in `YYYY-MM-DD` format, and `status` set to `open`. Have the page rendered and published, then hand off to the next stage.

## When a stage finishes

A completed stage returns the path to its goal record. Synchronize the local copy, then read the record and the stage's artifacts. Update the record to reflect the result:

- Add the stage, its artifacts, and its outcome to Stages.
- Remove resolved items from Open and add newly raised questions.
- Update the front matter and Waiting on the user.

Choose the next step using the routing guidance. Have the page refreshed and published. When an issue exists, add the completed stage's page to its opening links if that stage has a page, and update its `stage:` label. Then prepare the handoff.

<important if="the record lives outside the project's local copy, as for goals begun before the project had a tree">
Continue at the recorded paths. Keep the page local, open it for the user, and leave the goal out of the published tree and goal list.
</important>

Basecamp is the only writer of the record and page, including page work delegated to its renderer. Stages read the record and own the artifacts they create in the goal's directory.

A goal is complete when its change has merged, or when the requested outcome has been delivered if no code change was needed. Record completion as the final stage and set its `status` in `goals/goals.json` to `done`. Promote this goal's proposals in `glossary/glossary.json` to `current`, remove their `goal` fields, and replace any current entries with the same `id`. Preserve other goals' proposals and tell the user about open comment threads on the promoted terms. Refresh and publish the page as for any completed stage, and close the issue if the merge did not close it.

## The page

The page shows the goal's status and provides access to its artifacts. Give a rendering subagent [the page brief](references/page-brief.md), the record's path, and a short summary of changes since the last render. Identify goals that must remain local. Select the subagent's model using the available guidance for visual design work.

You own the record's content; the renderer owns presentation and publishes the local copy. Check its coverage report against the record: every stage, artifact, open item, and item waiting on the user must appear, and links must work on the published page. Resolve any merge conflicts the renderer reports, then request a fresh render and publication. If a merge changed the record, reconcile it and have the page refreshed and published again.

## Handing off

End with a message the user can use to start the next stage, shown in a Markdown code block so it can be copied whole. Name its skill and, for `design-interview`, its profile. Include the record path, goal directory, and any context the completed stage identified for its successor, such as a branch and worktree or an approved outline. Close with: "When this stage is complete, use the `basecamp` skill with <record path> to record it; it writes the handoff to the next stage." Open the goal page for the user alongside the message.

For a goal done now, the message names the branch, its worktree, the issue, and the goal's directory with its demos, and needs no closing line.

## Completion

Taking in a goal is complete when:

- The goal says what the user meant, in the glossary's terms where it has them: where your wording or reading went beyond the user's words, the user has seen it and corrected or accepted it.
- Every question that would change the goal, its scope, or the next step is answered, or recorded under Open for the stage that will answer it.
- The issue is open, or your report says why there is none.
- The next step is chosen, with its reason.
- For the "Do it now" route, the change is verified, committed on its branch, and handed to the pull request stage.
- For other goals, the record is written, the goal is listed in `goals/goals.json`, the published page reflects the record, the issue links to it when an issue exists, and the handoff message is ready.

Recording a completed stage requires a current record and page that account for its artifacts, resolved questions, and new questions. Any issue must link to the stage's page when one exists and carry the current stage label. The handoff must be ready unless the goal is complete.

For goals maintained outside the project tree, apply these completion checks to the local record and page without requiring listing or publication.

<important if="Dossier is unreachable">
Keep the completed record and page locally, and state in the handoff that publication is outstanding. Publish them when the next stage returns.
</important>

A restatement the user has not seen is not a confirmed goal. Publication alone does not establish that a page is current; its coverage must match the record.
