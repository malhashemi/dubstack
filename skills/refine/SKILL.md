---
name: refine
description: Run a refinement session on a running app. The user reviews it and raises requests, questions, and design choices one at a time, and each is handled and tested locally until one pull request carries it all. Only use when the user invokes this skill by name.
---

# Refine

The user is reviewing the running app. They will raise requests and questions one at a time. Apply and test each fix locally as it arrives. When everything is addressed, the session ends with one pull request.

Before the first item, run the app locally where the user can open it, with mock data wherever a page needs something to show. Keep out of the pull request anything added only for the review.

<important if="an item comes through onlay">
Use the `onlay` skill to read and answer it.
</important>

## Design choices

When the user must pick between designs, show the options inline as HTML, using the `visualize-html` skill. Draw them in the app's design system, and include everything this session has already changed. Make each option selectable, with a notes field and a button that copies the choice so the user can paste it back. The copied text must make sense without the page.

## Completion

The session ends when the user says everything is addressed. Run the project's checks, then open the pull request with the `describe-pr` skill.
