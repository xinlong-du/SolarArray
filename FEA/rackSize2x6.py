# -----------------------------------------------------------------------------
# Solar PV rack 2x6 CS-400W
# Units: m, N, kg, s, N/m2, kg/m3
# Xinlong Du, 2022
#
# -----------------------------------------------------------------------------
# set systemTime [clock seconds] 
# puts "Starting Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"
# set startTime [clock clicks -milliseconds];
from opensees import *
import numpy as np
import matplotlib.pyplot as plt
import os

# SET UP ----------------------------------------------------------------------
wipe();
model('basic', '-ndm', 3, '-ndf', 6);
dataDir = 'Data';
#os.mkdir(dataDir);
in2m=0.0254; #convert inch to meter

# MATERIAL properties----------------------------------------------------------
E_mod = 2.0e11;		      #Steel Young's modulus
nu = 0.3;                 #Poisson's ratio
G_mod = E_mod/2./(1+nu);  #Shear modulus
rho_steel = 7850.0;       #mass density
rho_module = 7850.0;      #mass density

# Define  SECTIONS ------------------------------------------------------------
purlinSecTag = 1;
rafterSecTag = 2;
postSecTag = 3;
braceSecTag = 4;
moduleSecTag = 5;

# SECTION properties for purlin
A = 100.0;    #cross-sectional area
Iz = 10000.0; #second moment of area about the local z-axis
Iy = 10000.0; #second moment of area about the local y-axis
Jxx = 8424.0; #torsional moment of inertia of section
section('Elastic', purlinSecTag, E_mod, A, Iz, Iy, G_mod, Jxx);

# SECTION properties for rafter
A = 100.0;    #cross-sectional area
Iz = 10000.0; #second moment of area about the local z-axis
Iy = 10000.0; #second moment of area about the local y-axis
Jxx = 8424.0; #torsional moment of inertia of section
section('Elastic', rafterSecTag, E_mod, A, Iz, Iy, G_mod, Jxx);
    
# SECTION properties for post
A = 100.0;    #cross-sectional area
Iz = 10000.0; #second moment of area about the local z-axis
Iy = 10000.0; #second moment of area about the local y-axis
Jxx = 8424.0; #torsional moment of inertia of section
section('Elastic', postSecTag, E_mod, A, Iz, Iy, G_mod, Jxx);
    
# SECTION properties for brace
A = 100.0;    #cross-sectional area
Iz = 10000.0; #second moment of area about the local z-axis
Iy = 10000.0; #second moment of area about the local y-axis
Jxx = 8424.0; #torsional moment of inertia of section
section('Elastic', braceSecTag, E_mod, A, Iz, Iy, G_mod, Jxx);

# SECTION properties for module
h = 1.181*in2m; #depth of module
section('ElasticMembranePlateSection', moduleSecTag, E_mod, nu, h, rho_module)

# define NODES-----------------------------------------------------------------
# east side rack, north post
node(101, 0.0,           0.0,          0.0)
node(102, 0.0,           7*in2m,       0.0)
node(103, 0.0,           11*in2m,      0.0)
node(104, 0.0,           92.25*in2m,   0.0)
# east side rack, south post
node(105, 88*in2m,       0.0,          0.0)
node(106, 88*in2m,       7*in2m,       0.0)
node(107, 88*in2m,       41.25*in2m,   0.0)
# east side rack, rafter
node(108, -5.3308*in2m,  95.3394*in2m, 0.0)
node(109, 31.0077*in2m,  74.2796*in2m, 0.0)
node(110, 69.2423*in2m,  52.1209*in2m, 0.0)
node(111, 105.5808*in2m, 31.0611*in2m, 0.0)

