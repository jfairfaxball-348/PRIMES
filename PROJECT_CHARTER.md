# PRIMES Project Charter

## Root purpose

PRIMES exists to discover mathematically meaningful structure in the prime numbers that is not selected in advance from an existing famous problem or theorem.

The project is a long-horizon discovery and conjecture-synthesis programme. It combines exact computation, pattern search, adversarial falsification, mathematical interpretation, and disciplined prior-art checking.

Success means producing one or more durable mathematical contributions: a genuinely new conjecture with substantial evidence and mechanism, a new theorem, a new invariant or representation that reveals useful structure, a new counterexample, or a negative result that closes a plausible research direction.

## Separation of concerns

PRIMES owns:

- exact prime-data generation and provenance;
- derived representations and invariant definitions;
- computational experiments;
- observation and failure ledgers;
- conjecture generation;
- holdout and adversarial falsification;
- mechanism search;
- bounded prior-art collision audits;
- candidate lifecycle state;
- graduation packages for serious theorem projects.

A graduated theorem repository owns:

- the frozen theorem statement;
- proof development;
- formal verification where useful;
- manuscript preparation;
- journal/arXiv packaging;
- publication workflow.

## Discovery principle

The project must not choose a known open problem and merely search for a local improvement.

Candidate generation should begin from data, representations, transformations, anomalies, and structural questions. Existing theory may be used as a control and later as a collision test, but it should not silently determine what we are looking for.

This is not a claim that researchers can become historically ignorant. It is an operational firewall: literature-guided ideas are labelled as such, while blind-discovery experiments are generated from declared primitive objects and transforms.

## Prime universe

The base object is the ordered prime sequence

`2 = p_1 < p_2 < p_3 < ...`

together with structures derived exactly from it.

No single representation is privileged. Index space, value space, gaps, finite differences, residue words, interval occupancy, local configurations, graphs, symbolic encodings, and other exact transforms are all admissible if their definitions and provenance are recorded.

## Hard epistemic rules

1. Finite computation may refute a universal statement but never proves one.
2. A negative literature search is not evidence of novelty.
3. A visual pattern is not a conjecture until converted into an exact falsifiable statement.
4. A fitted curve is not a mechanism.
5. A statistically surprising feature is not automatically number theory.
6. Holdout data must not be used to generate the candidate it later tests.
7. A known theorem used as a control must be labelled as known.
8. Failed conjectures, duplicate discoveries, triviality explanations, and prior-art collisions remain in the permanent record.
9. Approximate numerical objects must never be silently substituted for exact arithmetic objects.
10. A candidate cannot graduate merely because it survived a large computation.

## Non-goals

PRIMES is not:

- a Riemann Hypothesis project;
- a prime-gap project by default;
- a catalogue of known prime facts;
- a benchmark for primality software;
- a machine-learning prediction competition;
- a proof repository for speculative claims;
- a publication factory;
- a system that equates obscurity with originality.

## Authority

The Git history of this repository is the authoritative PRIMES record. Conversation history, private notes, or unstaged experiments are not authoritative project state.

Material claims must be represented in committed records with enough provenance to reproduce how they arose.
