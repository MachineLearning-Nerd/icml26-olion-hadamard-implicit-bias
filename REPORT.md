# Audit report

## Executive result

This repository is a published, source-pinned audit of OLion: Approaching the Hadamard Ideal by Intersecting Spectral and l-infinity Implicit Biases. The final result is INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY, with publication_allowed: false.

Claim 1 has an exact 2-by-2 diagonal special-case check of the sign-after-orthogonalization update. Claim 2 has a source-backed CPU-infeasibility decision for the literal GPT-2 comparison. Claims 3–6 have documented paper production paths but no independent local result.

## Claim results

| Claim | Result |
| --- | --- |
| C1 | TOY_SOURCE_ALGORITHM1 |
| C2 | INCONCLUSIVE_CPU_INFEASIBLE |
| C3 | UNVERIFIED |
| C4 | UNVERIFIED |
| C5 | UNVERIFIED |
| C6 | UNVERIFIED |

## Reproduction boundary

The repository distinguishes paper-reported values, source-audited production paths, and outputs independently generated here. It does not claim the paper's GPT-2, Llama, SiT, benchmark, norm, or convergence results as reproduced.

## Verification

Run python3 verify_final.py from the repository root for the repository-native publication gate. It checks branch state, canonical commit attribution, source/output hashes, archive shape, claim contracts, the evidence manifest, and the scoped verdict.
