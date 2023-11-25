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

# MATERIAL properties----------------------------------------------------------
Es = 2.0e11;		      #Steel Young's modulus
nu = 0.3;                 #Poisson's ratio
Gs = Es/2./(1+nu);        #Shear modulus of steel
rho_s = 7850.0;           #Steel mass density
Em = 70.0e9;              #Glass Young's modulus for module
nu_m = 0.22;              #Glass Poisson's ratio
rho_m = 2500.0;           #Glass mass density
Emf = 68.3e9;             #Aluminum Young's modules (module frame)
Gmf = Emf/2./(1+nu);      #Shear modulus of aluminum
rho_mf = 2690.0;          #Aluminum mass density

# Define  SECTIONS ------------------------------------------------------------
# SECTION properties for purlin C-Section 8CS2.5x059 in AISI Manual (2002)
A_pu = 0.538*in2m**2;     #cross-sectional area
Iz_pu = 1.35*in2m**4;     #second moment of area about the local z-axis
Iy_pu = 0.331*in2m**4;    #second moment of area about the local y-axis
Jx_pu = 0.000625*in2m**4; #torsional moment of inertia of section
mass_pu = A_pu*rho_s;     #mass per unit length

# SECTION properties for rafter HAT Section 6HU3x060 in AISI Manual (2002)
A_r = 0.954*in2m**2;      #cross-sectional area
Iz_r = 1.92*in2m**4       #second moment of area about the local z-axis
Iy_r = 4.15*in2m**4;      #second moment of area about the local y-axis
Jx_r = 0.00115*in2m**4;   #torsional moment of inertia of section
mass_r = A_r*rho_s;       #mass per unit length
    
# SECTION properties for post Pipe 2.25x2.25x1/8 (https://www.engineersedge.com/standard_material/aisc-steel-tube.htm)
A_po = 0.956*in2m**2;     #cross-sectional area
Iz_po = 0.712*in2m**4;    #second moment of area about the local z-axis
Iy_po = 0.712*in2m**4;    #second moment of area about the local y-axis
Jx_po = 1.15*in2m**4;     #torsional moment of inertia of section
mass_po = A_po*rho_s;     #mass per unit length
    
# SECTION properties for internal brace Pipe 2x2x1/8
A_ib = 0.84*in2m**2;      #cross-sectional area
Iz_ib = 0.486*in2m**4;     #second moment of area about the local z-axis
Iy_ib = 0.486*in2m**4;     #second moment of area about the local y-axis
Jx_ib = 0.796*in2m**4;     #torsional moment of inertia of section
mass_ib = A_ib*rho_s;      #mass per unit length

# SECTION properties for external brace Pipe 2x2x1/8
A_eb = 0.84*in2m**2;      #cross-sectional area
Iz_eb = 0.486*in2m**4;     #second moment of area about the local z-axis
Iy_eb = 0.486*in2m**4;     #second moment of area about the local y-axis
Jx_eb = 0.796*in2m**4;     #torsional moment of inertia of section
mass_eb = A_eb*rho_s;      #mass per unit length

# SECTION properties for module frames
A_mf = 168.07*0.001**2;    #cross-sectional area
Iz_mf = 21828.0*0.001**4;  #second moment of area about the local z-axis
Iy_mf = 9841.7*0.001**4;   #second moment of area about the local y-axis
#torsional moment of inertia of section: hollow section     + open section
Jx_mf = (4*319.8657*319.8657*(1.37+1.67+1.67+1.42)/4/74.21+11.96*2.01**3/3+4.96*1.36**3/3+17.86*1.42**3/3)*0.001**4;
mass_mf = A_mf*rho_mf;     #mass per unit length

# SECTION properties for module
moduleSecTag = 1;
h = 4.96*0.001; #depth of module
section('ElasticMembranePlateSection', moduleSecTag, Em, nu_m, h, rho_m)

