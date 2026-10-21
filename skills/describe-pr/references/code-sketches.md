# Code sketches

A **code sketch** is a short text view of one shape the change touches in the code: an interface, execution path, data shape, or allocation of responsibility. In a pull request, sketches make up the description's change outline and appear in the walkthrough wherever a shape explains more than the diff. Draw them from the diff, as the code landed, not as the plan described it.

## Choose a useful view

These are starting points. Combine or depart from them when another representation explains the decision better.

- **Logic or an algorithm:** pseudocode in plain words.
- **Runtime control flow:** a call tree of the calls that matter.
- **UI structure:** a component tree with the state, hooks, and module or package boundaries that matter, and file locations where they help.
- **File responsibility or a broad refactor:** a shallow file tree with a short note per entry.
- **Interaction or data flow across components:** a Mermaid sequence or flow diagram.
- **A contract across a seam:** its signature, or its endpoint and message shapes, with the invariants and error modes a caller must know.
- **Persisted data:** the schema in the project's own form (SQL, the ORM, or the schema library it uses).
- **Dependencies:** a dependency-injection map grouped by what receives them, saying what each dependency lets the code do.

Use the codebase's language and names so the reader can connect the sketch to the implementation, and tree glyphs (`├──`, `└──`, `│`) for trees. Keep existing identifiers exact and make proposed names recognizable as proposals.

## Diff or whole

Draw a `diff` when the shape exists and the point is what changes. Start added and changed lines with `+`, removed lines with `-`, and unchanged context with a space; in a file tree, a `~` note after a path marks a change inside that file. Keep only enough context to place the change:

```diff
 submitForm
   createSession
     persistPrompt
+    expandSkillMention
     launchAgent
   navigateToSession
+    subscribeToEvents
```

```diff
 src/
 ├── commands/
+│   └── show-me.ts       # expands the slash command
 ├── sessions/
-└── transport.ts
+└── transport/
+    ├── client.ts
+    └── stream.ts
```

Show the target shape when most of it is new, omitted context would hide ownership or order, or the implementer needs an exact contract. For example, a small function can express a proposed transformation directly:

```ts
function expandSkill(command: string): string {
  const skillName = command.slice(1)
  return `use the ${skillName} skill`
}
```

## Keep it small

Keep only the calls, files, fields, components, states, and boundaries the decision at hand needs. One sketch shows one shape; a decision usually needs one or two, and a sketch that helps no decision stays out. Say what a sketch simplifies or leaves out, so readers know how literally to take it.
