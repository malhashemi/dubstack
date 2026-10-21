# Setting up Dossier

Dossier hosts the project's pages and records: the home, interviews, goals, outlines, and reports that people and agents both work from. Most stages publish there, so a missing setup blocks them. Find the first missing step, guide the user through it, and continue to the next.

Run what you can with the user's agreement, such as installing the CLI. Signing in, accepting invitations, and anything in their own accounts are theirs to do; tell them exactly what to do and confirm the result afterwards.

## 1. The CLI

`dossier --version` shows whether it is installed. It needs Node.js 22.12 or newer:

```sh
npm i -g @agent964/dossier
```

## 2. Signed in to a deployment

`dossier whoami` shows the person and deployment the CLI acts for. To sign in:

```sh
dossier login <deployment>
```

It prints a link and a code and opens the link: the user checks that the code matches and presses Allow. A deployment is one running Dossier at its own address, such as `dossier.agent964.com`.

## 3. Somewhere to publish

`dossier ls` lists the user's workspace memberships, their trees and permissions, and shared targets. For an existing project, check for write access at its tree root; a share can grant this without workspace membership. Creating a new tree needs membership in its workspace.

- **An existing deployment.** Sign in and check for access first. If the deployment permits the user to create workspaces, they can create one in Settings and become its admin. Otherwise, ask a workspace admin for membership to create a new tree, or a writer on an existing project's tree to share it with write access.
- **Their own deployment.** Self-hosting runs Dossier on the user's Cloudflare account, following [Dossier's runbook](https://github.com/agent964dev/dossier/blob/main/docs/RUNBOOK.md#2-set-up-a-new-deployment-self-hosting). It needs a Cloudflare account on the Workers Paid plan, two domains (one for the deployment and a separate one that serves pages), and a Google or Microsoft Entra app for sign-in. After deploying, they sign in as its super admin, choose who may create workspaces, create one, and sign the CLI in to their own deployment. Offer to work through the runbook with them: the commands can run here, while accounts, domains, and the sign-in app are set up in their dashboards.

## 4. The project's tree

Continue the project's existing tree when it has one. Otherwise, the first stage that publishes creates it in the workspace and records it in the project's `AGENTS.md`; `project-home` is the usual first, since it builds the home every other stage expects.