# define NODES-----------------------------------------------------------------
# purlin # 1 from North
node(301, -5.3308*in2m,  95.3394*in2m, -54.0000*in2m)
node(302, -5.3308*in2m,  95.3394*in2m, -12.9167*in2m)
node(303, -5.3308*in2m,  95.3394*in2m, -11.4167*in2m)
node(304, -5.3308*in2m,  95.3394*in2m, 28.9167*in2m)
node(305, -5.3308*in2m,  95.3394*in2m, 30.4167*in2m)
node(306, -5.3308*in2m,  95.3394*in2m, 70.7500*in2m)
node(307, -5.3308*in2m,  95.3394*in2m, 72.2500*in2m)
node(308, -5.3308*in2m,  95.3394*in2m, 112.5833*in2m)
node(309, -5.3308*in2m,  95.3394*in2m, 114.0833*in2m)
node(310, -5.3308*in2m,  95.3394*in2m, 154.4167*in2m)
node(311, -5.3308*in2m,  95.3394*in2m, 155.9167*in2m)
node(312, -5.3308*in2m,  95.3394*in2m, 197.0000*in2m)
# purlin # 2 from North
node(401, 31.0077*in2m,  74.2796*in2m, -54.0000*in2m)
node(402, 31.0077*in2m,  74.2796*in2m, -12.9167*in2m)
node(403, 31.0077*in2m,  74.2796*in2m, -11.4167*in2m)
node(404, 31.0077*in2m,  74.2796*in2m, 28.9167*in2m)
node(405, 31.0077*in2m,  74.2796*in2m, 30.4167*in2m)
node(406, 31.0077*in2m,  74.2796*in2m, 70.7500*in2m)
node(407, 31.0077*in2m,  74.2796*in2m, 72.2500*in2m)
node(408, 31.0077*in2m,  74.2796*in2m, 112.5833*in2m)
node(409, 31.0077*in2m,  74.2796*in2m, 114.0833*in2m)
node(410, 31.0077*in2m,  74.2796*in2m, 154.4167*in2m)
node(411, 31.0077*in2m,  74.2796*in2m, 155.9167*in2m)
node(412, 31.0077*in2m,  74.2796*in2m, 197.0000*in2m)

# module edge # 1 from North
node(701, -23.5000*in2m, 105.8693*in2m, -54.0000*in2m)
node(702, -23.5000*in2m, 105.8693*in2m, -12.9167*in2m)
node(703, -23.5000*in2m, 105.8693*in2m, -11.4167*in2m)
node(704, -23.5000*in2m, 105.8693*in2m, 28.9167*in2m)
node(705, -23.5000*in2m, 105.8693*in2m, 30.4167*in2m)
node(706, -23.5000*in2m, 105.8693*in2m, 70.7500*in2m)
node(707, -23.5000*in2m, 105.8693*in2m, 72.2500*in2m)
node(708, -23.5000*in2m, 105.8693*in2m, 112.5833*in2m)
node(709, -23.5000*in2m, 105.8693*in2m, 114.0833*in2m)
node(710, -23.5000*in2m, 105.8693*in2m, 154.4167*in2m)
node(711, -23.5000*in2m, 105.8693*in2m, 155.9167*in2m)
node(712, -23.5000*in2m, 105.8693*in2m, 197.0000*in2m)
# module edge # 2 from North
node(801, 49.1770*in2m,  63.7497*in2m, -54.0000*in2m)
node(802, 49.1770*in2m,  63.7497*in2m, -12.9167*in2m)
node(803, 49.1770*in2m,  63.7497*in2m, -11.4167*in2m)
node(804, 49.1770*in2m,  63.7497*in2m, 28.9167*in2m)
node(805, 49.1770*in2m,  63.7497*in2m, 30.4167*in2m)
node(806, 49.1770*in2m,  63.7497*in2m, 70.7500*in2m)
node(807, 49.1770*in2m,  63.7497*in2m, 72.2500*in2m)
node(808, 49.1770*in2m,  63.7497*in2m, 112.5833*in2m)
node(809, 49.1770*in2m,  63.7497*in2m, 114.0833*in2m)
node(810, 49.1770*in2m,  63.7497*in2m, 154.4167*in2m)
node(811, 49.1770*in2m,  63.7497*in2m, 155.9167*in2m)
node(812, 49.1770*in2m,  63.7497*in2m, 197.0000*in2m)

# define BOUNDARY CONDITIONS---------------------------------------------------
fix(301, 1, 1, 1, 0, 0, 1);  #fix on twist need to be changed after switch to coordinate system that uses Z for vertical
fix(312, 1, 1, 1, 0, 0, 0);
fix(401, 1, 1, 1, 0, 0, 1);  
fix(412, 1, 1, 1, 0, 0, 0);

# define ELEMENTS--------------------------------------------------------------
postTransfTag = 1;
vecxz = [1.0, 0.0, 0.0];
geomTransf('Linear', postTransfTag, *vecxz);

rafterTransfTag = 2;
vecxz = [0.0, -1.0, 0.0];
geomTransf('Linear', rafterTransfTag, *vecxz);

purlinTransfTag = 3;
vecxz = [0.0 - 88.0, 92.25 - 41.25, 0.0]; #local z' direction (nodes 104 - 107)
geomTransf('Linear', purlinTransfTag, *vecxz);

