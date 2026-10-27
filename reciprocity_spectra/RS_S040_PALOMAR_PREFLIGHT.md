# RS-S040 — Palomar Registry submission preflight (2026-10-27)

**Scope:** policy/schema/path audit only; no external submission or consent. The committed
preflight baseline is public PRIMES `main` at `ff6ef1742582a9acddefe4ab56203b16c30d4ed4` (the honest owner-reviewed
AI-disclosure merge). Submission must pin the **final merged** 40-character commit, not this
intermediate baseline. No change was made to the 26 selected theorems or source proofs.

## Binding external sources checked

- PalomarRegistry/PalomarPolicy, live submitter policy:
  https://github.com/PalomarRegistry/PalomarPolicy/blob/main/CONTRIBUTING.md
  (especially §§1–4 and 6.1–6.2).
- Palomar how to submit: https://palomar-registry.org/how-to-submit
- PalomarSubmission taxonomy snapshots:
  https://github.com/PalomarRegistry/PalomarSubmission/tree/main/taxonomies

## Repository-relative submission inputs

| Form input | Exact value |
|---|---|
| Repository | `jfairfaxball-348/PRIMES` |
| Revision | Final merged **full 40-character commit SHA**; never branch name |
| Selected Lean project path | `formalisation` |
| Comparator configuration path | `formalisation/comparator.json` |
| Metadata path (default inside selected project) | `formalisation/formalization.yaml` |
| Challenge module | `Challenge` (resolves to `formalisation/Challenge.lean`) |
| Solution module | `Solution` (resolves to `formalisation/Solution.lean`) |
| Repository licence | `LICENSE`, Apache-2.0 (root, not under `formalisation/`) |

The Palomar form supports project directories inside the repository. Its Comparator and
metadata paths are repository-root relative, even for a nested project; the project directory
is **not** `.`. Use the exact pinned immutable revision ultimately submitted.

## Preflight findings (baseline `ff6ef1742582a9acddefe4ab56203b16c30d4ed4`)

| Check | Result |
|---|---|
| Public repository, SHA, nested project layout | **PASS**; root licence and nested `lean-toolchain`, `lakefile.toml`, committed `lake-manifest.json` are present |
| Selected declarations | **PASS**; 26 unique `theorem_names` all exist in independently stated Challenge; no compared `definition_names` |
| Comparator JSON schema | **PASS**; only supported keys, distinct `Challenge` / `Solution` modules, permitted axioms `propext`, `Quot.sound`, `Classical.choice`; NanoDa enabled |
| Challenge size | **PASS WITH AUDIT WARNING**; 20,253 bytes and 515 lines, below hard limits 100 KiB and 1,000 lines, above advisory 300-line warning threshold |
| Project snapshot size | **PASS**; Git tree contains 10,456,370 bytes of tracked blobs, far below 500 MiB hard ceiling (without Git metadata or checkout overhead) |
| Untrusted repository artefacts | **PASS on Git tree audit**; no committed compiled-artifact suffixes, submodules or symlink entries; full registry intake retains independent authority for source scan |
| Lean/Mathlib dependency pins | **PASS**; Lean v4.35.0 and Mathlib `56a005855ea17e0b0958f73ec801ae140b0a1679`, with matching manifest; all Git dependencies have public GitHub HTTPS URLs and full 40-character SHA pins |
| Metadata required shape | **PASS on manual schema inspection**; `version: v0.4`, project name/description, human author/maintainer, Apache-2.0, nonempty source relationship, classification, automation and self-assessed review |
| Controlled taxonomy | **PASS**; `math.NT`, `11A15`, `11L05` present in current PalomarSubmission taxonomy lists |
| AI disclosure | **PASS**; `automation.methods` uses `method: agent` and names `OpenAI ChatGPT` as materially involved; untracked underlying model versions not invented |
| Informal account | **SUPPLEMENTED** with a reader's guide for all 26 selected declarations at the top of `formalisation/README.md`; exact Lean types/hypotheses take precedence |
| Prior independent 26-theorem kernel verification | **PASS** at `98c8f54d` (Comparator/NanoDa 40566801477; cloud 40566801479); reverified at the AI-disclosure baseline `ff6ef1742582a9acddefe4ab56203b16c30d4ed4` (Comparator/NanoDa 40569785577; scoped cloud 40569785692) |

The Challenge has 26 `by sorry` placeholders **only as independent statements**. They are not
proofs or admitted lemmas. The Solution and original proved library have no `sorry`; the
independent Comparator/NanoDa checks, not this textual scan, establish verification.
A normal repository-wide CI Ruff failure on frozen, unrelated D1 files does not replace
or invalidate successful scoped Lean and Comparator workflows; keep that distinction explicit.

## Disposition and remaining gates

**Technical preflight: submission-ready for an author-initiated intake**, subject to both
independent workflows passing on the **final submitted SHA** after the documentation merge.
The advisory 515-line Challenge warning is real but not a hard rejection. Palomar's separate
editorial research-interest standard (§1) requires a potentially paper-worthy result with a
credible mathematical audience; 26 verified supporting finite identities do **not** automatically
satisfy it, and editorial acceptance cannot be promised. The reader's guide does not claim
asymptotics, novelty, review or registration. Formalization metadata's source-based relationship
to the in-repo exact-identity inventory remains declared, not a claim of priority.

**External action remains owner-controlled:** begin a separate RS-S041 session only at the
author's request. At https://submit.palomar-registry.org/ enter the full final commit and the
project/configuration paths above, then use the Palomar GitHub sign-in to establish repository
write access and indicate the true author/maintainer authorisation basis. The status-page URL
must be retained; Palomar does not email it. Editorial review and explicit registration consent
are distinct from local mechanical success. Do not create a Palomar ID, assert registration,
or submit merely because RS-S040 completed.

**Unchanged boundaries:** CAND-002(1)–(3) remain unproved; RS-S040 did not start D1, edit the
original finite proofs, run new experiments, draft a paper, or perform a novelty audit.
