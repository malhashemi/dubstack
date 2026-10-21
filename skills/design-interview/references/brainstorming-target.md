# Brainstorming

artifact-type: Brainstorm

Explore a problem or opportunity with the people who care about it: develop possibilities, make the promising ones concrete, and find useful directions and the questions still open. A brainstorm can finish with possibilities open; a chosen solution, approved requirements, or a goal is not required.

## Where it lives

Like requirements gathering, a brainstorm sits above goals: what it finds can start work, but it is not a stage of a goal. Its folder is `<slug>-interview/` at the root of the project's local copy, with a short name for the subject as its slug. It is team material, published for the owner's team like any interview folder. When people from outside the team take part, the owner decides what they may see.

## Who decides

Ideas belong to the people who bring them. The user decides what the brainstorm is for, what counts as promising, and whether anything is chosen. You contribute as a partner, and your ideas are recorded as yours. Nothing becomes a direction because you favoured it, and a strong recommendation is not a choice.

## Start from what is known

Read what is already known about the problem: what the user wrote, documents and research they point to, the project, earlier rounds and sessions. Show it in the user's own framing of the problem rather than asking them to restate it.

## Kinds of questions

- **Prompts that open the field:** an open question, a provocation, a constraint, an analogy, or another person's perspective, each with a visual to think with. They invite the user's ideas and carry no recommendation.
- **A promising idea made concrete:** who it serves, what happens, why it would matter, and its sharpest open question, drawn so the user can react to it and develop it. Making an idea concrete is not choosing it.
- **Framing questions,** when a proposed solution is hiding the problem, the question allows only one answer, or a constraint seems inherited rather than real: what is the underlying need, what would success look like, and which constraints actually hold?
- **Weighing questions,** only once the user is ready: ideas compared on criteria the user names, across the whole field rather than the most recent ideas. Recommend only when the user asks for one.

## How the exploration moves

These are judgments, not steps. Use whichever the round calls for.

- **Open up before judging.** Let possibilities accumulate before weighing them. Early praise or criticism steers people before the field is wide, and so does leading with your own idea before theirs. When you contribute, offer ideas that widen the field rather than refine the first one.
- **Test what an idea rests on.** When an idea, or the whole discussion, depends on a premise nobody has examined, ask what happens if it does not hold.
- **Bring another perspective** when one viewpoint dominates: the person most affected, the newest user, a competitor, whoever pays when it goes wrong. An imagined perspective raises questions; it never stands in for what real people want.
- **Return to earlier ideas,** including the odd ones, and look for combinations.
- **Change the angle when it stalls.** When answers repeat or thin out, try a constraint, an analogy, a concrete scenario, or a picture, rather than asking for more of the same.
- **Recognise readiness to evaluate:** the user asks which is best, ideas start converging, or energy for new ones is spent. Do not manufacture critique where nothing important is weak.
- **Turn gaps into questions.** When an idea needs a fact or a decision nobody in the interview holds, record the question rather than inventing an answer.

Size each round to keep the exploration moving: a round that widens the field, a round that develops what looked promising, a round that weighs, as the user is ready. When a round would go better talked through, the interview can continue in `conversational-interview`.

## Completion

The brainstorm is complete when the user says it has served its purpose and:

- every contribution is in the record, in its contributor's words;
- each direction says why it is promising, and set-aside ideas worth keeping are recorded;
- the open questions are recorded, with who or what could answer each;
- the user has read the page and confirmed it says what they meant.

It can end with possibilities still open; an empty frontier is not required. When the user does choose, record the choice with who chose and why.

## Ledger

The ledger holds the brainstorm as lists, in place of Settled, current rather than cumulative, with stable IDs that are retired and added, never renumbered or reused. Every entry records who contributed it (`by`), whether it came from a participant or from you (`origin`), and where (`evidence`: the round, or the session and time).

- **Header:** `target` (brainstorming), `subject` (the problem or opportunity in the user's words), `state` (exploring, weighing, or finished), the participants, and the `confidentiality` line.
- **Framings** (`F-01`): the ways the problem has been stated, which one is current, and why it changed.
- **Ideas** (`I-01`): each idea in its contributor's words; what it builds on; its status (raw, developed, promising, set aside, or chosen); and, once developed, its concrete form: who it serves, what happens, why it matters, and its open question.
- **Directions** (`DR-01`): what a group of ideas points toward, the ideas it gathers, and what makes it promising, in whose judgment.
- **Criteria** (`CR-01`): what the user wants options weighed on, once weighing starts.
- **Assumptions** (`A-01`): premises surfaced, whether they were tested, and what follows if one is false.
- **Questions** (`Q-01`): what is still open, and who or what could answer it.
- **Delta:** the IDs that changed since the previous round, each with a one-line reason.

Keep contributions in the words they arrived in. When you reword an idea while developing it, keep the original beside it; a rewording that changes the meaning is a new idea. The skill's round header fields, Frontier, and Not yet sit beside these lists; a frontier prompt about an idea names it with `about=<ID>`.

## Page

These fill the brief's page placeholders. The visuals are starting points the builder may better; the page rules hold.

- **Settled title:** the problem as framed, and the space explored so far.
- **Settled visuals that fit:** a map of the ideas, clustered by what they share; promising ideas drawn concretely, as a storyboard, a sketch, or a worked example; directions with the ideas they gather.
- **Question visuals that fit:** a provocation or a constraint drawn as a scene; another person's view of the problem; for weighing, the ideas laid out against the user's criteria.
- **Page rules:** ideas appear in their contributors' words, and your contributions are marked as yours. No idea is shown as the winner until the user chooses. Set-aside ideas stay visible, small. Open questions sit beside the ideas they hold back.

## Handoff

Leave the project's glossary unchanged; terms that came up stay in the record. Report where everything is and the possible next moves, such as a requirements interview, research, or another design interview; when the user picks one, end with a ready-to-use message that starts it, shown in a Markdown code block so it can be copied whole.
