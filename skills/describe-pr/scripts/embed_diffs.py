#!/usr/bin/env python3
"""Write a branch's per-file diffs beside a PR walkthrough page.

For PAGE `pr-walkthrough.html`, the script writes `pr-walkthrough-diffs.json` in
the same folder, which the page loads by its URL. The file holds JSON
describing every file changed between the merge base of BASE and HEAD, and HEAD:

    {"base": "<sha>", "head": "<sha>", "pr": "<url or null>",
     "files": [{"path", "oldPath", "status", "additions", "deletions",
                "url", "diff", "hunks"}]}

`status` is added, deleted, renamed, or modified; `url` opens the file in the
pull request's Files changed view when --pr-url is given; `diff` is the file's
unified diff. `hunks` holds the same diff parsed into lines:

    [{"header": "@@ -1,3 +1,4 @@",
      "lines": [{"kind": "context|added|removed", "old": n, "new": n,
                 "id": "R2", "text": "..."}]}]

`id` is the line's address in GitHub's scheme: R<new line> for an added or
context line, L<old line> for a removed one. Appended to `url`, it opens that
line; with the head commit, it places a review comment on it.

The JSON encodes "<" as \\u003c. Re-running replaces the data file. If the
payload exceeds Dossier's 50 MiB limit, the script exits 1 and leaves the
previous file unchanged. Use --max-lines to shorten each file's diff.

Usage:
    embed_diffs.py PAGE [--repo DIR] [--base REF] [--head REF]
                        [--pr-url URL] [--max-lines N]
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

# The largest file Dossier publishes.
FILE_LIMIT = 50 * 1024 * 1024


def git(repo, *args):
    result = subprocess.run(
        ["git", "-C", repo, "-c", "core.quotePath=false", *args],
        capture_output=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(stderr or f"git {' '.join(args)} failed")
    return result.stdout.decode("utf-8", errors="replace")


def default_base(repo):
    try:
        ref = git(repo, "rev-parse", "--abbrev-ref", "origin/HEAD").strip()
        if ref and ref != "origin/HEAD":
            return ref
    except RuntimeError:
        pass
    for candidate in ("origin/main", "origin/master", "main", "master"):
        try:
            git(repo, "rev-parse", "--verify", "--quiet", candidate)
            return candidate
        except RuntimeError:
            continue
    sys.exit("embed_diffs: cannot find the base branch; pass --base")


def clean_path(raw, prefix):
    path = raw.rstrip("\r\n")
    if path.endswith("\t"):
        path = path[:-1]
    if len(path) >= 2 and path[0] == path[-1] == '"':
        path = path[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if path != "/dev/null" and path.startswith(prefix):
        path = path[len(prefix):]
    return path


def split_files(diff_text):
    blocks, current = [], None
    # Git ends each line with LF; splitlines() would also break at form feeds,
    # Unicode line separators, and carriage returns inside a line.
    for line in re.findall(r"[^\n]*\n|[^\n]+\Z", diff_text):
        if line.startswith("diff --git "):
            if current:
                blocks.append(current)
            current = [line]
        elif current is not None:
            current.append(line)
    if current:
        blocks.append(current)
    return blocks


HUNK_HEADER = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def parse_hunks(block):
    hunks, old, new = [], 0, 0
    for line in block[1:]:
        header = HUNK_HEADER.match(line)
        if header:
            old, new = int(header.group(1)), int(header.group(2))
            hunks.append({"header": line.rstrip("\r\n"), "lines": []})
            continue
        if not hunks or line.startswith("\\"):
            continue
        text = line.rstrip("\r\n")[1:]
        if line.startswith("+"):
            hunks[-1]["lines"].append(
                {"kind": "added", "old": None, "new": new, "id": f"R{new}", "text": text})
            new += 1
        elif line.startswith("-"):
            hunks[-1]["lines"].append(
                {"kind": "removed", "old": old, "new": None, "id": f"L{old}", "text": text})
            old += 1
        else:
            hunks[-1]["lines"].append(
                {"kind": "context", "old": old, "new": new, "id": f"R{new}", "text": text})
            old, new = old + 1, new + 1
    return hunks


def describe(block, max_lines, pr_url):
    status, path, old_path, minus, plus = "modified", None, None, None, None
    additions = deletions = 0
    in_hunks = False
    for line in block[1:]:
        if in_hunks:
            if line.startswith("+"):
                additions += 1
            elif line.startswith("-"):
                deletions += 1
            continue
        if line.startswith("@@"):
            in_hunks = True
        elif line.startswith("new file mode"):
            status = "added"
        elif line.startswith("deleted file mode"):
            status = "deleted"
        elif line.startswith("rename from "):
            status, old_path = "renamed", clean_path(line[len("rename from "):], "")
        elif line.startswith("rename to "):
            path = clean_path(line[len("rename to "):], "")
        elif line.startswith("--- "):
            minus = clean_path(line[4:], "a/")
        elif line.startswith("+++ "):
            plus = clean_path(line[4:], "b/")
    if path is None:
        if plus and plus != "/dev/null":
            path = plus
        elif minus and minus != "/dev/null":
            path = minus
        else:
            header = block[0].rstrip("\r\n")
            path = clean_path(header[header.rfind(" b/") + 1:], "b/")

    hunks = parse_hunks(block)
    lines = block
    if max_lines and len(block) > max_lines:
        kept = max_lines
        for hunk in hunks:
            if kept <= 0:
                hunk["lines"] = []
            elif len(hunk["lines"]) > kept:
                hunk["lines"] = hunk["lines"][:kept]
            kept -= len(hunk["lines"])
        hunks = [hunk for hunk in hunks if hunk["lines"]]
        lines = block[:max_lines] + [
            f"... {len(block) - max_lines} more lines not shown; see the file in the pull request\n"
        ]
    anchor = hashlib.sha256(path.encode("utf-8")).hexdigest()
    return {
        "path": path,
        "oldPath": old_path if old_path and old_path != path else None,
        "status": status,
        "additions": additions,
        "deletions": deletions,
        "url": f"{pr_url.rstrip('/')}/files#diff-{anchor}" if pr_url else None,
        "diff": "".join(lines),
        "hunks": hunks,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("page", type=Path,
                        help="walkthrough HTML page; the diffs file is written beside it")
    parser.add_argument("--repo", default=".", help="repository directory (default: .)")
    parser.add_argument("--base", help="base branch (default: the remote's default branch)")
    parser.add_argument("--head", default="HEAD", help="head revision (default: HEAD)")
    parser.add_argument("--pr-url", help="pull request URL, for Files changed links")
    parser.add_argument("--max-lines", type=int, default=0,
                        help="shorten any file's diff to N lines (default: no limit)")
    args = parser.parse_args()

    if not args.page.parent.is_dir():
        sys.exit(f"embed_diffs: no such folder: {args.page.parent}")
    out = args.page.with_name(f"{args.page.stem}-diffs.json")

    try:
        base = args.base or default_base(args.repo)
        head_sha = git(args.repo, "rev-parse", args.head).strip()
        base_sha = git(args.repo, "merge-base", base, args.head).strip()
        diff_text = git(args.repo, "diff", "--no-color", "--no-ext-diff", "--no-textconv",
                        "--src-prefix=a/", "--dst-prefix=b/", "--find-renames",
                        f"{base_sha}..{head_sha}")
    except RuntimeError as error:
        sys.exit(f"embed_diffs: {error}")

    files = [describe(block, args.max_lines, args.pr_url) for block in split_files(diff_text)]
    data = {"base": base_sha, "head": head_sha, "pr": args.pr_url, "files": files}
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    size = len(payload.encode("utf-8"))
    if size <= FILE_LIMIT:
        out.write_text(payload, encoding="utf-8")

    total_add = sum(f["additions"] for f in files)
    total_del = sum(f["deletions"] for f in files)
    print(f"embed_diffs: {len(files)} files, +{total_add} -{total_del}, "
          f"{base_sha[:7]}..{head_sha[:7]} -> {out}")
    for f in files:
        print(f"  {f['status']:<8} +{f['additions']:<5} -{f['deletions']:<5} {f['path']}")

    if size > FILE_LIMIT:
        sys.exit(f"embed_diffs: the diffs are {size / 2**20:.1f} MiB, past Dossier's 50 MiB file "
                 f"limit, so {out} was left unchanged; run again with --max-lines N to shorten "
                 f"long generated files")


if __name__ == "__main__":
    main()