ibTransfTag = 4;
vecxz = [0.0, 0.0, 1.0];
geomTransf('Linear', ibTransfTag, *vecxz);

ebTransfTag = 5;
vecxz = [1.0, 0.0, 0.0];
geomTransf('Linear', ebTransfTag, *vecxz);

# purlins
nPurlin1 = [301,302,303,304,305,306,307,308,309,310,311,312]; #nodes of purlin # 1
nPurlin2 = [401,402,403,404,405,406,407,408,409,410,411,412]; #nodes of purlin # 2
for i in range (0,11):
    # purlin # 1
    #                            elemID   nodeI  nodeJ
    element('elasticBeamColumn', i+300, *[nPurlin1[i], nPurlin1[i+1]], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, purlinTransfTag, '-mass', mass_pu);
    # purlin # 2
    element('elasticBeamColumn', i+400, *[nPurlin2[i], nPurlin2[i+1]], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, purlinTransfTag, '-mass', mass_pu);

# modules and module frames
for i in range (1,7):
    #                    elemID    node1      node2    node3    node4 counter-clockwise
    element('ShellMITC4',i+700,  *[700+2*i-1, 700+2*i, 300+2*i, 300+2*i-1], moduleSecTag)
    element('ShellMITC4',i+800,  *[300+2*i-1, 300+2*i, 400+2*i, 400+2*i-1], moduleSecTag)
    element('ShellMITC4',i+900,  *[400+2*i-1, 400+2*i, 800+2*i, 800+2*i-1], moduleSecTag)
    
    element('elasticBeamColumn', i+1400, *[700+2*i-1, 700+2*i], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', i+1500, *[800+2*i-1, 800+2*i], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
    
    element('elasticBeamColumn', i+1800, *[700+2*i-1, 300+2*i-1], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', i+1900, *[300+2*i-1, 400+2*i-1], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', i+2000, *[400+2*i-1, 800+2*i-1], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    
    element('elasticBeamColumn', i+2400, *[700+2*i, 300+2*i], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', i+2500, *[300+2*i, 400+2*i], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', i+2600, *[400+2*i, 800+2*i], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);

# render the model
#vfo.createODB(model="solarPanel")
vfo.plot_model()

# eigen analysis---------------------------------------------------------------
eigenValues = eigen(12);
omega = np.sqrt(eigenValues);
freq = omega/(2*math.pi);

vfo.plot_modeshape(modenumber=1, scale=1); #plot mode shape 1
vfo.plot_modeshape(modenumber=2, scale=1); #plot mode shape 2
vfo.plot_modeshape(modenumber=3, scale=1); #plot mode shape 3
vfo.plot_modeshape(modenumber=4, scale=1); #plot mode shape 4
vfo.plot_modeshape(modenumber=5, scale=1); #plot mode shape 5
vfo.plot_modeshape(modenumber=6, scale=1); #plot mode shape 6

# define loads-----------------------------------------------------------------
F = 1.0; 
timeSeries('Linear',1);
pattern('Plain', 1, 1);
load(801, *[0.0,  F, 0.0, 0.0, 0.0, 0.0]);

# Define RECORDERS ------------------------------------------------------------
recorder('Node', '-file', f'{dataDir}/ElasDispEndDB40.out', '-time', '-node', *[801], '-dof', *[1, 2, 3, 4, 5, 6,], 'disp');

# define ANALYSIS PARAMETERS---------------------------------------------------
constraints('Plain'); # how it handles boundary conditions
numberer('Plain');	   # renumber dof's to minimize band-width 
system('BandGeneral');# how to store and solve the system of equations in the analysis
test('NormDispIncr', 1.0e-08, 1000); # determine if convergence has been achieved at the end of an iteration step
#algorithm NewtonLineSearch;# use Newton's solution algorithm: updates tangent stiffness at every iteration
algorithm('Linear');
integrator('LoadControl', 0.1)
#integrator ArcLength 0.05 1.0; #arclength alpha
#Dincr = -0.01; #-0.00002
                                  #Node,  dof, 1st incr, Jd,  min,   max
#integrator('DisplacementControl', EndNode, 1,   Dincr,    1,  Dincr, -0.01);
analysis('Static');	# define type of analysis static or transient
analyze(100);
print('Finished')
wipe()
#------------------------------------------------------------------------------
# set finishTime [clock clicks -milliseconds];
# puts "Time taken: [expr ($finishTime-$startTime)/1000] sec"
# set systemTime [clock seconds] 
# puts "Finished Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"