# west side rack, north post
node(201, 0.0,           0.0,          143.0*in2m)
node(202, 0.0,           7*in2m,       143.0*in2m)
node(203, 0.0,           11*in2m,      143.0*in2m)
node(204, 0.0,           92.25*in2m,   143.0*in2m)
# west side rack, south post
node(205, 88*in2m,       0.0,          143.0*in2m)
node(206, 88*in2m,       7*in2m,       143.0*in2m)
node(207, 88*in2m,       41.25*in2m,   143.0*in2m)
# west side rack, rafter
node(208, -5.3308*in2m,  95.3394*in2m, 143.0*in2m)
node(209, 31.0077*in2m,  74.2796*in2m, 143.0*in2m)
node(210, 69.2423*in2m,  52.1209*in2m, 143.0*in2m)
node(211, 105.5808*in2m, 31.0611*in2m, 143.0*in2m)

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
# purlin # 3 from North
node(501, 69.2423*in2m,  52.1209*in2m, -54.0000*in2m)
node(502, 69.2423*in2m,  52.1209*in2m, -12.9167*in2m)
node(503, 69.2423*in2m,  52.1209*in2m, -11.4167*in2m)
node(504, 69.2423*in2m,  52.1209*in2m, 28.9167*in2m)
node(505, 69.2423*in2m,  52.1209*in2m, 30.4167*in2m)
node(506, 69.2423*in2m,  52.1209*in2m, 70.7500*in2m)
node(507, 69.2423*in2m,  52.1209*in2m, 72.2500*in2m)
node(508, 69.2423*in2m,  52.1209*in2m, 112.5833*in2m)
node(509, 69.2423*in2m,  52.1209*in2m, 114.0833*in2m)
node(510, 69.2423*in2m,  52.1209*in2m, 154.4167*in2m)
node(511, 69.2423*in2m,  52.1209*in2m, 155.9167*in2m)
node(512, 69.2423*in2m,  52.1209*in2m, 197.0000*in2m)
# purlin # 4 from North
node(601, 105.5808*in2m, 31.0611*in2m, -54.0000*in2m)
node(602, 105.5808*in2m, 31.0611*in2m, -12.9167*in2m)
node(603, 105.5808*in2m, 31.0611*in2m, -11.4167*in2m)
node(604, 105.5808*in2m, 31.0611*in2m, 28.9167*in2m)
node(605, 105.5808*in2m, 31.0611*in2m, 30.4167*in2m)
node(606, 105.5808*in2m, 31.0611*in2m, 70.7500*in2m)
node(607, 105.5808*in2m, 31.0611*in2m, 72.2500*in2m)
node(608, 105.5808*in2m, 31.0611*in2m, 112.5833*in2m)
node(609, 105.5808*in2m, 31.0611*in2m, 114.0833*in2m)
node(610, 105.5808*in2m, 31.0611*in2m, 154.4167*in2m)
node(611, 105.5808*in2m, 31.0611*in2m, 155.9167*in2m)
node(612, 105.5808*in2m, 31.0611*in2m, 197.0000*in2m)

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
# module edge # 3 from North
node(901, 51.0730*in2m,  62.6508*in2m, -54.0000*in2m)
node(902, 51.0730*in2m,  62.6508*in2m, -12.9167*in2m)
node(903, 51.0730*in2m,  62.6508*in2m, -11.4167*in2m)
node(904, 51.0730*in2m,  62.6508*in2m, 28.9167*in2m)
node(905, 51.0730*in2m,  62.6508*in2m, 30.4167*in2m)
node(906, 51.0730*in2m,  62.6508*in2m, 70.7500*in2m)
node(907, 51.0730*in2m,  62.6508*in2m, 72.2500*in2m)
node(908, 51.0730*in2m,  62.6508*in2m, 112.5833*in2m)
node(909, 51.0730*in2m,  62.6508*in2m, 114.0833*in2m)
node(910, 51.0730*in2m,  62.6508*in2m, 154.4167*in2m)
node(911, 51.0730*in2m,  62.6508*in2m, 155.9167*in2m)
node(912, 51.0730*in2m,  62.6508*in2m, 197.0000*in2m)
# module edge # 4 from North
node(1001, 123.7500*in2m, 20.5312*in2m, -54.0000*in2m)
node(1002, 123.7500*in2m, 20.5312*in2m, -12.9167*in2m)
node(1003, 123.7500*in2m, 20.5312*in2m, -11.4167*in2m)
node(1004, 123.7500*in2m, 20.5312*in2m, 28.9167*in2m)
node(1005, 123.7500*in2m, 20.5312*in2m, 30.4167*in2m)
node(1006, 123.7500*in2m, 20.5312*in2m, 70.7500*in2m)
node(1007, 123.7500*in2m, 20.5312*in2m, 72.2500*in2m)
node(1008, 123.7500*in2m, 20.5312*in2m, 112.5833*in2m)
node(1009, 123.7500*in2m, 20.5312*in2m, 114.0833*in2m)
node(1010, 123.7500*in2m, 20.5312*in2m, 154.4167*in2m)
node(1011, 123.7500*in2m, 20.5312*in2m, 155.9167*in2m)
node(1012, 123.7500*in2m, 20.5312*in2m, 197.0000*in2m)

# define BOUNDARY CONDITIONS---------------------------------------------------
fix(101, 1, 1, 1, 1, 1, 1);  
fix(105, 1, 1, 1, 1, 1, 1);
fix(201, 1, 1, 1, 1, 1, 1);  
fix(205, 1, 1, 1, 1, 1, 1);

