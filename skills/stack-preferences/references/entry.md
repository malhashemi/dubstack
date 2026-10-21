# Entry fields

An entry describes one category. A patch holds only the fields that change; a new category needs `layer`, `title`, `choices`, `why`, `decided`, and `checked`.

| Field | Holds |
| --- | --- |
| `layer` | one of the layers `scope` lists |
| `title` | the category's name |
| `decides` | what the choice covers, in one line |
| `choices` | the preferred options in order, each `{"option": "...", "when": "..."}`; `when` is the condition it applies under, omitted when it always applies |
| `per_project` | `true` when there is no standing preference; `choices` then lists the candidates |
| `decided_by` | for a per-project category, what decides it |
| `avoid` | options not to use |
| `why` | why the first choice leads, in one line: the user's reason when they gave one, otherwise "user choice, no reason given" |
| `override_when` | what in a project's requirements would set the preference aside |
| `over` | contenders that lost, each "<option>: <why it lost>" |
| `revisit_when` | events that would reopen the preference, such as a beta reaching stable |
| `decided` | `YYYY-MM-DD` the choices were last decided; `apply` sets it when they change |
| `checked` | `YYYY-MM-DD` the preference was last reviewed against current sources; set it for a review, never for a decision edit |
| `history` | earlier choices with their reasons and dates; `apply` keeps it |

An entry records the user's decision and its reasons, not the research behind it: findings, summaries, and source citations go to the user, not into the entry.
