# Claim evidence ledger

Overall verdict: INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY. No full-paper reproduction or publication claim is allowed.

## C1 — Sign after orthogonalization

- Paper claim: OLion applies entrywise Sign to an orthogonalized momentum direction to approximate the intersection of spectral and l-infinity constraint sets.
- Production path: form the momentum and Nesterov mix, apply the Newton–Schulz or polar orthogonalization, apply entrywise sign, scale the direction, and update the parameter. The source anchors are method.tex lines 47–59 and 138–202.
- Local evidence: src/claim1_olion_diagonal_toy.py checks a diagonal gradient (3,-2), beta1=beta2=0, eta=0.1, gamma=1, zero weight decay, and x0=(1,-1). It records polar Q=(1,-1), sign S=(1,-1), and x1=(0.9,-0.9).
- Status: TOY_SOURCE_ALGORITHM1. This validates one exact special case only; it does not establish general matrix behavior, training loss, norm trajectories, or Theorem 4.4.

## C2 — GPT-2 convergence

- Paper claim: OLion converges faster than AdamW, Lion, and Muon on GPT-2 Small 124M, Medium 355M, and Large 770M trained on OpenWebText.
- Production path: train all three model sizes under the common optimizer protocol, preserve the loss trajectories, and compare convergence in Figure 3. The paper overview is experiments.tex lines 14–46; appendix.tex lines 17–27 gives the A100/DDP, model, dataset, and schedule details.
- Local evidence: outputs/claim2_source_cpu_audit/report.json checks the literal model sizes, dataset, comparator names, token scope, and four-A100 requirement. No reduced optimizer toy is used as Figure 3 evidence.
- Status: INCONCLUSIVE_CPU_INFEASIBLE. The source-scale run is not performed under the local CPU/GTX-1050-only policy. The source's 48B-token/100K-iteration overview and 20,000-step appendix detail are both preserved.

## C3 — Llama-2-7B pretraining

- Paper claim: OLion maintains lower training loss than Muon, Lion, and AdamW on Llama-2-7B pretraining with 32B tokens and an effective batch size of 4M.
- Production path: run the distributed Llama-2-7B FSDP pipeline, compare training and validation loss curves, and retain the 8K-step/4M-token protocol. The paper anchors are experiments.tex lines 14–16 and 49–67 and appendix.tex lines 35–37.
- Local evidence: no Llama-2 checkpoint, distributed run, dataset, or loss artifact is present.
- Status: UNVERIFIED.

## C4 — Llama-3.1-8B supervised fine-tuning

- Paper claim: OLion gives the best downstream accuracy across GSM8K, MATH, NumGLUE, SimulEq, and Aqua, including 60.04% versus AdamW's 57.99% on GSM8K 0-shot.
- Production path: fine-tune AdamW-pretrained Llama-3.1-8B on MathInstruct with the full-parameter 1533-step protocol, then run the five benchmark evaluation scripts. The paper anchors are experiments.tex lines 263–286 and appendix.tex lines 437–464.
- Local evidence: the table is present in the pinned source, but no checkpoint, fine-tuning run, benchmark predictions, or metric log is stored here.
- Status: UNVERIFIED.

## C5 — Diagonal-isotropy convergence theorem

- Paper claim: under Assumption 4.2, OLion achieves an O(1/sqrt(T)) convergence rate using a geometry-aware stationarity measure.
- Production path: audit the diagonal-isotropy assumption, alignment lower bound, descent argument, and theorem rate in method.tex lines 205–399; independently test equalities and relaxed-condition controls.
- Local evidence: the exact diagonal toy does not test the assumption or replace an independent theorem audit. The source's empirical assumption checks are described in appendix.tex lines 202–204, but their training outputs are not locally reproduced.
- Status: UNVERIFIED.

## C6 — Simultaneous spectral and l-infinity control

- Paper claim: OLion keeps both spectral norm and l-infinity norm small relative to the optimizer-specific baselines, combining the biases associated with AdamW and Muon.
- Production path: train GPT-2 Small, record representative matrix singular-value/spectral and entrywise-magnitude trajectories, and compare OLion with AdamW, Lion, and Muon. The paper anchors are experiments.tex lines 97–142 and intro.tex lines 85–112.
- Local evidence: source figures and descriptions are pinned, but no source-scale run or norm trajectory is present.
- Status: UNVERIFIED.

## Publication gate

The repository is suitable for a scoped source-and-toy audit. It is not evidence that the six paper claims have been independently reproduced, so publication_allowed is false.
