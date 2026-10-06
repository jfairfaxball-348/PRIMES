# Prior-Art and Novelty Protocol

## Purpose

Prime-number research has centuries of prior art and many equivalent terminologies. PRIMES therefore treats novelty checking as a dedicated research stage.

A negative search never proves novelty.

## Collision ladder

For each candidate, search progressively.

### 1. Exact-language search

Search the literal objects, formulae, and property names used in the candidate.

### 2. Synonym search

Replace project terminology with standard mathematical language. Search alternative names for the same sequence, transform, graph, statistic, or extremal property.

### 3. Equivalent-form search

Derive equivalent statements and contrapositive/extremal forms. A candidate may be known in a representation completely different from the one that discovered it.

### 4. Stronger-theorem search

Ask whether a general theorem makes the candidate immediate even if the exact statement is absent.

### 5. Sequence/data collision

Search distinctive integer sequences or finite signatures in sequence databases and computational tables.

### 6. Citation-chain search

When a near match is found, inspect its references and later citations. The relevant result may predate the terminology used in the candidate.

### 7. Expert-language translation

Write a short neutral description of the candidate suitable for a specialist. If the candidate remains serious, external expert review is required before strong novelty claims.

## Search record

Each audit records:

- candidate ID and exact version;
- date;
- databases/search engines used;
- queries;
- papers/results inspected;
- closest overlaps;
- whether the overlap is exact, stronger, weaker, or merely adjacent;
- unresolved terminology;
- conclusion and uncertainty.

## Allowed conclusions

Use one of:

- **KNOWN_EQUIVALENT**
- **KNOWN_IMPLIED**
- **POSSIBLE_OVERLAP**
- **SEARCHED_NO_COLLISION_FOUND**
- **NOVELTY_REQUIRES_EXPERT_REVIEW**

Do not use **NOVEL** as an internal status.

## White space

"White space" means a region where a candidate appears mathematically coherent, nontrivial, and not yet collided with checked prior art.

It is a research hypothesis, not a fact about the literature.
