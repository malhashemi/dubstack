---
name: project-scaffolding
description: Start a basecamp goal that sets up a new project's whole stack ready for its first feature, or brings an existing codebase's checks and CI up to a proven standard. Only use when the user invokes this skill by name.
---

# Project Scaffolding

Scaffolding is a goal. In a new repository, the goal sets up the whole stack the architecture chose, connected end to end, so the first feature adds product behaviour to a working foundation. In an existing codebase, it brings the checks that guard the code up to the standard below and fixes the code until it passes them. This skill supplies the standard; basecamp owns intake and routing, and the goal's stages assess the scaffolding from the product's side, settle the remaining design decisions, and deliver the work.

The standard holds for any stack. The tools come from the project: in a new repository from its architecture, in an existing codebase from what the code already uses. Whatever neither settles is a decision for the user: recommend from their stack preferences, retrieved with the `stack-preferences` skill, never a default carried over from another project.

## Taking in the goal

A repository with no product code yet is new, even when some setup exists; one with product code is existing. Use the `basecamp` skill in this session to take in the goal, giving it the requirements for that situation and the shared standard below. Carry every applicable requirement and any user-approved exception into the goal's scope, because the stages that follow read the goal, not this skill. Preserve settled choices and their sources; record only unresolved facts and decisions as open, using basecamp's rules for what to ask now and what belongs to a later stage.

### A new repository

Set up the stack the architecture settles in `architecture/` in the project's tree: its toolchain, repository layout, building blocks, contracts, stores, and cross-cutting concerns. The result is a walking skeleton with no product behaviour:

- Every building block exists on its chosen technology. Start each app from its framework's own generator where one exists; otherwise follow its documented minimal setup. Preserve usable setup already present.
- Every store runs locally, with its schema and migration tooling in place. A store available only as a managed service follows the external-service decision below.
- Every contract between building blocks is wired the way the architecture chose.
- The cross-cutting concerns the architecture settles, such as configuration and secrets, logging, authentication, and translations, are in place for the first feature to use.
- Trivial end-to-end paths collectively exercise every building block, store, and contract included in the skeleton, with tests in the full check proving the connections. Use one path where the architecture permits it, and several for independent or asynchronous flows; preserve the chosen topology.
- One command starts the whole system locally.

Each external service that needs an account, such as an auth provider, payments, or email, is a decision for the user: wire it now with credentials they provide, in the vendor's test mode where one exists, or leave it to the first feature that uses it. Record each deferral and the affected startup paths and integration checks; a stand-in does not prove the deferred service works. The skeleton's startup and end-to-end proof cover the agreed integrations, and its handoff identifies what the first dependent feature must still set up. Whatever the architecture leaves unsettled is a decision for the user too, including the whole stack when there is no architecture, as for a small one-off app.

### An existing codebase

The code is the account of what is in place. `architecture/` only explains past decisions, since it was frozen when it was delivered. Fact to find: which checks exist, and which of them enforce, by running in CI and failing the build on a finding, rather than being advisory, vacuous, never installed, or allowed to fail.

Replacing a tool keeps the coverage the old one gave: each rule that still applies carries over, and any rule dropped is shown with its reason. Fix findings while preserving existing product behaviour and public contracts; a necessary change to either is a decision for the user. Instructions in the project's agent guidance that a check now enforces are proposed for removal.

### The standard for both

**Safeguards.** Account for each safeguard with its enforcing tool and setting, or the reason it does not apply. Omitting an applicable safeguard, relaxing a rule, or baselining an analyzer is a decision for the user, made per safeguard, rule, or tool, with the reason recorded. Fix findings under the agreed settings rather than silently exempting them.

- a pinned toolchain and reproducible installs;
- formatting;
- linting, with warnings treated as errors;
- the strictest type checking the stack practically allows;
- analysis of dead code, dependencies, duplication, and complexity, where the ecosystem has a tool for it;
- the repository's dependency rules, enforced as boundaries;
- a test runner with a first test through a public interface, and browser or device tests where the project wants them;
- secret scanning;
- automated dependency updates and vulnerability scanning;
- CI that runs the full check on every pull request.

Git or agent hooks are a decision for the user.

**Proof.** A passing check alone does not establish enforcement. Each check passes, fails on a deliberate violation of what it claims to enforce, and passes again once the violation is reverted. A setup failure does not count. Use disposable changes or fixtures, including synthetic scanner test data, and retain the commands and results as verification evidence. CI runs exactly the local full command and passes on the pull request's final commit.

**Discoverability.** The project itself shows how to verify a change. It has one full command, which CI runs, and a fast one where that helps, both defined in the project's manifest or task runner with names that say what they do. No command's name misleads, such as a `check` that rewrites files. The project's `AGENTS.md` gains a line only for what the code cannot show and an agent would get wrong, such as a test suite outside the full command that needs Docker or a simulator. Style rules stay out of it; the checks enforce them.

**Conduct.**

- Record each deliberate exception, such as a relaxed rule or an ignored path, with its reason beside the setting. When the format cannot hold comments, use a nearby note that identifies the exact setting.
- Exclude reference source, such as the `repos/` that `upstream-source` installs, and other vendored code from checks that treat it as application code. Preserve repository-wide security and policy coverage; any exception follows the safeguard decision rule above.
- Each tool is set up from its own documentation or its installed upstream reference, with its version resolved at setup and pinned exactly.
- Merge changes into existing configuration and agent instructions, preserving unrelated content and applying agreed removals.

**Out of scope.**

- Deployment and release: each is a goal of its own, following the architecture's deployment decisions.
- Changing the language, framework, or runtime: that is design work for `design-interview`, before a goal of its own.

## Completion

This skill's part is done when basecamp's intake is complete and the goal carries every applicable requirement, settled choice, approved exception, and unresolved question needed by later stages. Missing facts and decisions remain open for the stages that settle them. Intake completion does not establish that the scaffold or safeguards have been implemented or verified.
