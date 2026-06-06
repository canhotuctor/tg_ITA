import matplotlib.pyplot as plt
import numpy as np
from math import pi

x = np.arange(0, 1.01, 0.01)
y1 = np.sin(2.0 * pi * x)
y2 = np.sin(2.0 * pi * 2.0 * x)

plt.figure()
plt.plot(x, y1)
plt.plot(x, y2)
plt.legend(['1 Hz', '2 Hz'])
plt.savefig('image_plt_png.png', format='png')

plt.rc('text', usetex=True)
plt.rcParams.update({'font.family': 'serif'})
plt.rcParams.update({'font.size': 16})

plt.figure()
plt.grid()
plt.plot(x, y1, linewidth=2)
plt.plot(x, y2, linewidth=2)
plt.xlim(0, 1)
plt.ylim(-1, 1)
plt.xlabel(r'Time ($s$)')
plt.ylabel(r'Voltage ($V$)')
plt.legend([r'$1\ \mathrm{Hz}$', r'$2\ \mathrm{Hz}$'])
plt.tight_layout()
plt.savefig('image_plt_eps.eps', format='eps')
plt.savefig('image_plt_png400.png', format='png', dpi=400)
