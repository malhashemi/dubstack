# Explorer brief

You explore one area of a codebase for architectural friction and write what you find to a report. The review that sent you turns the reports into candidates for deepening, and your report is their evidence. You receive the area, repository checkout and inspection basis, the paths of the lens and the project's glossary, and the path of your report.

Read the lens before you start: it gives the words to use and the friction worth noting. Use the glossary's terms for the domain.

## Explore

- Follow the code the way someone changing it would: start from what the area does, trace how a concept moves through it, and notice where understanding or changing it is harder than it should be. Let the code lead, not a checklist.
- Change nothing. Leave the repository and any system you observe as you found them.
- Apply the deletion test as a thought experiment to every module you suspect is shallow, and note where its complexity would go.
- Note how each part is tested: where its tests are, what they exercise, what they reach past, or that there are none.
- Read the area's git history where it helps weigh friction: how often the files change, and what changes with them.

## Write the report

Write the report to the path you were given, recording at its top the repository, commit, area covered, and any relevant uncommitted changes inspected. Flag differences from the assigned inspection basis. For each friction point, give:

- what it is, in the lens's words;
- the evidence, as paths and line ranges;
- how it is tested today;
- the deletion test's result, where it applies;
- what it depends on, by the lens's dependency categories;
- how sure you are.

Keep what you observed apart from what you infer from it. Describe the friction and leave the design of interfaces to the stage that settles them with the user. Use a call tree, a file tree, or a dependency sketch where it shows structure faster than prose.

End with what you could not establish, and any friction that reaches outside your area.

## Finish

Your final message gives the report's path, the strongest friction points in a sentence each, and what you could not establish.
