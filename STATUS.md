# Status

- Paper: OLion, arXiv 2602.01105; challenge record fG4nXq9Ytm, submission 21407.
- Classification: direct paper match for the ICML 2026 reproduction collection.
- Contract: six anchored live claims / 12 maximum points, saved under contract/.
- Sources: arXiv PDF and source archive are hash-pinned in evidence/source/SHA256SUMS.
- Official code: kv-wang/OLion, audited at commit 017e5defc621db1e122759797b88bbf251aed5ee.
- Compute policy: local CPU and GTX 1050 only; no HF Jobs, paid, upgraded, or remote compute.
- Branch policy: main is the only canonical branch; no legacy or ORX branches remain.
- Claim 1: toy. Exact diagonal special case of Algorithm 1 verifies the orthogonalize/sign/update operation order. It does not verify GPT training, Figure 2, or Theorem 4.4.
- Claim 2: inconclusive source audit. The literal GPT-2 124M/355M/770M OpenWebText comparison requires the source's four A100 80GB DDP setup. The source's 48B-token/100K-iteration overview and 20,000-step appendix detail are both recorded in README.md.
- Claims 3–6: unverified; their paper production paths and current evidence boundaries are documented in README.md.
- Publication: not allowed by the current local challenge state.
- Next: source-audit Claim 3, then independently review the Claim 2 feasibility boundary.
