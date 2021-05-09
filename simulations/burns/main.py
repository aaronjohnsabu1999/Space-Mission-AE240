import numpy                  as np
from math       import pi, cos, exp, log, sin, tan, atan
from matplotlib import pyplot as plt

G  = 6.67259*(10**(-11))
Me = 5.97219*(10**24)
Re = 6378100.0
mu = G*Me
g0 = 9.81
deg2rad = pi/180.0

emptyM = {'booster':  4067.0, 'stage1':  21351.0, 'stage2':  2316.0, 'AEHF': 6168.0}
proppM = {'booster': 42630.0, 'stage1': 284089.0, 'stage2': 20830.0, 'AEHF':    0.0}
Isp    = {'booster':   279.3, 'stage1':    311.3, 'stage2':   450.5, 'AEHF':    0.0}
bTime  = {'booster':    94.0, 'stage1':    253.0, 'stage2':   842.0, 'AEHF':    0.0}
M0     = 0.0
for component in emptyM.keys():
  if component == 'booster':
    M0 +=  5*emptyM[component] + 5*proppM[component]
  else:
    M0 += emptyM[component] + proppM[component]

## Calculate g at Height h
def gravity(h):
  return mu/((Re+h)**2)

## Vertical Ascent - Constant Mass Rate
def vertAsc(t, m0, Isp, v0, h0, x0, j0, ht1, beta):
  m = m0 - beta*t
  v = g0*Isp*log(m0/m) - g0*t + v0
  j = j0
  h = (m0*g0*Isp/beta)*((1.0-(beta*t/m0))*log(1.0-(beta*t/m0))+(beta*t/m0)) - 0.5*gravity(ht1)*(t**2) + v0*t + h0
  x = x0
  return m, v, j, h, x
  
## Constant Pitch Rate Gravity Turn
def constQ(t, m0, Isp, v0, h0, x0, j0, ht1, q0):
  j = q0*t + j0
  m = m0*exp(-2*gravity(ht1)*(sin(j)-sin(j0))/(q0*g0*Isp))
  v = gravity(ht1)*sin(j)/q0 + v0
  h = gravity(ht1)*(cos(2*j0)-cos(2*j))/(4*q0*q0) + h0
  x = gravity(ht1)*((j-j0)-((sin(2*j)-sin(2*j0))/2.0))/(2*q0*q0) + x0
  return m, v, j, h, x

## Constant Velocity Gravity Turn
def constV(t, m0, Isp, v0, h0, x0, j0, ht1):
  v = v0
  j = 2*atan(exp(gravity(ht1)*t/v)*tan(j0/2.0))
  m = m0*((sin(j)/sin(j0))**(-v/(g0*Isp)))
  h = (v**2/gravity(ht1))*log(sin(j)/sin(j0)) + h0
  x = (v**2/gravity(ht1))*(j-j0) + x0
  return m, v, j, h, x

## Plot all values
def plotter(tArr, mArr, vArr, jArr, hArr, xArr):
  plt.plot(tArr, mArr, label = 'Burn Profile')
  plt.legend()
  plt.show()
  plt.plot(tArr, vArr, label = 'Velocity')
  plt.legend()
  plt.show()
  plt.plot(tArr, jArr, label = 'Angle')
  plt.legend()
  plt.show()
  plt.plot(tArr, hArr, label = 'Vertical Distance')
  plt.plot(tArr, xArr, label = 'Horizontal Distance')
  plt.legend()
  plt.show()

if __name__ == "__main__":
  tArr, vArr, jArr, hArr, xArr = [[0.0] for i in range(5)]
  mArr = [M0]
  
  ### Launch to Ejection of Boosters
  T1   = bTime['booster']
  m0   = M0
  Isp1 = (5*Isp['booster']*proppM['booster']/bTime['booster'] + Isp['stage1']*proppM['stage1']/bTime['stage1'])/(5*proppM['booster']/bTime['booster'] + proppM['stage1']/bTime['stage1'])
  mpB  = 5*proppM['booster']
  mpS1 = proppM['stage1']*T1/bTime['stage1']
  mp   = mpB + mpS1
  beta = mp/T1
  for t in np.arange(0, T1, 0.01):
    m, v, j, h, x = vertAsc(t, m0, Isp1, 0.0, 0.0, 0.0, 0.0, hArr[-1], beta)
    tArr.append(t)
    mArr.append(m)
    vArr.append(v)
    jArr.append(j)
    hArr.append(h)
    xArr.append(x)
  
  ### Ejection of Boosters to Ejection of Stage 1
  t0   = tArr[-1]
  T2   = bTime['stage1'] - bTime['booster']
  m0   = mArr[-1] - 5*emptyM['booster']
  Isp2 = Isp['stage1']
  v0   = vArr[-1]
  h0   = hArr[-1]
  x0   = xArr[-1]
  j0   = 0.5*deg2rad  # Pitch Kick
  q0   = 0.1*deg2rad
  for t in np.arange(0, T2, 0.01):
    m, v, j, h, x = constQ(t, m0, Isp2, v0, h0, x0, j0, hArr[-1], q0)
    tArr.append(t+t0)
    mArr.append(m)
    vArr.append(v)
    jArr.append(j)
    hArr.append(h)
    xArr.append(x)
  
  ### Ejection of Stage 1 to Satellite Deployment
  t0   = tArr[-1]
  T3   = bTime['stage2']
  m0   = mArr[-1] - emptyM['stage1']
  Isp3 = Isp['stage2']
  v0   = vArr[-1]
  h0   = hArr[-1]
  x0   = xArr[-1]
  j0   = jArr[-1]
  for t in np.arange(0, T3, 0.01):
    m, v, j, h, x = constV(t, m0, Isp3, v0, h0, x0, j0, hArr[-1])
    tArr.append(t+t0)
    mArr.append(m)
    vArr.append(v)
    jArr.append(j)
    hArr.append(h)
    xArr.append(x)
  
  plotter(tArr, mArr, vArr, jArr, hArr, xArr)