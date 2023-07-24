# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 16:13:48 2023

@author: xinlo
"""
from openseespy.opensees import *
import numpy as np
import math

# visulization
import vfo.vfo as vfo

#%% SET UP ----------------------------------------------------------------------
wipe();
model('basic', '-ndm', 3, '-ndf', 6);
dataDir = 'Data';

node(1,0.0,0.0,0.0);
node(2,0.0,0.0,0.0);
fix(1, 1, 1, 1, 1, 1, 1);

Fy=3.65;
E0=1494.8;
b=0.0001;
a1=0.0;
a2=1.0;
a3=0.0;
a4=1.0;
uniaxialMaterial('Steel01', 1, Fy, E0, b, a1, a2, a3, a4)

E=10000.0;
Fy=10000.0;
gap=0.05;
eta=0.99999;
uniaxialMaterial('ElasticPPGap', 2, E, Fy, gap, eta)

E=10000.0;
Fy=-10000.0;
gap=-0.05;
eta=0.99999;
uniaxialMaterial('ElasticPPGap', 3, E, Fy, gap, eta)

uniaxialMaterial('Parallel', 4, *[1,2,3])
element('zeroLength', 1, *[1,2], '-mat', *[4,4,4,4,4,4], '-dir', *[1,2,3,4,5,6])

timeSeries('Linear',1);
#timeSeries('Path',1,'-dt',1.0,'-values',*[0.0,1.0,0.0,-1.0,0.0],'-prependZero');
pattern('Plain',1,1);
load(2, *[1.0, 0.0, 0.0, 0.0, 0.0, 0.0]);

# Define RECORDERS ------------------------------------------------------------
recorder('Node', '-file', f'{dataDir}/zeroLengthTest.out', '-time', '-node', *[2], '-dof', *[1], 'disp');

# define ANALYSIS PARAMETERS---------------------------------------------------
constraints('Plain');  # how it handles boundary conditions
numberer('Plain');	   # renumber dof's to minimize band-width 
system('BandGeneral'); # how to store and solve the system of equations in the analysis
test('NormDispIncr', 1.0e-08, 1000); # determine if convergence has been achieved at the end of an iteration step
algorithm('Linear');
integrator('LoadControl', 0.0001)
analysis('Static');	# define type of analysis static or transient
analyze(200000);

integrator('LoadControl', -0.0001)
analysis('Static');	# define type of analysis static or transient
analyze(400000);

integrator('LoadControl', 0.0001)
analysis('Static');	# define type of analysis static or transient
analyze(400000);

print('Finished')
wipe()

#%%
file_name = './Data/zeroLengthTest.out'
nodeDisps = np.loadtxt(file_name)

import matplotlib.pyplot as plt
big_fig_size = (3.5,3);
plt_line_width = 0.5; 
fig_font_size = 8;

fig = plt.figure(figsize=big_fig_size)
ax = fig.add_axes([0, 0, 1, 1])
plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
ax.tick_params(direction="in")
ax.plot(nodeDisps[:,1],nodeDisps[:,0], linewidth=plt_line_width)