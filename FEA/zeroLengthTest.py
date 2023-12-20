# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 16:13:48 2023

@author: xinlo
"""
from openseespy.opensees import *
import numpy as np
import math
import pandas as pd

# visulization
import vfo.vfo as vfo

import matplotlib.pyplot as plt
big_fig_size = (3.5,3);
plt_line_width = 0.5; 
fig_font_size = 8;

#%% SET UP---------------------------------------------------------------------
wipe();
model('basic', '-ndm', 3, '-ndf', 6);
dataDir = 'Data';

node(1,0.0,0.0,0.0);
node(2,0.0,0.0,0.0);
fix(1, 1, 1, 1, 1, 1, 1);

# material for dispX-----------------------------------------------------------
Fy=1500.0;
E0=7.0e6;
b=0.0001;
uniaxialMaterial('Steel01', 1, Fy, E0, b)

E=2.55e7;
Fy=-1.0e6;
gap=-1.8e-3;
eta=0.99999;
uniaxialMaterial('ElasticPPGap', 2, E, Fy, gap, eta)

uniaxialMaterial('Parallel', 101, *[1,2])

# material for dispY-----------------------------------------------------------
Fy=2000.0;
E0=6.0e6;
b=0.45;
uniaxialMaterial('Steel01', 3, Fy, E0, b)

E=7.7e7;
Fy=-1.0e6;
gap=-2.7e-4;
eta=0.99999;
uniaxialMaterial('ElasticPPGap', 4, E, Fy, gap, eta)

uniaxialMaterial('Parallel', 102, *[3,4])

# material for dispZ-----------------------------------------------------------
Fy=1600.0;
E0=7.0e6;
b=0.001;
uniaxialMaterial('Steel01', 103, Fy, E0, b)

# material for rotX-----------------------------------------------------------
Fy=17.0;
E0=2.9e4;
b=0.13;
uniaxialMaterial('Steel01', 5, Fy, E0, b)

E=1.0e4;
Fy=1.0e7;
gap=0.0088;
eta=0.99999;
uniaxialMaterial('ElasticPPGap', 6, E, Fy, gap, eta)

E=3.5e4;
Fy=-1.0e3;
gap=-0.0075;
eta=0.99999;
uniaxialMaterial('ElasticPPGap', 7, E, Fy, gap, eta)

# E=9.6e4;
# uniaxialMaterial('Elastic', 8, E)

uniaxialMaterial('Parallel', 104, *[5,6,7])

# material for rotY-----------------------------------------------------------
Fy=28.0;
E0=8.9e3;
b=0.005;
uniaxialMaterial('Steel01', 9, Fy, E0, b)

E=5.6e3;
Fy=30.0;
gap=0.027;
eta=0.1;
uniaxialMaterial('ElasticPPGap', 10, E, Fy, gap, eta)

E=5.0e3;
Fy=-30;
gap=-0.017;
eta=0.09;
uniaxialMaterial('ElasticPPGap', 11, E, Fy, gap, eta)

uniaxialMaterial('Parallel', 105, *[9,10,11])

# material for rotZ-----------------------------------------------------------
Fy=40.0;
E0=5.0e4;
b=0.05;
uniaxialMaterial('Steel01', 12, Fy, E0, b)

E=7.0e3;
Fy=-1.0e7;
gap=-0.03;
eta=0.99999;
uniaxialMaterial('ElasticPPGap', 13, E, Fy, gap, eta)

fpc=-1.4e3;
epsc0=-0.1;
fpcu=0.0;
epsU=-0.06;
uniaxialMaterial('Concrete01',14,fpc,epsc0,fpcu,epsU)

uniaxialMaterial('Parallel', 106, *[12,13,14])

# define element---------------------------------------------------------------
element('zeroLength', 1, *[1,2], '-mat', *[101,102,103,104,105,106], '-dir', *[1,2,3,4,5,6])

timeSeries('Linear',1);
#timeSeries('Path',1,'-dt',1.0,'-values',*[0.0,1.0,0.0,-1.0,0.0],'-prependZero');
pattern('Plain',1,1);
load(2, *[1.0, 1.0, 1.0, 1.0, 1.0, 1.0]);

# Define RECORDERS ------------------------------------------------------------
recorder('Node', '-file', f'{dataDir}/zeroLengthTest.out', '-time', '-node', *[2], '-dof', *[1,2,3,4,5,6], 'disp');

# define ANALYSIS PARAMETERS---------------------------------------------------
constraints('Plain');  # how it handles boundary conditions
numberer('Plain');	   # renumber dof's to minimize band-width 
system('BandGeneral'); # how to store and solve the system of equations in the analysis
test('NormDispIncr', 1.0e-08, 1000); # determine if convergence has been achieved at the end of an iteration step
algorithm('Linear');
#integrator('LoadControl', 0.1)
dof=5;
if dof==1:
    Dincr=0.1e-3;
    nSteps=35;
elif dof==2:
    Dincr=1.5e-3/50;
    nSteps=50;
elif dof==3:
    Dincr=0.1e-3;
    nSteps=50;
elif dof==4:
    Dincr=0.01/50;
    nSteps=50;
elif dof==5:
    Dincr=0.05/50;
    nSteps=50;
elif dof==6:
    Dincr=-0.05/50
    nSteps=55;
                                  #Node,  dof, 1st incr, Jd,  min,   max
integrator('DisplacementControl',    2,   dof,   Dincr,    1,  Dincr, Dincr);
analysis('Static');	# define type of analysis static or transient
analyze(nSteps);

                                  #Node,  dof, 1st incr, Jd,  min,   max
integrator('DisplacementControl',    2,   dof,  -Dincr,    1,  -Dincr, -Dincr);
analysis('Static');	# define type of analysis static or transient
analyze(nSteps*2);

                                  #Node,  dof, 1st incr, Jd,  min,   max
integrator('DisplacementControl',    2,   dof,   Dincr,    1,  Dincr, Dincr);
analysis('Static');	# define type of analysis static or transient
analyze(nSteps+5);

print('Finished')
wipe()

#%% postprocessing-------------------------------------------------------------
file_name = './Data/zeroLengthTest.out'
nodeDisps = np.loadtxt(file_name)

abaqusData=pd.ExcelFile('jointResponseVelBC.xlsx');

# dispX------------------------------------------------------------------------
if dof==1:
    abaDispX=pd.read_excel(abaqusData,'dispX2');
    
    fig = plt.figure(figsize=big_fig_size)
    ax = fig.add_axes([0, 0, 1, 1])
    plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
    ax.tick_params(direction="in")
    ax.plot(0.001*abaDispX[abaDispX.columns[14]],abaDispX[abaDispX.columns[13]],linewidth=plt_line_width,color='b',label='Abaqus solid ele.')
    ax.plot(nodeDisps[:,dof],nodeDisps[:,0],linewidth=plt_line_width,color='r',label='OpenSees springs')
    plt.legend(loc="lower right")
    ax=plt.gca()
    ax.set_xlabel('X disp. (m)',fontsize=fig_font_size)
    ax.set_ylabel('Force (N)',fontsize=fig_font_size)
    plt.savefig('./Data/springOutput/dispX.tif', transparent=False, bbox_inches='tight', dpi=100)
    ax.set_ylim([-10000,2500])
    plt.savefig('./Data/springOutput/dispXlocal.tif', transparent=False, bbox_inches='tight', dpi=100)
elif dof==2:
    abaDispY=pd.read_excel(abaqusData,'dispY2');
    
    fig = plt.figure(figsize=big_fig_size)
    ax = fig.add_axes([0, 0, 1, 1])
    plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
    ax.tick_params(direction="in")
    ax.plot(0.001*abaDispY[abaDispY.columns[14]],abaDispY[abaDispY.columns[13]],linewidth=plt_line_width,color='b',label='Abaqus solid ele.')
    ax.plot(nodeDisps[:,dof],nodeDisps[:,0],linewidth=plt_line_width,color='r',label='OpenSees springs')
    plt.legend(loc="lower right")
    ax=plt.gca()
    ax.set_xlabel('Y disp. (m)',fontsize=fig_font_size)
    ax.set_ylabel('Force (N)',fontsize=fig_font_size)
    plt.savefig('./Data/springOutput/dispY.tif', transparent=False, bbox_inches='tight', dpi=100)
    ax.set_ylim([-20000,6000])
    plt.savefig('./Data/springOutput/dispYlocal.tif', transparent=False, bbox_inches='tight', dpi=100)
elif dof==3:
    abaDispZ=pd.read_excel(abaqusData,'dispZ2');
    
    fig = plt.figure(figsize=big_fig_size)
    ax = fig.add_axes([0, 0, 1, 1])
    plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
    ax.tick_params(direction="in")
    ax.plot(0.001*abaDispZ[abaDispZ.columns[14]],abaDispZ[abaDispZ.columns[13]],linewidth=plt_line_width,color='b',label='Abaqus solid ele.')
    ax.plot(nodeDisps[:,dof],nodeDisps[:,0],linewidth=plt_line_width,color='r',label='OpenSees springs')
    plt.legend(loc="lower right")
    ax=plt.gca()
    ax.set_xlabel('Z disp. (m)',fontsize=fig_font_size)
    ax.set_ylabel('Force (N)',fontsize=fig_font_size)
    plt.savefig('./Data/springOutput/dispZ.tif', transparent=False, bbox_inches='tight', dpi=100)
elif dof==4:
    abaRotX=pd.read_excel(abaqusData,'rotaX');
    
    fig = plt.figure(figsize=big_fig_size)
    ax = fig.add_axes([0, 0, 1, 1])
    plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
    ax.tick_params(direction="in")
    ax.plot(abaRotX[abaRotX.columns[6]],0.001*abaRotX[abaRotX.columns[3]],linewidth=plt_line_width,color='b',label='Abaqus solid ele.')
    ax.plot(nodeDisps[:,dof],nodeDisps[:,0],linewidth=plt_line_width,color='r',label='OpenSees springs')
    plt.legend(loc="lower right")
    ax=plt.gca()
    ax.set_xlabel('X rotation (rad)',fontsize=fig_font_size)
    ax.set_ylabel('Moment (N.m)',fontsize=fig_font_size)
    plt.savefig('./Data/springOutput/rotX.tif', transparent=False, bbox_inches='tight', dpi=100)
    ax.set_ylim([-40,40])
    plt.savefig('./Data/springOutput/rotXlocal.tif', transparent=False, bbox_inches='tight', dpi=100)
elif dof==5:
    abaRotY=pd.read_excel(abaqusData,'rotaY');
    
    fig = plt.figure(figsize=big_fig_size)
    ax = fig.add_axes([0, 0, 1, 1])
    plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
    ax.tick_params(direction="in")
    ax.plot(abaRotY[abaRotY.columns[1]],0.001*abaRotY[abaRotY.columns[3]],linewidth=plt_line_width,color='b',label='Abaqus solid ele.')
    ax.plot(nodeDisps[:,dof],nodeDisps[:,0],linewidth=plt_line_width,color='r',label='OpenSees springs')
    plt.legend(loc="lower right")
    ax=plt.gca()
    ax.set_xlabel('Y rotation (rad)',fontsize=fig_font_size)
    ax.set_ylabel('Moment (N.m)',fontsize=fig_font_size)
    plt.savefig('./Data/springOutput/rotY.tif', transparent=False, bbox_inches='tight', dpi=100)
    ax.set_ylim([-40,40])
    plt.savefig('./Data/springOutput/rotYlocal.tif', transparent=False, bbox_inches='tight', dpi=100)
elif dof==6:
    abaRotZ=pd.read_excel(abaqusData,'rotaZ2');
    
    fig = plt.figure(figsize=big_fig_size)
    ax = fig.add_axes([0, 0, 1, 1])
    plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
    ax.tick_params(direction="in")
    ax.plot(-abaRotZ[abaRotZ.columns[14]],-0.001*abaRotZ[abaRotZ.columns[13]],linewidth=plt_line_width,color='b',label='Abaqus solid ele.')
    ax.plot(nodeDisps[:,dof],nodeDisps[:,0],linewidth=plt_line_width,color='r',label='OpenSees springs')
    plt.legend(loc="lower right")
    ax=plt.gca()
    ax.set_xlabel('Z rotation (rad)',fontsize=fig_font_size)
    ax.set_ylabel('Moment (N.m)',fontsize=fig_font_size)
    plt.savefig('./Data/springOutput/rotZ.tif', transparent=False, bbox_inches='tight', dpi=100)