# define ELEMENTS--------------------------------------------------------------
postTransfTag = 1;
vecxz=[0.0, 0.0, 1.0];
geomTransf('Linear', postTransfTag, *vecxz);
#**********transfTag need to be updated for other members except for posts*****
# east side rack, north post ID    nodeI nodeJ                            TBD for mass, release can be omitted for fixed BC
element('elasticBeamColumn', 101, *[101, 102], postSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 102, *[102, 103], postSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 103, *[103, 104], postSecTag, postTransfTag, 'mass', 0.0, '-releasez', 2, 'releasey', 2);
# east side rack, south post
element('elasticBeamColumn', 104, *[105, 106], postSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 105, *[106, 107], postSecTag, postTransfTag, 'mass', 0.0, '-releasez', 2, 'releasey', 2);
# east side rack, rafter
element('elasticBeamColumn', 106, *[108, 104], rafterSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 107, *[104, 109], rafterSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 108, *[109, 110], rafterSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 109, *[110, 107], rafterSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 110, *[107, 111], rafterSecTag, postTransfTag, 'mass', 0.0);
# east side rack, brace
element('elasticBeamColumn', 111, *[102, 106], braceSecTag, postTransfTag, 'mass', 0.0, '-releasez', 3, 'releasey', 3);
element('elasticBeamColumn', 112, *[103, 107], braceSecTag, postTransfTag, 'mass', 0.0, '-releasez', 3, 'releasey', 3);

# west side rack, north post ID    nodeI nodeJ                            TBD for mass, release can be omitted for fixed BC
element('elasticBeamColumn', 201, *[201, 202], postSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 202, *[202, 203], postSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 203, *[203, 204], postSecTag, postTransfTag, 'mass', 0.0, '-releasez', 2, 'releasey', 2);
# west side rack, south post
element('elasticBeamColumn', 204, *[205, 206], postSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 205, *[206, 207], postSecTag, postTransfTag, 'mass', 0.0, '-releasez', 2, 'releasey', 2);
# west side rack, rafter
element('elasticBeamColumn', 206, *[208, 204], rafterSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 207, *[204, 209], rafterSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 208, *[209, 210], rafterSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 209, *[210, 207], rafterSecTag, postTransfTag, 'mass', 0.0);
element('elasticBeamColumn', 210, *[207, 211], rafterSecTag, postTransfTag, 'mass', 0.0);
# west side rack, brace
element('elasticBeamColumn', 211, *[202, 206], braceSecTag, postTransfTag, 'mass', 0.0, '-releasez', 3, 'releasey', 3);
element('elasticBeamColumn', 212, *[203, 207], braceSecTag, postTransfTag, 'mass', 0.0, '-releasez', 3, 'releasey', 3);

# purlins
for i in range (1,12):
    # perlin # 1
    elemID = i+300;
    nodeI = i+300;
    nodeJ = i+301;
    element('elasticBeamColumn', elemID, *[nodeI, nodeJ], postSecTag, postTransfTag, 'mass', 0.0);
    # purlin # 2
    elemID = i+400;
    nodeI = i+400;
    nodeJ = i+401;
    element('elasticBeamColumn', elemID, *[nodeI, nodeJ], postSecTag, postTransfTag, 'mass', 0.0);
    # perlin # 3
    elemID = i+500;
    nodeI = i+500;
    nodeJ = i+501;
    element('elasticBeamColumn', elemID, *[nodeI, nodeJ], postSecTag, postTransfTag, 'mass', 0.0);
    # purlin # 4
    elemID = i+600;
    nodeI = i+600;
    nodeJ = i+601;
    element('elasticBeamColumn', elemID, *[nodeI, nodeJ], postSecTag, postTransfTag, 'mass', 0.0);
end

# define loads-----------------------------------------------------------------
F = 10.0;
P = 10000.0; 
timeSeries('Linear',1);
pattern('Plain', 1, 1);
load(MidNode, *[0.0,  F, 0.0, 0.0, 0.0, 0.0]);
load(EndNode, *[-P, 0.0, 0.0, 0.0, 0.0, 0.0]);

# Define RECORDERS ------------------------------------------------------------
recorder('Node', '-file', f'{dataDir}/ElasDispEndDB40.out', '-time', '-node', *[EndNode], '-dof', *[1, 2, 3, 4, 5, 6,], 'disp');
recorder('Node', '-file', f'{dataDir}/ElasDispMidDB40.out', '-time', '-node', *[MidNode], '-dof', *[1, 2, 3, 4, 5, 6,], 'disp');

# define ANALYSIS PARAMETERS---------------------------------------------------
constraints('Plain'); # how it handles boundary conditions
numberer('Plain');	   # renumber dof's to minimize band-width 
system('BandGeneral');# how to store and solve the system of equations in the analysis
test('NormDispIncr', 1.0e-08, 1000); # determine if convergence has been achieved at the end of an iteration step
#algorithm NewtonLineSearch;# use Newton's solution algorithm: updates tangent stiffness at every iteration
algorithm('Newton');
integrator('LoadControl', 0.01)
#integrator ArcLength 0.05 1.0; #arclength alpha
#Dincr = -0.01; #-0.00002
                                  #Node,  dof, 1st incr, Jd,  min,   max
#integrator('DisplacementControl', EndNode, 1,   Dincr,    1,  Dincr, -0.01);
analysis('Static');	# define type of analysis static or transient
analyze(1000);
print('Finished')

#------------------------------------------------------------------------------
# set finishTime [clock clicks -milliseconds];
# puts "Time taken: [expr ($finishTime-$startTime)/1000] sec"
# set systemTime [clock seconds] 
# puts "Finished Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"