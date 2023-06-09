# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 15:13:13 2023

@author: xinlo
"""
# -----------------------------------------------------------------------------
# Solar PV table (one 2x11 CS-400W)
# Units: m, N, kg, s, N/m2, kg/m3
# Xinlong Du, 2023
# -----------------------------------------------------------------------------
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

# MATERIAL properties----------------------------------------------------------
Es = 2.0e11;		      #Steel Young's modulus
nu = 0.3;                 #Poisson's ratio
Gs = Es/2./(1+nu);        #Shear modulus of steel
rho_s = 7850.0;           #Steel mass density

# Define  SECTIONS ------------------------------------------------------------
# SECTION properties for purlin C-Section 8CS2.5x059 in AISI Manual (2002)
A_pu = 0.822*in2m**2;     #cross-sectional area
Iz_pu = 7.79*in2m**4;     #second moment of area about the local z-axis
Iy_pu = 0.674*in2m**4;    #second moment of area about the local y-axis
Jx_pu = 0.000954*in2m**4;  #torsional moment of inertia of section
mass_pu = A_pu*rho_s;     #mass per unit length

# define NODES-----------------------------------------------------------------
node(1,             0.0, 0.0,    0.0)
node(2,         30*in2m, 0.0,    0.0)
node(3,         60*in2m, 0.0,    0.0)
node(4,         90*in2m, 0.0,    0.0)

# define BOUNDARY CONDITIONS---------------------------------------------------
fix(1, 1, 1, 1, 1, 1, 1);

# define ELEMENTS--------------------------------------------------------------
postTransfTag = 1;
vecxz = [0.0, 0.0, 1.0];
geomTransf('Linear', postTransfTag, *vecxz);

element('elasticBeamColumn', 101, *[1, 2], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, postTransfTag, '-mass', mass_pu);
element('elasticBeamColumn', 102, *[2, 3], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, postTransfTag, '-mass', mass_pu);
element('elasticBeamColumn', 103, *[3, 4], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, postTransfTag, '-mass', mass_pu);

allNodeTags=getNodeTags();
alleleTags=getEleTags();
# render the model
#vfo.createODB(model="solarPanel")
vfo.plot_model()

# eigen analysis---------------------------------------------------------------
eigenValues = eigen(3);
omega = np.sqrt(eigenValues);
freq = omega/(2*math.pi);

vfo.plot_modeshape(modenumber=1, scale=1); #plot mode shape 1
vfo.plot_modeshape(modenumber=2, scale=1); #plot mode shape 2
vfo.plot_modeshape(modenumber=3, scale=1); #plot mode shape 3

#%% load wind tunnel test DATA
import h5py
filename = "../../../../RWDI/Wind Tunnel Data/tilt_n30deg.hdf5"

with h5py.File(filename, "r") as f:
    # get the key of interest; may or may NOT be a group
    a_group_key = list(f.keys())[0]
    # get the object names in the group and returns as a list
    objNames = list(f[a_group_key])
    # preferred methods to get dataset values
    Cp = f[a_group_key]['Row1'][()]  # returns as a numpy array
    dtNorm = f[a_group_key]['dtNorm'][()]

#%% define LOADS---------------------------------------------------------------
L=169.25*in2m;
U=27.0;
dt=0.02;
rho_air=1.226;
p=0.5*rho_air*U*U*Cp;
x=L*np.array([0.125/2+0.25/2,0.25,0.25,0.25/2+0.125/2]);
y=L*np.array([0.125/2+0.5/2,0.5/2+0.75/2,0.75/2+1/2,1/2+1.25/2,1.25/2+1/2,1/2+0.75/2,0.75/2+0.125/2]);
A_trib=np.outer(x, y);
A_trib=np.reshape(A_trib,(1,28),order='F');
#A_trib=np.repeat(A_trib,np.shape(p)[0],axis=0);
Force=np.multiply(p,A_trib);
Force=Force.T.tolist()

timeSeries('Path',1,'-dt',dt,'-values',*Force[1],'-prependZero');
pattern('Plain',1,1);
load(3, *[0.0, 1.0, 1.0, 0.0, 0.0, 0.0]);

# define DAMPING
rayleigh(0.0,0.0,0.0,2*0.02/(eigenValues[0]**0.5));

# define ANALYSIS PARAMETERS---------------------------------------------------
constraints('Plain');  # how it handles boundary conditions
numberer('RCM');	   # renumber dof's to minimize band-width 
system('UmfPack');     # how to store and solve the system of equations in the analysis
test('NormDispIncr', 1.0e-08, 1000); # determine if convergence has been achieved at the end of an iteration step
algorithm('KrylovNewton');
integrator('Newmark', 0.5, 0.25);
analysis('Transient'); # define type of analysis static or transient
ok = analyze(100, 0.02);
print('Finished')

#%% output forces on joints at the last time step, used for verification-------
# element resisting forces for purlins
eleForces101=eleForce(101);
eleForces101Local=eleResponse(101, 'localForces')
eleForces102=eleForce(102);
eleForces102Local=eleResponse(102, 'localForces')
eleForces103=eleForce(103);
eleForces103Local=eleResponse(103, 'localForces')
nodeForces2end=np.array(eleForces101Local[6:12])+np.array(eleForces102Local[0:6]);
nodeForces3end=np.array(eleForces102Local[6:12])+np.array(eleForces103Local[0:6]);