# StableLab

**Supported. Minimal. Still not stable.**

A dependency-free finite normal logic-program workbench for answer-set semantics.
Inspect every candidate, every Gelfond-Lifschitz reduct, synchronous derivation
round, rule violation, support and nonempty unfounded subset. A separate checker
uses complete reduct model tables instead of the generator's closure algorithm.

## Contrasts that separate the claims

- `p <- not p; p <- q; q <- p` has exactly one classical model, `{p,q}`. It is
  supported and minimal, but not stable: its reduct has only a positive cycle and
  derives nothing. Minimal supported does not imply stable.
- `p <- q; q <- p` has empty and full supported models; only empty is stable.
- `p <- not q; q <- not p` has two stable alternatives. An odd self-default cycle
  instead has none. Absence of stable models gives null brave/skeptical answers,
  not an assertion from vacuity.
- A constraint filters one even-cycle alternative. A fact seeds a positive cycle
  and four derivation layers. An exception defeats a default conclusion.
- Empty program has one empty stable model. An empty-body constraint has no model.
- Four independent even cycles yield 16 stable models among 256 candidates.

Ten developed synthetic controls use 300 candidate interpretations in total.
They illustrate established semantics, not empirical agent behavior.

## Run

Python 3.10+, no runtime dependencies. Node 22+ and Chrome for browser checks.

```sh
python -m pip install .
python -m stablelab analyze docs/example.json > evidence.json
python -m stablelab verify evidence.json
stablelab verify evidence.json
python -m unittest discover -s tests -v
node --test tests/test_*.mjs tests/test_browser.cjs
bash tools/check_wheel.sh
python -m http.server --directory docs 8000
```

Open `http://localhost:8000` for editable models and complete evidence export.
The page computes locally after its static assets load. No model or API is used.

Optional external solver comparison, separate from runtime installation:

```sh
python -m pip install 'clingo==5.8.3'
PYTHONPATH=. python tools/check_clingo.py
```

## Evidence, not a solver wrapper

The Python generator enumerates candidates and grows each reduct closure. The
checker enumerates every reduct model and tests proper subsets for stability;
model intersections and bounded proof heights reconstruct the other evidence.
All unfounded subsets are independently checked. Shared strict parsing is
explicit. JavaScript provides equivalent evidence for browser exploration, but
an export is independently checked only after `stablelab verify` accepts it.

Local checks: nine Python tests; four Node/actual-Chrome tests; all 1,177 two-atom
programs with up to two signed-body normal rules/constraints; 200 seeded
three-atom programs; strict report forgery checks; installed wheel reproduction.
Optional clingo 5.8.3 reference agreed on stable families for all 1,387 programs
(ten controls plus 1,177 exhaustive and 200 seeded cases). These finite tests do
not prove general solver equivalence.

Chrome checks ten controls at widths 1280/390/320, all 900 candidate selections,
6,537 unfounded subset selections and 16,605 obligations, 1,926 closure rounds,
all queries, rule/reduct/support verdicts, ten downloaded exports accepted by the
independent Python checker, stale input, invalid input and recovery.

## Exact boundaries

At most eight supplied atoms, 32 normal rules/constraints. No implicit grounding,
classical negation, disjunction, choice, aggregates, optimization or well-founded
semantics. JSON, not clingo-language compatibility. Stable model counts are not
probabilities. This implements established finite methods, not a new algorithm.

[Exact contract](CONTRACT.md) · [Prior-work ledger](SOURCES.md)

## Safe replacement: strong equivalence

The [safe-replacement inspector](https://midya8.github.io/stablelab/equivalence.html) compares every finite SE interpretation and supplies a concrete positive-normal context when two modules differ. Equal stable families, even with equal classical models, are not enough. Eleven controls include that exact failure and a cycle-context witness.

The comparison accepts at most five atoms and 24 rules per side. It checks all 3ⁿ pairs, exports both augmented evidence families, and has an independent three-valued checker plus proper-subset stable-family reconstruction. Shared parsers/base checker and the fixed-vocabulary normal-context scope are explicit in [EQUIVALENCE.md](EQUIVALENCE.md).

```sh
stablelab compare comparison.json > proof.json
stablelab verify-comparison proof.json
```

Version 0.2.0 preserves the base eight-atom inspector. It introduces no paid API or runtime solver dependency.
