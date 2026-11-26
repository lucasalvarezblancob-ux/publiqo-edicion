# lut_quicktime.py DIR SALIDA.cube "t1,t2,t3"   (estándar desde 2026-11-26, Lucas: hoy-restock-*)
# DIR con qp_<t>.png (proxy SIN corrección, p. ej. proxy-base.mp4) y qb_<t>.png (bruto) capturados con
# herramientas/capturar_quicktime.sh en los mismos instantes. Se aplica encima del proxy con ffmpeg:
#   format=gbrp,lut3d=SALIDA.cube:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p + etiquetas bt709
# y se valida en un instante NO usado para medir con herramientas/evaluar_color.py (pared Y piel).
# LUT 3D proxy→bruto ajustada con regresión polinómica de grado 3 (con términos cruzados) sobre bloques de las capturas
# de QuickTime (qp_t = proxy-base, qb_t = bruto, mismo instante). A diferencia de curva.py (curvas por canal, que clavan
# los grises pero dejan la piel más roja/saturada), corrige también tono y saturación.
import numpy as np, sys
from PIL import Image
D, OUT, TS = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
def L(p): return np.asarray(Image.open(p).convert('RGB')).astype(np.float64)[20:1600, 10:1060]
def bloques(X, Y, k=4):
    n0 = (X.shape[0]//k)*k; n1 = (X.shape[1]//k)*k
    BX = X[:n0,:n1].reshape(n0//k,k,n1//k,k,3); BY = Y[:n0,:n1].reshape(n0//k,k,n1//k,k,3)
    ok = (BX.std((1,3)).max(-1) < 10) & (BY.std((1,3)).max(-1) < 10)
    return BX.mean((1,3))[ok], BY.mean((1,3))[ok]
def feats(P):
    x = P/255.0; r,g,b = x[:,0],x[:,1],x[:,2]
    cols = [np.ones_like(r), r,g,b, r*r,g*g,b*b, r*g,r*b,g*b, r**3,g**3,b**3, r*r*g,r*r*b,g*g*r,g*g*b,b*b*r,b*b*g, r*g*b]
    return np.stack(cols, 1)
P=[];R=[]
for t in TS:
    a,b = bloques(L(f'{D}/qp_{t}.png'), L(f'{D}/qb_{t}.png')); P.append(a); R.append(b)
P=np.concatenate(P); R=np.concatenate(R)
# pesos: que la piel (R>G>B saturada) cuente tanto como la pared aunque haya menos bloques
piel = (P[:,0]>P[:,1])&(P[:,1]>P[:,2])&(P[:,0]-P[:,2]>30)
w = np.where(piel, max(1.0, (~piel).sum()/max(piel.sum(),1)), 1.0)
F = feats(P); W = np.sqrt(w)[:,None]
coef = np.linalg.lstsq(F*W, (R/255.0)*W, rcond=None)[0]
print('bloques', len(P), 'piel', piel.sum(), 'error medio ajuste', np.abs(F@coef*255-R).mean().round(2))
N=33; g=np.linspace(0,1,N)
bb,gg,rr = np.meshgrid(g,g,g, indexing='ij')
grid = np.stack([rr.ravel(),gg.ravel(),bb.ravel()],1)*255
out = np.clip(feats(grid)@coef, 0, 1)
with open(OUT,'w') as f:
    f.write(f'LUT_3D_SIZE {N}\n')
    for v in out: f.write(f'{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n')
