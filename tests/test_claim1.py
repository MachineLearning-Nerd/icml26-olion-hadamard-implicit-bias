import json,subprocess,sys
subprocess.run([sys.executable,'src/claim1_olion_diagonal_toy.py'],check=True)
r=json.load(open('outputs/claim1_algorithm_toy/results.json'))
assert r['polar_q']==[1,-1] and r['sign_s']==[1,-1] and r['x1']==[.9,-.9]
