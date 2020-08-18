import rpy2.robjects as ro
from rpy2.robjects.packages import importr

grdevices = importr('grDevices')

grdevices.png(file="Rpy2Curve.png", width=512, height=512)
p = ro.r('curve(sin, -2*pi, 2*pi)')
grdevices.dev_off()
p = ro.r('curve(sin, -2*pi, 2*pi)')    
