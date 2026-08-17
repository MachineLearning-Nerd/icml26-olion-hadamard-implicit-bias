# Environment and compute boundary

- Audit date: 2026-08-17.
- Allowed compute: local CPU and the local GTX 1050.
- Disallowed compute: remote GPUs, paid compute, Hugging Face CPU upgrades, Hugging Face Jobs, and other external accelerators.
- The repository stores the pinned arXiv PDF/source archive, an exact diagonal Algorithm 1 fixture, and a source-only GPT-2 feasibility audit.
- It does not contain the authors' training implementation, GPT-2/Llama/SiT checkpoints, OpenWebText or benchmark data, or source-scale loss and norm trajectories.

The local boundary is part of the result. The exact toy validates one operation path; it is not promoted to evidence for model training, figures, or the convergence theorem.
