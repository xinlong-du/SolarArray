# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 00:07:38 2023

@author: xinlo
"""
# -----------------------------------------------------------------------------
# Solar PV rack 2x6 CS-400W
# Units: m, N, kg, s, N/m2, kg/m3
# Xinlong Du, 2022
#
# -----------------------------------------------------------------------------
# set systemTime [clock seconds] 
# puts "Starting Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"
# set startTime [clock clicks -milliseconds];
from openseespy.opensees import *
import numpy as np
import math

# visulization
import vfo.vfo as vfo

# SET UP ----------------------------------------------------------------------
wipe();
model('basic', '-ndm', 3, '-ndf', 6);
dataDir = 'Data';
#os.mkdir(dataDir);
in2m=0.0254; #convert inch to meter
g=9.8;       #gravitational acceleration (m/s2)

# MATERIAL properties----------------------------------------------------------
Es = 2.0e11;		      #Steel Young's modulus
nu = 0.3;                 #Poisson's ratio
Gs = Es/2./(1+nu);        #Shear modulus of steel
rho_s = 7850.0;           #Steel mass density

# Define  SECTIONS ------------------------------------------------------------
# SECTION properties for purlin C-Section 12CS3.5x105 in AISI Manual (2002)
# A_pu = 2.09*in2m**2;     #cross-sectional area
# Iz_pu = 43.8*in2m**4;     #second moment of area about the local z-axis
# Iy_pu = 3.07*in2m**4;    #second moment of area about the local y-axis
# Jx_pu = 0.00769*in2m**4;  #torsional moment of inertia of section
# mass_pu = A_pu*rho_s;     #mass per unit length

# SECTION properties for purlin C-Section 8CS3.5x059 in AISI Manual (2002)
A_pu = 0.940*in2m**2;     #cross-sectional area
Iz_pu = 9.65*in2m**4;     #second moment of area about the local z-axis
Iy_pu = 1.52*in2m**4;     #second moment of area about the local y-axis
Jx_pu = 0.00109*in2m**4;  #torsional moment of inertia of section
mass_pu = A_pu*rho_s;     #mass per unit length

# SECTION properties for loading beam
A_lb = A_pu*10**2;         #cross-sectional area
Iz_lb = Iz_pu*10**4;     #second moment of area about the local z-axis
Iy_lb = Iy_pu*10**4;     #second moment of area about the local y-axis
Jx_lb = Jx_pu*10**4;  #torsional moment of inertia of section
mass_lb = mass_pu*10*2;     #mass per unit length

# SECTION properties for spring
A_sp = A_pu*0.1**2;         #cross-sectional area
Iz_sp = Iz_pu*0.1**4;     #second moment of area about the local z-axis
Iy_sp = Iy_pu*0.1**4;     #second moment of area about the local y-axis
Jx_sp = Jx_pu*0.1**4;  #torsional moment of inertia of section
mass_sp = mass_pu*0.1*2;     #mass per unit length

for i in range(0,13):
    node(i+1,   i*0.5,  0, 0);
    node(i+101, i*0.5, 0.5, 0);

fix(1,  1, 1, 1, 1, 0, 0);
fix(13, 0, 1, 1, 0, 0, 0);

purlinTransfTag = 1;
vecxz = [0.0, 0.0, 1.0];
geomTransf('Linear', purlinTransfTag, *vecxz);
for i in range (0,12):
    # purlin # 1
    #                            elemID   nodeI  nodeJ
    element('elasticBeamColumn', i+1,   *[i+1,     i+2], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, purlinTransfTag, '-mass', mass_pu);
    element('elasticBeamColumn', i+101, *[i+101, i+102], A_lb, Es, Gs, Jx_lb, Iy_lb, Iz_lb, purlinTransfTag, '-mass', mass_lb);
    
for i in range(0,6):
    element('elasticBeamColumn', i+201, *[i*2+2, i*2+102], A_sp, Es, Gs, Jx_sp, Iy_sp, Iz_sp, purlinTransfTag, '-mass', mass_pu);

allNodeTags=getNodeTags();
alleleTags=getEleTags();

# render the model
vfo.createODB(model="loadingBeam", loadcase="static")
vfo.plot_model()

loadNode=107;
timeSeries('Linear',10000);
pattern('Plain', 10000, 10000);
load(loadNode, *[0.0, 1.0, 0.0, 0.0, 0.0, 0.0]);

# define ANALYSIS PARAMETERS---------------------------------------------------
constraints('Plain');  # how it handles boundary conditions
numberer('RCM');	   # renumber dof's to minimize band-width 
system('UmfPack'); # how to store and solve the system of equations in the analysis
test('NormDispIncr', 1.0e-08, 1000); # determine if convergence has been achieved at the end of an iteration step
algorithm('Linear');
integrator('DisplacementControl', loadNode, 2, 0.01)
#integrator('LoadControl',1000000)
analysis('Static');	# define type of analysis static or transient
analyze(10);
print('Finished')

wipe()
vfo.plot_deformedshape(model="loadingBeam", loadcase="static", scale=5)