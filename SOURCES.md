# Sources and attribution

StableLab implements established finite normal-program semantics. No algorithm,
new semantics, benchmark superiority or general solver equivalence is claimed.
The ten controls and implementation are developed for this project. Historical
phenomena are not presented as newly invented examples or discoveries.

1. Michael Gelfond and Vladimir Lifschitz, **The Stable Model Semantics for Logic
   Programming** (1988), ICLP/SLP, pp. 1070-1080.
   https://www.cs.utexas.edu/~vl/papers/stable.pdf
   Bibliographic record: https://www.cs.utexas.edu/~ai-lab/?gel88=
   Direct introduction, definition and theorem/example sections read. Basis for
   deletion/erasure reduct and candidate-equals-least-model test. Its original
   paper's unique-canonical-model terminology is not used to exclude programs
   with several stable models from this tool's enumerated family.
2. Vladimir Lifschitz, **Answer Sets and the Language of Answer Set Programming**.
   https://www.cs.utexas.edu/~vl/papers/1.AnswerSets.pdf
   Positive/negative normal-rule definitions and extensions/constraint sections
   read directly. Basis for least closure, reduct and headless constraints. Other
   reviewed language extensions are NOT implemented here.
3. Vladimir Lifschitz, **Thirteen Definitions of a Stable Model**.
   https://www.cs.utexas.edu/~vl/papers/13defs.pdf
   Abstract/introduction and sections on unfounded sets and support read directly,
   not a claim to have read the whole paper. Basis for model-plus-no-nonempty-
   unfounded-subset characterization and support/acyclic-grounding distinction.
   StableLab enumerates all candidate subsets, not just loops or loop formulas.
4. Marek Sergot, Imperial College, **Stable models ('Answer sets')**, course 491
   Knowledge Representation, February 2006 / November 2016 version.
   http://www.doc.ic.ac.uk/~mjs/teaching/KnowledgeRep491/StableModels-2x1.pdf
   Definitions, relationship-to-other-semantics and summary/generating-rule
   sections read. Supports the warning that minimal plus supported is insufficient.
5. Potassco, **ASP Basics**.
   https://potassco.org/guide/basics/
   Core-rule syntax and cyclic derivation/negation sections read. Confirms normal
   rules, constraints, and even/odd cycles. Illustrative constructs inspire the
   controls, without copying a tutorial or claiming the project invented them.
6. Potassco, **The clingo Input Language**.
   https://potassco.org/guide/language/
   Basic atoms/literals and normal/constraint syntax consulted. The much larger
   language is explicitly excluded. This web guide may describe work-in-progress
   language extensions; none of those extensions is used to define this subset.
7. ASP competition, **ASP-Core-2 Input Language Format**.
   https://www.mat.unical.it/aspcomp2013/files/ASP-CORE-2.03b.pdf
   Section 2.5 model/minimal-reduct-model semantics read. Its retained-true-body
   reduct presentation differs from this project's classical GL deletion/erasure
   presentation. For the implemented ground normal fragment the subset-model
   stability criterion is used; no full ASP-Core conformance is claimed.
8. Potassco, **clingo**.
   https://potassco.org/clingo/
   Official software overview read; distinguishes grounding from solving and links
   stable series documentation versus work-in-progress series 6. Optional local
   clingo 5.8.3 was used ONLY as an external check of stable-model families for
   1,387 explicitly finite programs. Runtime implementation has no clingo
   dependency; that comparison does not independently validate proof evidence/UI.

## Independent boundaries

The generator uses iterative closure. The checker does not import it: it enumerates
all models of each reduct, tests inclusion-minimality, intersects definite models,
and reconstructs rounds by bounded proof heights. Both use the same strict input
parser. They independently enumerate unfounded subsets. The browser computes its
own matching report, but an individual export is not described as independently
verified until the separate Python checker accepts it.

This is a bounded learning and inspection tool, not a new ASP solver. It does not
infer real agents' beliefs, execute supplied code, call a model/API or assign
probabilities to model counts.
