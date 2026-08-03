# Status

- OpenReview ID: `fG4nXq9Ytm`; submission: 21407.
- Contract: 6 anchored live claims / 12 maximum points, saved under `contract/` from `outputs/live/20260803T023041Z`.
- Sources: arXiv 2602.01105 source/PDF hash-pinned in `evidence/source/`.
- Compute: local CPU/local GTX 1050 only; no HF Jobs, cpu-upgrade, paid, or remote compute.
- Claim 1: **toy**. Exact diagonal special case of Algorithm 1 verifies the source sign-after-orthogonalization update chain. It does not reproduce GPT-scale training, Figure 2, or Theorem 4.4.
- Next: independent Claim 1 toy review, then Claim 2 source audit.
- Claim 2: **inconclusive**. The literal GPT-2 124M/355M/770M, 48B-token Figure-3 convergence comparison requires the primary source's four A100 80GB DDP setup and is infeasible on local CPU/GTX 1050. No reduced optimizer toy is used as evidence for that ranking. Evidence: `outputs/claim2_source_cpu_audit/`.
