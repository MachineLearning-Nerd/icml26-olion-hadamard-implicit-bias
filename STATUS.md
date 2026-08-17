# Status

- Repository: https://github.com/MachineLearning-Nerd/icml26-olion-hadamard-implicit-bias
- Former name: icml26-repro-fG4nXq9Ytm-olion-hadamard-implicit-bias
- Paper: OLion: Approaching the Hadamard Ideal by Intersecting Spectral and l-infinity Implicit Biases
- Authors: Zixiao Wang, Yifei Shen, and Huishuai Zhang
- Venue: ICML 2026
- OpenReview: fG4nXq9Ytm
- arXiv: 2602.01105
- Branches: main only; canonical/default branch
- Commit identity: MachineLearning-Nerd
- Compute: local CPU/local GTX 1050 only; no remote, paid, Hugging Face, or other external compute

| Claim | Local status |
| --- | --- |
| C1 sign after orthogonalization | TOY_SOURCE_ALGORITHM1 |
| C2 GPT-2 convergence | INCONCLUSIVE_CPU_INFEASIBLE |
| C3 Llama-2-7B pretraining | UNVERIFIED |
| C4 Llama-3.1-8B supervised fine-tuning | UNVERIFIED |
| C5 diagonal-isotropy convergence theorem | UNVERIFIED |
| C6 simultaneous spectral and l-infinity control | UNVERIFIED |

Overall: INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY. The publication gate is false. The source PDF/archive, exact diagonal Algorithm 1 fixture, and GPT-2 feasibility record are locally pinned; no full-paper reproduction is claimed.

Evidence: CLAIM_EVIDENCE.md, SOURCE_AUDIT.md, EVIDENCE_MANIFEST.json, outputs/claim1_algorithm_toy/, outputs/claim2_source_cpu_audit/, contract/live_claims.json, and verify_final.py.
