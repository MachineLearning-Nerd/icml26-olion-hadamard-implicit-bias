# Claim 2 output — GPT-2 source and compute audit

This directory records a source-only feasibility audit for the anchored GPT-2 convergence claim. It does not train a reduced model and does not treat a toy optimizer result as evidence for Figure 3.

The pinned source contains the GPT-2 model sizes, OpenWebText dataset, optimizer comparators, and the paper's stated four NVIDIA A100 80GB DDP requirement. The local policy permits only CPU and GTX 1050 hardware, so the literal 124M/355M/770M experiment is marked inconclusive rather than reproduced or falsified.

The audit also preserves a source-detail discrepancy: the main experimental overview states 48B tokens and 100K iterations, while the appendix's detailed GPT-2 setup states 20,000 steps. Both are recorded in the repository README.

Files:

- report.json: machine-readable scope, decision, and verdict.
- source_excerpt.txt: minimal source phrases used by the audit.
- run.log: captured audit output.
- SHA256SUMS: checksums for the audit files.
