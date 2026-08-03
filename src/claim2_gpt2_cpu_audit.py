#!/usr/bin/env python3
"""Source-faithful feasibility audit for anchored Claim 2; no training is run."""
import hashlib,json,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
tar=ROOT/'evidence/source/arxiv-2602.01105-source.tar.gz'
out=ROOT/'outputs/claim2_source_cpu_audit'
with tarfile.open(tar,'r:gz') as z:
    # Hardware details are in the appendix; literal Figure-3 claim is in experiments.
    text='\n'.join(z.extractfile(name).read().decode() for name in ('experiments.tex','appendix.tex'))
required={
 'hardware':'4 NVIDIA A100 80GB GPUs',
 'sizes':'small} (124M)',
 'data':'OpenWebText dataset',
 'schedule':'20,000 steps',
 'claim':'converges faster than both AdamW, Lion and Muon.'
}
missing=[k for k,v in required.items() if v not in text]
report={
 'claim_id':2,'verdict':'inconclusive','kind':'cpu_infeasibility_source_audit',
 'source_sha256':hashlib.sha256(tar.read_bytes()).hexdigest(),
 'source_member':['experiments.tex','appendix.tex'],'required_source_phrases_found':not missing,
 'missing_phrases':missing,
 'literal_claim_scope':{'models':['GPT-2 Small 124M','Medium 355M','Large 770M'], 'dataset':'OpenWebText','tokens':'48B (anchored contract)','comparators':['OLion','AdamW','Lion','Muon']},
 'source_compute_requirement':'4 NVIDIA A100 80GB GPUs; DDP; CUDA 11.8+; GPT-2 Small/Medium/Large training',
 'available_compute':'local CPU/local GTX 1050 only',
 'decision':'CPU-infeasible: do not run a reduced optimizer toy as evidence for the literal cross-scale GPT-2 convergence claim.',
 'metric':'validation/training loss trajectories (Figure 3); unavailable without source-scale training/data.',
 'controls':'No synthetic control is warranted because it cannot test Figure 3 ranking; source audit checks all literal prerequisites.',
 'conclusion':'No verified/falsified/toy outcome is asserted for Claim 2.'
}
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
(out/'source_excerpt.txt').write_text('\n'.join(f'[{k}] {v}' for k,v in required.items())+'\n')
print(json.dumps(report,indent=2))
