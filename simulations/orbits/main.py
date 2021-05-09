import sys
import time
import matplotlib.pyplot as mplplt
from   math              import pi, cos, sin, sqrt
from   numpy             import arange
from   matplotlib        import animation
mplplt.style.use('fivethirtyeight')

tdoNum = int(sys.argv[1])
step   = pi/200
Re     = 6378.137
Perigees     = [[184.82+Re, 183.48+Re, 183.48+Re,   198.19+Re,   198.27+Re,   198.27+Re,   198.27+Re],
                [180.30+Re, 183.39+Re, 183.39+Re,   255.38+Re,   255.38+Re,   255.38+Re]]
Apogees      = [[351.01+Re, 398.42+Re, 398.42+Re, 35397.11+Re, 35458.49+Re, 35458.49+Re, 35458.49+Re],
                [310.70+Re, 341.02+Re, 341.02+Re, 35298.48+Re, 35298.48+Re, 35298.48+Re]]
Inclinations = [[   28.151,    28.166,    28.166,      26.367,      26.366,      26.366,      26.366],
                [   28.190,    28.211,    28.211,      26.233,      26.233,      26.233]]

def simulate(title, X, Y, Z, labels, nframes, markers, colors, orbitNum):
  def init():
    return(ax)
  def animate(frame):
    plots = [ax.plot(X[frame], Y[frame], Z[frame],
                     marker = markers[orbitNum[frame]],
                     color = colors[orbitNum[frame]], markersize = 2,
                     label = labels[orbitNum[frame]])]
    return plots

  xlim = (min(X)-abs(min(X)*0.5), max(X)+abs(max(X)*0.5))
  ylim = (min(Y)-abs(min(Y)*0.5), max(Y)+abs(max(Y)*0.5))
  zlim = (min(Z)-abs(min(Z)*0.5), max(Z)+abs(max(Z)*0.5))
  fig  = mplplt.figure()
  ax   = fig.add_subplot(111, projection = '3d', xlim = xlim, ylim = ylim, zlim = zlim)
  ax.legend(loc = 'upper right', shadow = True)
  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')
  ax.azim = 70
  ax.elev = 25
  anim = animation.FuncAnimation(fig, animate, init_func = init, frames = nframes)
  anim.save(title, fps = 30, writer = 'Pillow', progress_callback = lambda i, n: print(i))

X, Y, Z, orbitNum = [], [], [], []
startAngle = [   0.0,    0.0,    0.0, pi*0.2,    0.5,    0.0,    0.0]
endAngle   = [pi*2.0, pi*2.0, pi*0.5, pi*2.2, pi*2.0, pi*2.0, pi*2.0]
for orbit in range(len(Perigees[1])):
  peri = Perigees[tdoNum-1][orbit]       # Perigee
  apog = Apogees [tdoNum-1][orbit]       # Apogee
  incl = Inclinations[tdoNum-1][orbit]   # Inclination
  smaj = (peri+apog)/2.0          # Semi-Major Axis
  ecce = (peri-smaj)/smaj
  smin = sqrt(smaj**2*(1.0-ecce**2))
  orbitNum.extend([orbit for angle in arange(startAngle[orbit], endAngle[orbit], step)])
  X.extend([smaj*(ecce+cos(angle))*cos(incl) for angle in arange(startAngle[orbit], endAngle[orbit], step)])
  Y.extend([smin*sin(angle)                  for angle in arange(startAngle[orbit], endAngle[orbit], step)])
  Z.extend([smaj*(ecce+cos(angle))*sin(incl) for angle in arange(startAngle[orbit], endAngle[orbit], step)])

labels  = ['Orbit '+str(i) for i in range(len(Perigees[0]))]
markers = ['*', '.', '*', '.', '.', '.', '.']
colors  = ['b', 'r', 'y', 'g', 'k', 'k', 'k', 'k']
simulate('TDO'+str(tdoNum)+'.gif', X, Y, Z, labels, len(X), markers, colors, orbitNum)