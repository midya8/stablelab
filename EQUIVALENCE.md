# StableLab safe replacement / 0.2.0

Same stable models is not a safe module replacement criterion. This extension enumerates the complete set of SE interpretations, not a list of sample contexts, and constructs an actual normal-rule context when the sets differ.

## Input and claim boundary

Comparison input has exactly `atoms`, `left`, `right`. Both rule lists use the existing normal-rule schema: exact `id`, `head`, `positive`, `negative`; a null head is a constraint. At most five sorted unique atoms and 24 rules per side. Body lists are sorted unique declared atoms. Rule IDs are unique within each side, but the two sides may reuse an ID. Positive and default-negative bodies may overlap. Empty vocabularies and rule lists are accepted. The base single-program limit remains eight atoms / 32 rules.

The comparison checks every `X ⊆ Y` over this declared vocabulary: `3**n` pairs, including all diagonals. A pair belongs to `SE(P)` exactly when Y is a classical model of P and X satisfies the Gelfond-Lifschitz reduct `P^Y`. The exported original-rule and reduct-rule obligations state which body literals are missing/present and whether each head is present.

The strong-equivalence verdict concerns addition of **any finite normal-rule context over the same vocabulary**, including constraints. It is a semantic characterization of that class, not a finite sample of contexts. The UI accepts neither contexts with fresh atoms nor disjunction, aggregates, variables, classical negation, choice rules, nested negation, or external calls. No claim about program-update semantics, temporal replacement policies, scalability, new theory, or arbitrary ASP syntax is made.

## Deterministic witness

Pairs are ordered by Y bitmask then X bitmask, both ascending. The first SE-set difference is selected. Let the pair be in the inside program's SE set but not the outside program's.

1. If Y is not a model of the outside program, add one fact for each atom of Y. Y is stable in the inside augmented program and not even a model on the outside. This also handles a proper differing pair whose Y diagonal differs; it is not limited to diagonal witnesses.
2. Otherwise both sides model Y, but X satisfies the inside reduct and not the outside reduct. Add facts X and a directed positive cycle over `D = Y \ X`. If D has one atom, add no cycle rule. Every proper subset of Y satisfying this context must be X: facts force X; a cycle propagates any D atom through all of D. Thus below Y the context has exactly the models X and Y. Y is stable only in the outside augmented program.

This is a small implementation specialization of the published all-pairs-edge gadget, not a new theorem. The exact two-submodel property is also checked for every generated witness, independently of stable-family comparison. No cycle edges are omitted unless the strongly connected cycle still has this property. At most five facts/cycle edges are added, so each augmented side has at most 29 rules, below the base 32-rule limit. Context IDs use the first unoccupied `ctxN`, considering both modules.

The report includes the context, its models below Y, the distinguishing interpretation, and **complete base evidence for both augmented programs**, not just a claimed winner.

## Independent check and shared dependencies

`stablelab/equivalence.py` generates pairs using direct original/reduct satisfaction. It uses the existing base closure engine only to generate full augmented evidence. `stablelab/equivalence_oracle.py` does not import either generator: it reconstructs pairs through three-valued Godel conjunction and implication with values 0 (outside Y), 1 (in Y minus X), 2 (in X). Default negation is 2 only at 0. A rule is accepted at value 2. Context stable families are independently enumerated by proper-subset reduct models, with no least-closure call.

The strict request parser and atom/rule schema parser are shared. The existing independent base verifier checks the embedded augmented evidence. These are disclosed shared dependencies, not additional independent solvers. The browser JS generator mirrors the direct generator; matching JS/Python output is portability evidence, not independent semantic confirmation. Exact canonical JSON comparison rejects extra/missing fields and booleans disguised as numbers.

## Reproduce

```sh
python -m pip install .
python -m stablelab compare comparison.json > proof.json
python -m stablelab verify-comparison proof.json
# The installed console command supports the same two commands.
python -m unittest discover -s tests -v
node --test tests/test_*.mjs tests/test_*.cjs
bash tools/check_wheel.sh
# Optional external solver cross-check (never a runtime dependency)
python -m pip install clingo==5.8.3
python tools/check_equivalence_clingo.py
```

`make_equivalence_controls.py` deterministically regenerates the eleven comparison controls. The base controls and public inspector remain available. The comparison controls include agreement on both classical and stable families but different SE sets, a real cycle context, positive-cycle activation, safe transitive-edge removal, redundant rules, contextual inconsistency, empty vocabulary and all 243 five-atom pairs.

Tests exhaust all ordered pairs among the empty program and every one-rule two-atom normal program: 49² = 2,401 comparisons. There are also 180 seeded three-atom comparisons, field-by-field evidence corruption, identifier collisions, strict grammar/bounds, JS/Python complete-report parity and actual Chrome rule/pair rendering checks at desktop and two phone widths. These finite tests do not constitute proof for unbounded inputs; the implementation claim stays within the stated finite syntax.
