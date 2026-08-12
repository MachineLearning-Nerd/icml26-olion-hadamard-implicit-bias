# OLion: Approaching the Hadamard Ideal by Intersecting Spectral and l-infinity Implicit Biases

This repository is the MachineLearning-Nerd audit and reproduction workspace for the ICML 2026 reproduction record associated with OLion. It contains pinned primary-source material, a small exact algorithm check, and a documented feasibility boundary for the paper's large-scale experiments. It is not the authors' reference implementation.

Paper: [arXiv:2602.01105](https://arxiv.org/abs/2602.01105)

Challenge record: [OpenReview fG4nXq9Ytm](https://openreview.net/forum?id=fG4nXq9Ytm)

Official implementation: [kv-wang/OLion](https://github.com/kv-wang/OLion), audited at commit [017e5defc621db1e122759797b88bbf251aed5ee](https://github.com/kv-wang/OLion/tree/017e5defc621db1e122759797b88bbf251aed5ee)

## Current result

| Item | Result |
| --- | --- |
| Paper relationship | Direct paper match; ICML 2026 challenge record |
| Claim 1 | Toy reproduction: exact diagonal special case of Algorithm 1 |
| Claim 2 | Inconclusive: source-audited but literal GPT-2 experiment is infeasible on the available machine |
| Claims 3–6 | Unverified; source scope is recorded below |
| Local compute | CPU and GTX 1050 only |
| Publication | Not allowed by the local challenge state |
| Canonical branch | main only |

The narrow Claim 1 check reproduces the sign-after-orthogonalization update chain for a fixed 2-by-2 diagonal input. It does not reproduce model training, the paper's figures, or the convergence theorem. Claim 2 is not presented as a failed reproduction: the required source-scale run cannot be performed under the repository's local compute policy, and a reduced optimizer toy would not test the anchored GPT-2 ranking.

## What the paper does

OLion combines two update geometries for matrix-shaped parameters:

1. A Lion-style momentum/Nesterov direction is formed from the gradient.
2. The matrix direction is approximately orthogonalized with a few Newton–Schulz iterations, following the spectral geometry used by Muon.
3. An entrywise sign operation applies l-infinity-style coordinate control.
4. The resulting direction is used in the optimizer update, with the paper's weight-decay and optional magnitude-alignment details.

The motivating intersection is a scaled partial-Hadamard set: orthonormal columns with entries plus or minus 1/sqrt(d1), when such a matrix exists. The paper treats this as an idealized target; it does not guarantee that every update reaches an exact Hadamard matrix. Its empirical program compares OLion with AdamW, Lion, and Muon on GPT-2 and Llama pretraining, SiT image pretraining, and Llama-3.1 supervised fine-tuning.

## Repository contents

| Path | Purpose |
| --- | --- |
| contract/ | Immutable challenge metadata and the six anchored claims |
| evidence/source/ | Hash-pinned arXiv PDF and LaTeX source archive |
| src/claim1_olion_diagonal_toy.py | Exact diagonal special-case audit of the algorithmic update path |
| src/claim2_gpt2_cpu_audit.py | Source-only feasibility audit; intentionally does not train GPT-2 |
| outputs/claim1_algorithm_toy/ | Claim 1 values, verdict, and checksums |
| outputs/claim2_source_cpu_audit/ | Claim 2 report, source excerpt, run log, and checksums |
| tests/ | Small assertion-based checks for the two local audits |
| STATUS.md | Human-readable checkpoint and limitations |
| AUTONOMOUS_STATE.json | Machine-readable continuation state |

The official training code is kept as an external, commit-pinned reference because this repository's local artifacts are an audit record, not a fork of the authors' implementation.

## Branch inventory

| Branch | Role | State |
| --- | --- | --- |
| main | Canonical documentation, source pins, scripts, and evidence | Active and clean |

There are no ORX, challenge-ID, or stale legacy branches in the final repository. Future work for this audit should be committed to main with a claim-specific evidence directory and an explicit status change.

## Claim-to-evidence ledger

The challenge contract in contract/live_claims.json is the authority for the claim wording. The statuses below distinguish a source audit, a toy check, and a full reproduction.

### Claim 1 — sign after orthogonalization

Paper claim: OLion applies entrywise Sign to an orthogonalized momentum direction to approximate the intersection of spectral and l-infinity constraint sets (Section 4.1, Algorithm 1).

Production path in the paper:

1. Start with a matrix gradient and the optimizer's momentum state.
2. Form the mixed direction used by Algorithm 1.
3. Compute Q with NewtonSchulz(direction, K).
4. Compute S = sign(Q) entrywise.
5. Apply the scaled direction and parameter update.

Local evidence: src/claim1_olion_diagonal_toy.py uses a fixed diagonal gradient (3, -2), beta1 = beta2 = 0, learning rate 0.1, gamma = 1, zero weight decay, and x0 = (1, -1). For this exact diagonal case, the polar factor Q is (1, -1), the sign output S is (1, -1), and the update gives x1 = (0.9, -0.9). The checks and values are in outputs/claim1_algorithm_toy/.

Status: toy. This verifies the operation order and arithmetic in one exact special case. It is not evidence for general matrix behavior, training loss, norm trajectories, or Theorem 4.4.

### Claim 2 — GPT-2 convergence

Paper claim: on GPT-2 Small (124M), Medium (355M), and Large (770M), trained on OpenWebText with the anchored 48B-token scope, OLion converges faster than AdamW, Lion, and Muon (Figure 3a-c).

Production path in the paper:

1. Train each GPT-2 size on OpenWebText with the reported optimizer settings.
2. Use the four optimizer variants under a common evaluation protocol.
3. Compare training/validation loss trajectories and convergence speed in Figure 3.

Source boundary: the appendix specifies four NVIDIA A100 80GB GPUs with DDP and CUDA 11.8 or newer. The source's detailed GPT-2 paragraph says 20,000 steps, while the main experimental overview says 48B tokens and 100K iterations. Both statements are preserved here for auditability; this repository does not resolve the discrepancy.

Local evidence: outputs/claim2_source_cpu_audit/report.json checks the literal models, dataset, schedule, comparator names, and A100 requirement from the pinned source. Available hardware is only local CPU/GTX 1050.

Status: inconclusive source audit. The source-scale experiment was not run. No reduced optimizer toy is labeled as Figure 3 evidence because it would not test the cross-scale GPT-2 claim.

### Claim 3 — Llama-2-7B pretraining loss

Paper claim: with 32B tokens and an effective global batch size of 4M, OLion maintains lower training loss than AdamW, Lion, and Muon (Figure 4).

Production path in the paper: run the Llama-2-7B pretraining pipeline with FSDP2, context length 4096, local batch size 2, gradient accumulation 64, and 8192 steps; compare the loss curves under the same protocol. The appendix specifies eight NVIDIA RTX PRO 6000 GPUs and bfloat16 mixed precision.

Local evidence: no Llama run or loss artifact is present.

Status: unverified. The local machine cannot reproduce the stated scale.

### Claim 4 — Llama-3.1-8B supervised fine-tuning

Paper claim: full fine-tuning of AdamW-pretrained Llama-3.1-8B with OLion gives the best downstream accuracy across GSM8K, MATH, NumGLUE, SimulEq, and Aqua; the paper reports GSM8K 0-shot accuracy of 60.04% for OLion versus 57.99% for AdamW.

Production path in the paper: fine-tune the full model on MathInstruct for 1533 steps with global batch size 512, sequence length 2048, and bfloat16; evaluate the five math benchmarks under the reported zero- and few-shot protocols.

Local evidence: no Llama-3.1 checkpoint, fine-tuning run, or benchmark output is present.

Status: unverified. The cited numbers remain paper-reported values, not results produced by this repository.

### Claim 5 — diagonal-isotropy convergence theorem

Paper claim: under Assumption 4.2's diagonal-isotropy condition, OLion obtains an O(1/sqrt(T)) convergence rate using a geometry-aware stationarity measure (Theorem 4.4).

Production path in the paper: establish the diagonal-isotropy decomposition, use it to lower-bound the alignment between the mixed direction and the sign-after-orthogonalization direction, then derive the descent and rate argument. The appendix also reports empirical checks of the assumption along GPT-2 training.

Local evidence: the Claim 1 toy does not test this assumption or replace a proof. No independent numerical theorem audit or relaxed-condition control has been completed.

Status: unverified.

### Claim 6 — simultaneous spectral and l-infinity control

Paper claim: OLion keeps both spectral norm and l-infinity norm small relative to the optimizer-specific baselines, combining the biases associated with AdamW and Muon (Figure 2).

Production path in the paper: train GPT-2 Small, record representative weight-matrix singular-value/spectral and entrywise-magnitude trajectories, then compare OLion with AdamW and Muon across matrix shapes.

Local evidence: no source-scale GPT-2 run or norm trajectory is present. The Claim 2 feasibility audit does not produce Figure 2 evidence.

Status: unverified.

## Reproduction labels

- reproduced: the claimed result is independently obtained at the paper's relevant scope and the evidence is stored here.
- toy: a deliberately reduced or exact special-case check validates only a mechanism or boundary.
- source audit: the paper and implementation are inspected, but no claimed numerical result is generated.
- inconclusive: the claim cannot be decided under the documented compute/data boundary.
- unverified: no independent result has yet been produced.

This repository currently contains one toy result, one inconclusive source audit, and four unverified claims. It does not claim full reproduction.

## Source integrity and verification

The source archive and PDF are pinned in evidence/source/SHA256SUMS:

- arxiv-2602.01105-source.tar.gz: a731ba5fd46583ec282df7c6df76169f96e210602d4c992adc08e0f3f4a191b0
- arxiv-2602.01105.pdf: b5a0a43f3be4f22d6a6bfb947b3daf1f97b741d0d43c9c4f3f70377b241abf56

Run the lightweight checks from the repository root:

    (cd evidence/source && sha256sum -c SHA256SUMS)
    (cd outputs/claim1_algorithm_toy && sha256sum -c SHA256SUMS)
    (cd outputs/claim2_source_cpu_audit && sha256sum -c SHA256SUMS)
    python3 -m pytest -q tests/test_claim1.py tests/test_claim2_source_audit.py

The pytest command is an optional convenience check. The evidence verdicts do not depend on a full training run, and the repository intentionally does not launch the paper-scale experiments.

## Citation

    @misc{wang2026olionapproachinghadamardideal,
      title={OLion: Approaching the Hadamard Ideal by Intersecting Spectral and l-infinity Implicit Biases},
      author={Zixiao Wang and Yifei Shen and Huishuai Zhang},
      year={2026},
      eprint={2602.01105},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2602.01105}
    }

## Thank you

Thank you to Zixiao Wang, Yifei Shen, and Huishuai Zhang for sharing the OLion paper, its source materials, and the reference implementation. The clear algorithm description and published experimental details make it possible to separate a useful mechanism-level audit from claims that require substantially larger compute. This repository is intended as a respectful, transparent reproduction record and points readers back to the authors' work.

## Next checkpoint

The next scoped task is a source audit for Claim 3, followed by an independent review of the existing Claim 2 boundary. Any future result must add its command, configuration, source/model identity, output files, checksum, and claim-specific status before changing the overall verdict.
