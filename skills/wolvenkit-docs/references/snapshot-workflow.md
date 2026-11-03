# Private WolvenKit documentation snapshots

The authoritative documentation source is
[CDPR-Modding-Documentation/WolvenKit-8-Wiki](https://github.com/CDPR-Modding-Documentation/WolvenKit-8-Wiki),
which backs the [official WolvenKit documentation](https://wiki.redmodding.org/wolvenkit).
This is documentation acquisition, not installation of the WolvenKit application.

Keep fetched upstream text in the user's private data directory, outside this
distributable skill repository. The source repository had no explicit documentation
license at the initial 2026-11-02 acquisition; do not infer one from WolvenKit's
application license or publish the copied text with these original instructions.
Retain any upstream license/notice encountered on future acquisitions.

## Layout and lookup

The default root is `${XDG_DATA_HOME:-$HOME/.local/share}/codex-docs/wolvenkit`;
`WOLVENKIT_DOCS_ROOT` may point to another existing private root.

```text
current.json                       # selected relative snapshot path and revision
snapshots/<immutable-revision>/
  manifest.json                    # source/date/coverage, paths, URLs, hashes
  INDEX.md                         # searchable titles, paths and original URLs
  pages/<upstream-relative-path>    # unchanged upstream Markdown
```

Read the manifest before searching. It must distinguish source commit date from
acquisition date, list errors and identify excluded media/external resources.
The page entries bind relative path and original source URL to size and SHA256.
Verify a selected page's hash before trusting it; the absence of media means a
text page that depends on an image may require viewing that image at its source.
An upstream GitBook include or external link is not locally present unless the
manifest actually contains it. Preserve that gap in the answer.

The repository commit fixes text identity; it does not establish compatibility
with a particular game/tool release. Pages may describe old versions even in a
freshly acquired snapshot. Read their version notes rather than using the fetch
date as a version guarantee.

## Acquire or refresh

Reuse a matching verified cache. When acquisition is needed, use the available
GitHub connector or ordinary HTTPS/Git tooling; no new MCP server is required.

1. Resolve the documentation repository's requested ref to a full immutable
   commit. Record the source URL, commit and acquisition time before fetching.
2. Enumerate the full tree and require a non-truncated listing. Select Markdown
   and any license/notice text. Fetch only those blobs from the pinned commit;
   exclude images, archives, binaries, executable scripts and application source.
3. Write into a fresh private staging directory, preserving safe relative paths
   and original bytes. Refuse absolute/traversing paths, symlinks, HTML error pages
   masquerading as Markdown, and incomplete/mismatched blob responses. A download
   failure is a recorded acquisition failure, not a zero-page success.
4. Build the manifest and index with source URLs, dates, exclusions and content
   hashes. Verify every selected file and the complete expected path set. Search
   and read representative CLI, import/export and rig/animation pages; record
   missing topics rather than claiming the whole modding ecosystem is covered.
5. Promote the completed snapshot without overwriting a prior revision. Change
   `current.json` only after verification; preserve its previous contents. If the
   snapshot already exists, compare it and reuse only an exact match. A failed
   refresh leaves the old selection usable.

The existing general skill also ships
`scripts/setup/library/tools/sync-docs.py --sections wolvenkit` for a private
setup library. That is a website snapshot with retrieval dates/hashes, not a
Git-commit snapshot. Its `verify-docs.py`, index and search tools can validate and
query an already established setup library. Do not silently mix that layout,
source identity or coverage with this snapshot's manifest, or run provisioning
that installs unrelated tools just to read documentation.

## Evidence boundaries

Report acquired page count, revision/date, hash verification, representative
lookup results and gaps. Discovery of this skill proves its availability;
reading a page proves that documentation was consulted. Neither proves the
documented command ran, an asset round-tripped, or the game behaved correctly.
