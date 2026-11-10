# StableLab fact inputs / 0.3.0

Uniform equivalence is a different module promise from strong equivalence: both programs must give the same stable-model family after every set of positive facts is added. This extension checks the complete fact-input table and, independently of that table's generation path, computes the finite UE-pair characterization.

## Scope

The input is exactly the 0.2.0 comparison schema: `atoms`, `left`, `right`; up to five declared atoms and 24 normal rules per side, including constraints. The same strict body/identifier validation applies. Contexts contain only positive single-atom facts from this same vocabulary. Every one of the `2**n` fact sets is included, in ascending mask order, including empty and full input. There are at most 32 fact contexts and 243 SE interpretations. Duplicate input facts are immaterial; fact sets have unique atoms. Adding already-derivable facts remains a distinct input set.

No disjunction, classical negation, aggregates, variables, arbitrary ASP parser, fresh-atom context UI, update semantics or scalable algorithm claim. The cited papers cover broader languages; this implementation does not.

## Complete evidence

- Embedded 0.2.0 comparison evidence includes all SE pairs and any broader rule-context separator, preserving the strict difference between ordinary, uniform and strong equivalence.
- Each UE pair lists all strictly larger proper SE extensions at the same Y. A pair is a UE pair exactly when it is an SE pair and no such extension exists. Diagonal accepted SE pairs always qualify.
- Each fact context lists its concrete fact rules, both stable families and every candidate's original-model verdict, least definite reduct closure, closure-violated constraints and stable verdict. The UI exposes each augmented original program and actual reduct, not just a family count.
- If facts separate, select the context with smallest cardinality, then smallest mask. The report lists every smaller-cardinality context, all of which must agree, and embeds complete base evidence for both sides under the selected context. A separator can have zero facts.

This certifies minimum cardinality within the complete declared-vocabulary fact-context space. It is not merely subset minimality, not a claim about arbitrary rule contexts, and not a statement about the fewest edits to a program.

## Theory and independent checking

Eiter and Fink (2003), Definition 3 and Theorem 3: finite programs are uniformly equivalent exactly when their UE-model sets coincide. UE consists of diagonal SE pairs and maximal proper SE pairs for each fixed Y. Their Example 2 gives normal programs `P = {a <- not b; a <- b}` and `Q = {a <- not c; a <- c}`: uniformly equivalent but not strongly equivalent. Adding rule `b <- a` separates them. StableLab includes this credited control and checks all eight fact inputs plus an actual rule separator.

The generator computes fact families by the existing base closure engine, not by re-labeling UE pairs. The Python verifier imports neither generator. It calls the existing independent three-valued comparison checker for the embedded SE evidence, checks maximal proper extensions, then independently reconstructs every fact-context candidate by enumerating definite reduct models and intersecting them for least closure; stability uses exhaustive proper-subset reduct-model checks. The embedded minimum-witness reports also pass the existing independent base verifier. Equality of the UE-set verdict and the complete fact-table verdict is required. Shared strict parsers, atom ordering, checked comparison records and the base evidence checker are disclosed dependencies, not separate independent solvers. JS/Python parity is portability evidence.

## Controls and reproduction

Ten synthetic controls separate fact-only and rule-context guarantees, require minimum fact separators of cardinalities 0/1/2/3/4, retain a safe transitive rewrite, show contextual repair of an odd default loop, distinguish derivation from a constraint, and handle empty/five-atom vocabularies. These are finite semantics examples, not real agent behavior.

```sh
python -m pip install .
stablelab uniform comparison.json > proof.json
stablelab verify-uniform proof.json
python -m stablelab uniform comparison.json > proof.json
python -m stablelab verify-uniform proof.json
python -m unittest discover -s tests -v
node --test tests/test_*.mjs tests/test_*.cjs
bash tools/check_wheel.sh
```

The 0.2.0 strong-equivalence inspector and base eight-atom inspector remain available. No paid service or runtime solver is added. Browser exports need the Python verifier before they are independently checked.

Optional external family cross-check: `python -m pip install clingo==5.8.3`, then `python tools/check_uniform_clingo.py`. clingo is not installed by the project and is not a runtime dependency. This checks finite stable families, not every proof field or UI state.
