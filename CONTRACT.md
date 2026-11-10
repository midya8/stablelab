# StableLab contract

## Scope

Finite propositional normal rules with default negation and headless constraints.
At most eight declared atoms, 32 rules and therefore 256 candidate interpretations.
No variables/grounding, function symbols, classical negation, disjunction, choice,
aggregates, optimization or well-founded semantics. JSON interface, not a clingo
text parser. This is an inspectable finite enumeration, not a scalable ASP solver
or a new algorithm. All controls are developed synthetic programs.

Input has exactly `atoms` and `rules`. Atoms are sorted unique lowercase names
matching `[a-z][a-z0-9_]{0,23}`. Rules retain supplied order and have exactly `id`,
`head`, `positive`, `negative`. IDs are unique lowercase names. Head is a declared
atom or null (constraint). Body lists are sorted unique declared atoms. The same
atom may appear positively and negatively: that rule's original body cannot be
true. Facts have empty bodies. A constraint with empty body is always violated.
The declared atom vocabulary can include atoms absent from every rule.

## Semantics

For candidate M a body's positive atoms must all belong to M; its default-negated
atoms must all be absent. A rule is satisfied when its body is false or its head
belongs to M. A headless constraint must have a false body. A classical model
satisfies every rule. Supported additionally means every included atom is the
head of some true-body rule. Minimality means no proper subset is a classical
model of the ORIGINAL program. This is not the stability test.

The Gelfond-Lifschitz reduct removes rules with any default-negated atom in M,
then erases all default-negated literals from remaining rules. Its definite
(non-constraint) part has a least closure, built from empty in synchronous rounds.
All ready rule IDs are reported, including those with already derived heads.
A final no-new-atom round is included. Constraints do not derive atoms. A stable
candidate equals this least closure and violates no original rule or constraint.
Equivalently it is an inclusion-minimal model of its reduct.

Every candidate's nonempty subsets are tested for unfoundedness at the candidate.
For every rule whose head is in U, either the body is false at M (missing positive
or present negative), or the positive body intersects U. All three actual reason
lists are reported, not one arbitrary reason. No head rule means no external
support, so the obligation family may be empty. A model is stable iff none of its
nonempty subsets is unfounded. No such claim is made without model satisfaction.
These are complete unfounded subsets, not only graph loops or greatest sets.

Masks use declared atoms least-significant-bit first; records and subset masks
are ascending. Supports and atom lists follow declared lexical atom order.
Rule evidence retains input rule order. Countermodel counts are not probability.

For a nonempty stable-model family, brave means present in some stable model;
skeptical means present in every stable model. Both are null when there are no
stable models. This is an explicit UI convention that avoids presenting vacuous
skeptical truth as evidence. Witness masks with/without each atom are included.
Empty program has stable mask 0; empty-body constraint has no model.

## Evidence and independent checks

`stablelab-evidence-v1` embeds the exact normalized input. Every candidate has all
rule truth tests, retained positive reduct rules, synchronous closure rounds,
constraint violations, candidate/closure differences, every support, every
unfounded subset with full rule obligations, proper-subset classical models and
all four verdicts. Global model families and query witnesses are complete.

Python generator grows closure; independent checker enumerates all reduct models
and uses their intersection to check least definite closure, all proper subset
models to judge stability, and bounded proof heights to reconstruct rounds. It
also independently enumerates unfounded subsets and verifies the stable/model-
without-unfounded equivalence. Shared strict input validation is disclosed.
The checker never imports the generator. Full canonical JSON comparison includes
all fields, list order, types, missing/extra fields and Boolean-vs-number values.
Browser exports are independently checked only after Python verification, not
merely because their generator matches Python on tests.

Optional external reference: `tools/check_clingo.py` compares only stable-model
families for these ground normal programs against installed clingo. It does not
validate this project's UI, proof evidence or general clingo compatibility.
