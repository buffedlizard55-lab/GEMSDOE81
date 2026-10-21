"""Lazy-greedy submodular maximum-coverage emission under the exact 300 m
triangular kernel: gain(x|S)=sum_q S(q)*max(0,k(|x-q|)-C(q)), C=coverage so far.
Candidate pool = top-`pool` surface pixels outside the catalogue exclusion zone."""
import heapq, numpy as np
OFFS=[(dy,dx,max(1-np.hypot(dy,dx)/3,0.)) for dy in range(-3,4) for dx in range(-3,4) if max(1-np.hypot(dy,dx)/3,0.)>0]
def greedy_cover(S, foot, allowed, n_target, pool=160000):
    S=np.asarray(S,np.float32); cand=np.zeros(S.shape,bool)
    f=np.where(allowed,S,-np.inf).ravel(); pool=min(pool,int(allowed.sum()))
    idx=np.argpartition(f,-pool)[-pool:]; cand.ravel()[idx]=True
    from scipy.ndimage import convolve
    ker=np.zeros((7,7),np.float32)
    for dy,dx,k in OFFS: ker[dy+3,dx+3]=k
    gain=convolve(np.where(foot,S,0.),ker,mode="constant")
    C=np.zeros(S.shape,np.float32); chosen=np.zeros(S.shape,bool)
    heap=[(-float(gain[y,x]),0,int(y),int(x)) for y,x in zip(*np.nonzero(cand))]
    heapq.heapify(heap); ver=1; H,W=S.shape
    def marginal(y,x):
        t=0.
        for dy,dx,k in OFFS:
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W: t+=S[yy,xx]*max(0.,k-C[yy,xx])
        return t
    while int(chosen.sum())<n_target and heap:
        neg,_,y,x=heapq.heappop(heap)
        if chosen[y,x]: continue
        m=marginal(y,x)
        if heap and m < -heap[0][0]-1e-12:
            heapq.heappush(heap,(-m,ver,y,x)); ver+=1; continue
        if m<=0: break
        chosen[y,x]=True
        for dy,dx,k in OFFS:
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and k>C[yy,xx]: C[yy,xx]=k
    return chosen
def poisson_thin_priority(S, allowed, n_target, min_dist=2.8, seed=81):
    """Control emitter: raster-order-free, surface-priority Poisson thinning."""
    order=np.argsort(-np.where(allowed,S,-np.inf).ravel(),kind="stable")
    chosen=np.zeros(S.shape,bool); H,W=S.shape; r2=min_dist**2; grid={}
    cell=max(1.,min_dist); cnt=0
    for flat in order:
        if cnt>=n_target: break
        y,x=divmod(int(flat),W)
        if not allowed[y,x]: continue
        cy,cx=int(y//cell),int(x//cell); ok=True
        for gy in range(cy-2,cy+3):
            for gx in range(cx-2,cx+3):
                for ky,kx in grid.get((gy,gx),()):
                    if (y-ky)**2+(x-kx)**2<r2: ok=False;break
                if not ok: break
            if not ok: break
        if ok: chosen[y,x]=True; grid.setdefault((cy,cx),[]).append((y,x)); cnt+=1
    return chosen
def batch_greedy_cover(S, foot, allowed, n_target, pool=60000, batch=1000):
    """Vectorised batch-greedy: every `batch` picks, recompute exact marginal
    gains for pool candidates only (pool x 29 kernel offsets), pick top-batch
    non-chosen. Approximate greedy (batch), disclosed in run card."""
    S=np.asarray(S,np.float32); f=np.where(allowed,S,-np.inf).ravel()
    pool=min(pool,int(allowed.sum())); idx=np.argpartition(f,-pool)[-pool:]
    ys,xs=np.unravel_index(idx,S.shape); C=np.zeros(S.shape,np.float32)
    chosen=np.zeros(S.shape,bool); H,W=S.shape; cnt=0
    off=np.array([(dy,dx,k) for dy,dx,k in OFFS])
    while cnt<n_target:
        yy=np.clip(ys[:,None]+off[None,:,0].astype(int),0,H-1); xx=np.clip(xs[:,None]+off[None,:,1].astype(int),0,W-1)
        valid=(ys[:,None]+off[None,:,0]>=0)&(ys[:,None]+off[None,:,0]<H)&(xs[:,None]+off[None,:,1]>=0)&(xs[:,None]+off[None,:,1]<W)
        gain=(S[yy,xx]*np.maximum(0.,off[None,:,2]-C[yy,xx])*valid).sum(1)
        gain[chosen[ys,xs]]=-np.inf
        take=np.argpartition(gain,-min(batch,n_target-cnt))[-min(batch,n_target-cnt):]
        for t in take:
            y,x=int(ys[t]),int(xs[t])
            if chosen[y,x]: continue
            chosen[y,x]=True; cnt+=1
            for dy,dx,k in OFFS:
                yyy,xxx=y+dy,x+dx
                if 0<=yyy<H and 0<=xxx<W and k>C[yyy,xxx]: C[yyy,xxx]=k
        if cnt>=n_target: break
    return chosen
