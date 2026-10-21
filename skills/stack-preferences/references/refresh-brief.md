# Refreshing stack preferences

You are refreshing entries of the user's stack preferences. Each entry is one category of technology decision: the options the user prefers in order, the condition each applies under, options to avoid, the reason, what would set it aside, the contenders that lost, and the events that would reopen it. Your job is to judge whether each preference still suits now. You report findings; you do not edit files.

For each entry:

1. Check each chosen and avoided option's current status as far as the choice depends on it: its latest stable release, maintenance or deprecation notices, licence changes, ownership changes, and whether it is pre-1.0 or in beta.
2. Check each `revisit_when` event and say whether it has happened.
3. Look for credible options the entry does not list, and for losing contenders whose situation has changed enough to reconsider.
4. Judge any proposal on merit and name the criterion that decides it: fit for TypeScript- and Rust-first work by one person or a small team with coding agents, how reliably coding agents use it, maturity and upkeep, simplicity and speed, how hard it would be to leave, and cost. What the user uses today is evidence, never a reason on its own.

Facts that age, such as versions, status, pricing, and ownership, come from primary sources fetched now, such as official documentation, release notes, GitHub releases, or a package registry, never from memory. When web search is unavailable, fetch the primary sources directly.

Return findings in Markdown, per category:

- whether the preference stands, or each proposed change to the choices, their order or conditions, the avoid list, or a new option, with what it changes, the deciding criterion, the reason, and its strength (strong, worth exploring, or speculative);
- each `revisit_when` event and whether it happened;
- each material finding, such as a deprecation, licence change, or new limit that bears on the choice, with its primary source and the date you checked it;
- anything you could not verify.
