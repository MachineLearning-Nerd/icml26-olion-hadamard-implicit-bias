"""Exact 2x2 diagonal special case of OLion Algorithm 1, source method.tex:141-156.
No numerical SVD is needed: polar(diag(a,b))=diag(sign(a),sign(b))."""
import csv,json,hashlib,os
OUT='outputs/claim1_algorithm_toy'
def sign(x): return 1 if x >= 0 else -1
def polar_diag(a,b): return (sign(a),sign(b))
def main():
 # Fixed, predeclared diagonal gradient; beta values zero isolate Algorithm-1 orthogonalize/sign operation.
 a,b=3,-2; beta1=beta2=0; eta=.1; gamma=1; lam=0; x=(1.,-1.)
 # M=(1-beta2)g, Gtilde=(1-beta1)g + beta1 M = g.
 q=polar_diag(a,b); s=q; d=(gamma*s[0],gamma*s[1])
 xnext=(x[0]-eta*d[0]-lam*eta*x[0],x[1]-eta*d[1]-lam*eta*x[1])
 row={'gradient':[a,b],'momentum':[a,b],'nesterov_mix':[a,b],'polar_q':list(q),'sign_s':list(s),'direction_d':list(d),'x0':list(x),'x1':list(xnext),'parameters':{'beta1':beta1,'beta2':beta2,'eta':eta,'gamma':gamma,'lambda':lam}}
 os.makedirs(OUT,exist_ok=True)
 open(OUT+'/results.json','w').write(json.dumps(row,indent=2)+'\n')
 open(OUT+'/summary.json','w').write(json.dumps({'verdict':'toy','scope':'Exact diagonal special-case execution of Algorithm 1 orthogonalize/sign/update chain; not GPT training or Theorem 4.4 verification.','checks':{'polar_is_orthogonal':q[0]*q[0]==1 and q[1]*q[1]==1,'sign_after_orthogonalization':s==q,'expected_update':xnext==(.9,-.9)}},indent=2)+'\n')
 with open(OUT+'/SHA256SUMS','w') as f:
  for p in ['results.json','summary.json']:
   f.write(hashlib.sha256(open(OUT+'/'+p,'rb').read()).hexdigest()+'  '+p+'\n')
if __name__=='__main__':main()
