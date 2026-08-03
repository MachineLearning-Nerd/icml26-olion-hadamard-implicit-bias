import json, subprocess, sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,'src/claim2_gpt2_cpu_audit.py'],cwd=R,check=True,stdout=subprocess.DEVNULL)
d=json.loads((R/'outputs/claim2_source_cpu_audit/report.json').read_text())
assert d['required_source_phrases_found'] and d['verdict']=='inconclusive'
assert 'CPU-infeasible' in d['decision'] and 'toy outcome' in d['conclusion']
