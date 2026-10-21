# Glossary

artifact-type: Project Glossary

A glossary interview settles the project's vocabulary from business sources: the terms people use, their meanings and contexts, the preferred name for each concept, and the relationships between concepts. It runs independently of a goal, and agreed terms become current project vocabulary. When defining a term requires a product or design decision, defer that question to the stage responsible for it.

## Inputs

Use business sources such as transcripts, notes, documents, email threads, or a requirements interview's ledger and the terms in its requirements document. Cite each source and keep quotations exact and attributed, within the ledger's confidentiality limits. Read [glossary guidance](glossary.md) before seeding the Language list: current terms in `glossary.json` are settled input, while goals' proposals provide context.

Collect each word or phrase used for a domain concept, with its source passages, as a candidate. Compare it with the glossary's names, avoided words, and meanings. Apply the glossary guidance to distinguish project vocabulary from general programming and design terms.

## Settle the clear ones, ask about the rest

Seed a candidate directly into the Language list when it names one clear concept, conflicts with no existing term or candidate, and has a consistent meaning across the sources. Add examples and relations where the sources support them. The page shows the term as new and open to comment; it is agreed unless the user comments. Ask only about candidates that require a decision.

Put on the frontier only what the user must decide:

- **Several words for one concept:** which one the project adopts; the others go under avoid.
- **One word for several concepts:** split it by context, or rename one meaning.
- **A clash with a current term:** determine whether the concept is changing, its name is changing, or the source uses it imprecisely.
- **Sources that disagree** on what a term means.
- **A context or relation** the sources leave unclear.
- **A candidate that may not belong,** such as a word that is general rather than the project's.

## Comparing options

For a choice between words, compare which one the business people use most and in which situations, which reads least ambiguously to someone new to the project, which the code and existing documents already use, and which keeps clear of other contexts' terms. Name the criterion that decides it. For a split, show the source sentences sorted under each meaning; the sentences usually make the case.

## Coverage

Account for every candidate with one outcome:

- a new term;
- merged into another term, with its word under that term's avoid;
- an existing term, confirmed or changed;
- rejected, with the reason, such as a general word or a duplicate;
- a deferred question naming the stage that decides it.

Beyond the candidates:

- Every context the sources reveal, with a description.
- Every term's definition says what the thing is and tells it apart from related terms.
- The relations the sources state or clearly imply, recorded on the terms they start from.
- An example for each term that could be confused with another.
- Every term traceable to the passages it came from.

## Completion

The interview is complete when all of these hold:

- The frontier and not-yet lists are empty.
- Every candidate and every coverage item is accounted for in the ledger.
- The user confirmed the final vocabulary in a review round of its own.
- A reader who scans the page can find any term and tell similar terms apart.

The user must have seen a new term on the page before leaving it uncommented can count as agreement.

## Ledger

Settled entries carry `phase=vocabulary` and one of these groups: `inputs` (cited sources), `contexts`, `naming` (a choice between words or a split). The Language list holds the terms, with their examples and relations.

Declare one list after Settled:

- **Candidates** (`CA-01`): each word or phrase, its source passages and speakers, and its outcome: `term=<Language ID>`, `merged=<Language ID>`, `existing=<glossary id>`, `rejected=<reason>`, or `deferred=<Deferred question ID>`. While a candidate is undecided, use `open=<question ID>`. Page rule: a compact index beneath the vocabulary showing what happened to each candidate.

## Page

These fill the brief's page placeholders. The visuals are starting points the builder may better; the page rules hold.

- **Settled title:** the project's vocabulary.
- **Settled visuals that fit:** terms grouped by context, each with its definition, example, words to avoid, and relations; a small map of how the terms relate; the candidate index.
- **Question visuals that fit:** for a choice between words, each word with the source sentences that use it and how often; for a split, the source sentences sorted under each meaning; for a clash, the current definition beside the sources' use.
- **Page rules:** show each term's source quotations, exact and attributed, within the ledger's confidentiality limits. Mark new terms as new and open to comment. Present the vocabulary the project will use as a coherent document.

## Handoff

Write new and changed terms to `glossary.json` following the glossary guidance for an interview without a goal. They become `current`, with merged names in `avoid`, any agreed examples and relations, and any new contexts added. Preserve the candidate index and source evidence in the frozen ledger so later stages can trace the vocabulary's origins.
