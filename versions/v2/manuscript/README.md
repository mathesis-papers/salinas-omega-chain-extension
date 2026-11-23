# Least omega-chain-partitionable extensions

**Haobo Ma** — ChronoAI Pte Ltd, Singapore  
**Wenlin Zhang** — National University of Singapore; ChronoAI Pte Ltd, Singapore

## Result

A nonempty countable poset of bounded finite height has an extension
partitionable into omega-chains that order-embeds into every such extension
if and only if it has a greatest element. The comparison embeddings need
not preserve the specified copy of the original poset. In particular, the
two-element antichain answers Salinas Schmeis's Question 2.32 negatively.

The posing source is Remi Salinas Schmeis, *General Criterion for a Poset to
Admit a Partition Into omega-Chains*, arXiv:2610.29056v1, Question 2.32, p. 14:
https://arxiv.org/abs/2610.29056v1

## Build

The archive contains `note.tex`, `metadata.json`, `README.md`, `verify.py`
and `verification.json`. No additional figures or bibliography files are needed.
Build with Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively use a standard LaTeX distribution containing the packages named
in `note.tex`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The references are embedded in `note.tex`; no BibTeX invocation is needed.

## Mathematical coverage

- Written proofs: incompatible-ray obstruction, the two-point counterexample,
  arbitrary-poset extension existence, countable bounded-height classification,
  its finite and order-dual consequences, explicit lifting injections, ordinal
  chain extensions and the finite-skeleton obstruction.
- The pinned Lean declaration
  `D5.S3.ConceptDynamics.DagCompletion.SalinasSchmeisOmegaChainExtensionRefutation.result`
  proves the negative universal assertion using the connected fork. It does not
  state the two-point strengthening or the bounded-height classification.
  The definitions use induced order embeddings and partitions into inherited
  omega-chains. Exact source:
  https://github.com/the-omega-institute/trureturing/blob/2b5b552e72596710282b713f6587c7020544535d/D5/S3/ConceptDynamics/DagCompletion/SalinasSchmeisOmegaChainExtensionRefutation.lean
- Finite computations check the displayed orders, partitions and embeddings on
  the bounds in `verification.json`, all naturally labelled posets through five
  points, finite lifting sections and ordinal fibers. They do not establish the
  infinite statements; those have written proofs in `note.tex`.

To reproduce the finite computations using Python 3 and its standard library:

```sh
python3 verify.py > verification-new.json
diff -u verification.json verification-new.json
```

The source coverage table distinguishes the negative answer to Question 2.32,
new consequences not separately posed, results already established in the posing
paper, and questions outside the theorem's scope. Only the established problem
identifier `salinas-omega-chain-extension` is included in the metadata.

## License

Copyright 2026 Haobo Ma and Wenlin Zhang. Creative Commons Attribution 4.0
International, CC BY 4.0 (`cc-by-4.0`):
https://creativecommons.org/licenses/by/4.0/
