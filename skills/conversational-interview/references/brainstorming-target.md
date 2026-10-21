# Brainstorming

Explore a problem or opportunity with the people who care about it: develop possibilities, make the promising ones concrete, and find useful directions and the questions still open. A brainstorm can finish with possibilities open; a chosen solution, approved requirements, or a goal is not required.

## Where it lives

Like requirements gathering, a brainstorm sits above goals: what it finds can start work, but it is not a stage of a goal. Its folder is `<slug>-interview/` at the root of the project's local copy, with a short name for the subject as its slug. It is team material: published for the owner's team like any interview folder. When people from outside the team take part, the owner decides what they may see.

## Who decides

Ideas belong to the people who bring them. The person who started the brainstorm decides what it is for, what counts as promising, and whether anything is chosen. You contribute as a partner, and your ideas are recorded as yours. Nothing becomes a direction because you favoured it.

## Start from what is known

Read what is already known about the problem: what the user wrote, documents and research they point to, the project, earlier sessions. Open from it, in the user's own framing of the problem, rather than asking them to restate it.

## How the exploration moves

These are judgments, not steps. Use whichever the moment calls for.

- **Open up before judging.** Let possibilities accumulate before weighing them. Early praise or criticism steers people toward or away from ideas before the field is wide, and so does leading with your own idea before theirs. When you contribute, offer ideas that widen the field rather than refine the first one.
- **Examine the framing.** When a proposed solution is hiding the problem, the question is so narrow it allows only one answer, or a constraint seems inherited rather than real, step back: what is the underlying need, what would success look like, and which constraints actually hold?
- **Test what an idea rests on.** When an idea, or the whole discussion, depends on a premise nobody has examined, ask what happens if it does not hold.
- **Bring another perspective.** When one viewpoint dominates, ask how someone else would see it: the person most affected, the newest user, a competitor, whoever pays when it goes wrong. An imagined perspective raises questions; it never stands in for what real people want.
- **Make an idea concrete without choosing it.** Give a promising but vague idea a who, what happens, why it would matter, and its sharpest open question, or a sketch or a worked example. Making it concrete gives the conversation something to examine; exploration can continue afterwards.
- **Return to earlier ideas,** including the odd ones, and look for combinations. Summaries that only cover the latest thread lose the field.
- **Change the angle when it stalls.** When contributions repeat or energy thins, try a constraint, an analogy, a concrete scenario, a perspective, or a picture, rather than asking for more of the same.
- **Recognise readiness to evaluate.** When the user asks which is best, when ideas start converging, or when energy for new ones is spent, move to weighing them: on criteria the user names, across the whole field rather than the most recent ideas. Do not manufacture critique where nothing important is weak.
- **Turn gaps into questions.** When an idea needs a fact or a decision nobody in the conversation holds, record the question rather than inventing an answer.

You may offer a visual to think with, such as a map of the ideas so far or a quick sketch of a concept, whenever it would help the conversation; make it while the conversation continues. A quick lookup the user asks for can happen in the moment; anything longer waits until after the session, with reconciling and composing.

## The record

The ledger holds the brainstorm as lists, current rather than cumulative, with stable IDs that are retired and added, never renumbered or reused. Every entry records who contributed it (`by`), whether it came from a participant or from you (`origin`), and where (`evidence`: the session and time, or the round).

- **Header:** `target` (brainstorming), `subject` (the problem or opportunity in the user's words), `state` (exploring, weighing, or finished), the participants, and the `confidentiality` line.
- **Framings** (`F-01`): the ways the problem has been stated, which one is current, and why it changed.
- **Ideas** (`I-01`): each idea in its contributor's words; what it builds on; its status (raw, developed, promising, set aside, or chosen); and, once developed, its concrete form: who it serves, what happens, why it matters, and its open question.
- **Directions** (`DR-01`): what a group of ideas points toward, the ideas it gathers, and what makes it promising, in whose judgment.
- **Criteria** (`CR-01`): what the user wants options weighed on, once weighing starts.
- **Assumptions** (`A-01`): premises surfaced, whether they were tested, and what follows if one is false.
- **Questions** (`Q-01`): what is still open, and who or what could answer it.
- **Delta:** the IDs that changed since the previous reconciliation, each with a one-line reason.

Keep contributions in the words they arrived in. When you reword an idea while developing it, keep the original beside it; a rewording that changes the meaning is a new idea.

## What it produces

After the session, reconcile it into the ledger, then compose a summary page for the people who took part, `index.html` in the interview's folder, with the ledger as its agent version. It shows the framing, the ideas grouped by what they share, the directions with why they are promising, ideas set aside but worth remembering, the open questions, and possible next moves. Its readers may comment on it; fold their comments in as contributions and resolve the threads you folded.

## Completion

The brainstorm is complete when the user says it has served its purpose and:

- every contribution is in the record, in its contributor's words;
- each direction says why it is promising, and set-aside ideas worth keeping are recorded;
- the open questions are recorded, with who or what could answer each;
- the user has seen the summary and confirmed it says what they meant.

It can end with possibilities still open. When the user does choose, record the choice with who chose and why.

## Handoff

Leave the project's glossary unchanged; terms that came up stay in the record. Report where everything is and the possible next moves, such as a requirements interview, research, or a design interview; when the user picks one, end with a ready-to-use message that starts it, shown in a Markdown code block so it can be copied whole.
