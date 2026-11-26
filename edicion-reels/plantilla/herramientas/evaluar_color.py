# evaluar_color.py BRUTO.png CORREGIDO.png → diferencia en pared/techo y en PIEL (media RGB y saturación), capturas de
# QuickTime del mismo instante (herramientas/capturar_quicktime.sh). Aprobado: dif. media ≤ 5 niveles, piel ±2 niveles por canal
# y saturación de piel ±0,01. Mirar solo zonas neutras (pared) NO basta: una corrección puede clavar la pared y dejar la cara
# más roja/saturada (hoy-restock, 2026-11-26).
import numpy as np, sys
from PIL import Image
a = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)[20:1600,10:1060]
c = np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(float)[20:1600,10:1060]
m = (a[...,0]>a[...,1])&(a[...,1]>a[...,2])&(a[...,0]-a[...,2]>30)&(a[...,0]>90)
def sat(X): v=X[m]; return ((v.max(1)-v.min(1))/np.maximum(v.max(1),1)).mean()
print('dif media total', np.abs(a-c).mean().round(2), '| pared', a[100:300,30:200].mean((0,1)).round(1), c[100:300,30:200].mean((0,1)).round(1),
      '| piel', a[m].mean(0).round(1), c[m].mean(0).round(1), 'sat', round(sat(a),3), round(sat(c),3))
