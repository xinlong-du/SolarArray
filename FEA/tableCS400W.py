# -----------------------------------------------------------------------------
# Solar PV table (two 2x11 CS-400W)
# Units: m, N, kg, s, N/m2, kg/m3
# Xinlong Du, 2023
# -----------------------------------------------------------------------------
from openseespy.opensees import *
import numpy as np
import math

# visulization
import vfo.vfo as vfo

from plotFunctions import localForcePlot
from plotFunctions import globalDispPlot
from plotFunctions import localYdispPlot
from plotFunctions import springResPlot

#%% SET UP ----------------------------------------------------------------------
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
A_pu = 0.822*in2m**2;     #cross-sectional area
Iz_pu = 7.79*in2m**4;     #second moment of area about the local z-axis
Iy_pu = 0.674*in2m**4;    #second moment of area about the local y-axis
Jx_pu = 0.000954*in2m**4;  #torsional moment of inertia of section
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

# define springs---------------------------------------------------------------
# material for dispX-----------------------------------------------------------
Fy=1500.0;
E0=1.0e6;
b=0.0001;
uniaxialMaterial('Steel01', 1, Fy, E0, b)

E=1.95e7;
Fy=-1.0e6;
gap=-2.1e-3;
eta=0.99999;
uniaxialMaterial('ElasticPPGap', 2, E, Fy, gap, eta)

uniaxialMaterial('Parallel', 101, *[1,2])

# material for dispY-----------------------------------------------------------
Fy=4000.0;
E0=1.5e7;
b=0.0001;
uniaxialMaterial('Steel01', 3, Fy, E0, b)

E=4.0e5;
Eneg=1.95e8;
eta=0.0;
uniaxialMaterial('Elastic', 4, E, eta, Eneg)

uniaxialMaterial('Parallel', 102, *[3,4])

# material for dispZ-----------------------------------------------------------
Fy=1650.0;
E0=7.0e6;
b=0.002;
uniaxialMaterial('Steel01', 103, Fy, E0, b)

# material for rotX-----------------------------------------------------------
Fy=1.0e2;
E0=9.9e4;
b=0.1;
uniaxialMaterial('Steel01', 5, Fy, E0, b)

E=2.0e3;
Fy=1.0e7;
gap=0.0;
eta=0.99999;
uniaxialMaterial('ElasticPPGap', 6, E, Fy, gap, eta)

E=2.8e4;
Fy=-1.0e3;
gap=-0.0;
eta=0.99999;
uniaxialMaterial('ElasticPPGap', 7, E, Fy, gap, eta)

E=9.6e4;
uniaxialMaterial('Elastic', 8, E)

uniaxialMaterial('Parallel', 104, *[5,6,7,8])

# material for rotY-----------------------------------------------------------
Fy=80.0;
E0=8.0e3;
b=0.04;
uniaxialMaterial('Steel01', 9, Fy, E0, b)

E=1.6e3;
Fy=1.0e7;
gap=0.022;
eta=0.99999;
uniaxialMaterial('ElasticPPGap', 10, E, Fy, gap, eta)

E=1.6e3;
Fy=-1.0e7;
gap=-0.022;
eta=0.99999;
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

# define NODES-----------------------------------------------------------------
yRack=[0.0, 265.3600*in2m, 464.8600*in2m, 730.2200*in2m];
for i in range(1,5):
    # north post
    node(100*i+1,             0.0, yRack[i-1],          0.0)
    node(100*i+2,             0.0, yRack[i-1],       7*in2m)
    node(100*i+3,             0.0, yRack[i-1],      11*in2m)
    node(100*i+4,             0.0, yRack[i-1],   92.25*in2m)
    # south post
    node(100*i+5,        -88*in2m, yRack[i-1],          0.0)
    node(100*i+6,        -88*in2m, yRack[i-1],       7*in2m)
    node(100*i+7,        -88*in2m, yRack[i-1],   41.25*in2m)
    # rafter
    node(100*i+8,     5.3308*in2m, yRack[i-1], 95.3394*in2m)
    node(100*i+9,   -31.0077*in2m, yRack[i-1], 74.2796*in2m)
    node(100*i+10,  -69.2423*in2m, yRack[i-1], 52.1209*in2m)
    node(100*i+11, -105.5808*in2m, yRack[i-1], 31.0611*in2m)

# purlins and modules
for i in range (0,2):
    for j in range (0,22):
        node(501+400*i+2*j, (-123.7500+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (20.5313+43.2185*i)*in2m)
        node(502+400*i+2*j, (-123.7500+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (20.5313+43.2185*i)*in2m)
        node(601+400*i+2*j, (-105.5808+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (31.0611+43.2185*i)*in2m)
        node(1501+400*i+2*j,(-105.5808+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (31.0611+43.2185*i)*in2m)
        node(602+400*i+2*j, (-105.5808+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (31.0611+43.2185*i)*in2m)
        node(1502+400*i+2*j,(-105.5808+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (31.0611+43.2185*i)*in2m)
        node(701+400*i+2*j,  (-69.2423+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (52.1209+43.2185*i)*in2m)
        node(1601+400*i+2*j, (-69.2423+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (52.1209+43.2185*i)*in2m)
        node(702+400*i+2*j,  (-69.2423+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (52.1209+43.2185*i)*in2m)
        node(1602+400*i+2*j, (-69.2423+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (52.1209+43.2185*i)*in2m)
        node(801+400*i+2*j,  (-51.0730+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (62.6508+43.2185*i)*in2m)
        node(802+400*i+2*j,  (-51.0730+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (62.6508+43.2185*i)*in2m)
        node(1401+400*i+2*j, (-87.4115+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (41.5910+43.2185*i)*in2m)
        node(1402+400*i+2*j, (-87.4115+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (41.5910+43.2185*i)*in2m)

# intersection of external braces
node(1301, 0.0, 132.6800*in2m, 51.6250*in2m)
node(1302, 0.0, 597.5400*in2m, 51.6250*in2m)

# define BOUNDARY CONDITIONS---------------------------------------------------
fix(101, 1, 1, 1, 1, 1, 1);  
fix(105, 1, 1, 1, 1, 1, 1);
fix(201, 1, 1, 1, 1, 1, 1);  
fix(205, 1, 1, 1, 1, 1, 1);
fix(301, 1, 1, 1, 1, 1, 1);  
fix(305, 1, 1, 1, 1, 1, 1);
fix(401, 1, 1, 1, 1, 1, 1);  
fix(405, 1, 1, 1, 1, 1, 1);

# define ELEMENTS--------------------------------------------------------------
postTransfTag = 1;
vecxz = [1.0, 0.0, 0.0];
geomTransf('Corotational', postTransfTag, *vecxz);

rafterTransfTag = 2;
vecxz = [0.0, 0.0, -1.0];
geomTransf('Corotational', rafterTransfTag, *vecxz);

purlinTransfTag = 3;
vecxz = [0.0-(-88.0), 0.0, 92.25-41.25]; #local z' direction (nodes 104 - 107)
geomTransf('Corotational', purlinTransfTag, *vecxz);

ibTransfTag = 4;
vecxz = [0.0, 1.0, 0.0];
geomTransf('Corotational', ibTransfTag, *vecxz);

ebTransfTag = 5;
vecxz = [1.0, 0.0, 0.0];
geomTransf('Corotational', ebTransfTag, *vecxz);

vecx1 = [0.0,  1.0, 0]; #local x-axis for spring, module frame on the left side of the bolt
vecx2 = [0.0, -1.0, 0]; #local x-axis for spring, module frame on the right side of the bolt
vecyp = [-40.0211, 0.0000, 69.0560]; #vector in the local x-y plane for the element

for i in range(0,4):
    # north post                 ID           nodeI      nodeJ                            TBD for mass, release can be omitted for fixed BC
    element('elasticBeamColumn', 101+100*i, *[101+100*i, 102+100*i], A_po, Es, Gs, Jx_po, Iy_po, Iz_po, postTransfTag, '-mass', mass_po);
    element('elasticBeamColumn', 102+100*i, *[102+100*i, 103+100*i], A_po, Es, Gs, Jx_po, Iy_po, Iz_po, postTransfTag, '-mass', mass_po);
    element('elasticBeamColumn', 103+100*i, *[103+100*i, 104+100*i], A_po, Es, Gs, Jx_po, Iy_po, Iz_po, postTransfTag, '-mass', mass_po, '-releasez', 2, 'releasey', 2);
    # south post
    element('elasticBeamColumn', 104+100*i, *[105+100*i, 106+100*i], A_po, Es, Gs, Jx_po, Iy_po, Iz_po, postTransfTag, '-mass', mass_po);
    element('elasticBeamColumn', 105+100*i, *[106+100*i, 107+100*i], A_po, Es, Gs, Jx_po, Iy_po, Iz_po, postTransfTag, '-mass', mass_po, '-releasez', 2, 'releasey', 2);
    # rafter
    element('elasticBeamColumn', 106+100*i, *[108+100*i, 104+100*i], A_r, Es, Gs, Jx_r, Iy_r, Iz_r, rafterTransfTag, '-mass', mass_r);
    element('elasticBeamColumn', 107+100*i, *[104+100*i, 109+100*i], A_r, Es, Gs, Jx_r, Iy_r, Iz_r, rafterTransfTag, '-mass', mass_r);
    element('elasticBeamColumn', 108+100*i, *[109+100*i, 110+100*i], A_r, Es, Gs, Jx_r, Iy_r, Iz_r, rafterTransfTag, '-mass', mass_r);
    element('elasticBeamColumn', 109+100*i, *[110+100*i, 107+100*i], A_r, Es, Gs, Jx_r, Iy_r, Iz_r, rafterTransfTag, '-mass', mass_r);
    element('elasticBeamColumn', 110+100*i, *[107+100*i, 111+100*i], A_r, Es, Gs, Jx_r, Iy_r, Iz_r, rafterTransfTag, '-mass', mass_r);
    # internal brace
    element('elasticBeamColumn', 111+100*i, *[102+100*i, 106+100*i], A_ib, Es, Gs, Jx_ib, Iy_ib, Iz_ib, ibTransfTag, '-mass', mass_ib, '-releasez', 3, 'releasey', 3);
    element('elasticBeamColumn', 112+100*i, *[103+100*i, 107+100*i], A_ib, Es, Gs, Jx_ib, Iy_ib, Iz_ib, ibTransfTag, '-mass', mass_ib, '-releasez', 3, 'releasey', 3);

# purlins
nPurlin=[[0]*48]*4; #nodes of purlins
rowPurlin=[1501,1601,1901,2001];
nRafter=[11,10,9,8];
for i in range (0,4):
    nPurlin[i] = list(range(rowPurlin[i],rowPurlin[i]+44));
    nPurlin[i].insert(39,400+nRafter[i])
    nPurlin[i].insert(27,300+nRafter[i])
    nPurlin[i].insert(17,200+nRafter[i])
    nPurlin[i].insert(5,100+nRafter[i])

for i in range (0,4):
    for j in range (0,23):
        #                            elemID         nodeI          nodeJ
        element('elasticBeamColumn', i*100+501+j, *[nPurlin[i][j], nPurlin[i][j+1]], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, purlinTransfTag, '-mass', mass_pu);
        element('elasticBeamColumn', i*100+501+j+24, *[nPurlin[i][j+24], nPurlin[i][j+1+24]], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, purlinTransfTag, '-mass', mass_pu);

# modules and module frames
for i in range (0,2):
    for j in range (0,22):
        #                    elemID               node1          node2          node3          node4 counter-clockwise
        element('ShellMITC4',(18*i+1)*1000+j+1,  *[501+i*400+j*2,  601+i*400+j*2,  602+i*400+j*2,  502+i*400+j*2], moduleSecTag)
        element('ShellMITC4',(18*i+2)*1000+j+1,  *[601+i*400+j*2, 1401+i*400+j*2, 1402+i*400+j*2,  602+i*400+j*2], moduleSecTag)
        element('ShellMITC4',(18*i+3)*1000+j+1,  *[1401+i*400+j*2, 701+i*400+j*2,  702+i*400+j*2, 1402+i*400+j*2], moduleSecTag)
        element('ShellMITC4',(18*i+4)*1000+j+1,  *[701+i*400+j*2,  801+i*400+j*2,  802+i*400+j*2,  702+i*400+j*2], moduleSecTag)
    
        element('elasticBeamColumn', (18*i+5)*1000+j+1,  *[801+i*400+j*2,  701+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (18*i+6)*1000+j+1,  *[701+i*400+j*2, 1401+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (18*i+7)*1000+j+1,  *[1401+i*400+j*2, 601+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (18*i+8)*1000+j+1,  *[601+i*400+j*2,  501+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (18*i+9)*1000+j+1,  *[802+i*400+j*2,  702+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (18*i+10)*1000+j+1, *[702+i*400+j*2, 1402+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (18*i+11)*1000+j+1, *[1402+i*400+j*2, 602+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (18*i+12)*1000+j+1, *[602+i*400+j*2,  502+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (18*i+13)*1000+j+1, *[801+i*400+j*2,  802+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (18*i+14)*1000+j+1, *[501+i*400+j*2,  502+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
        element('zeroLength', (18*i+15)*1000+j+1, *[1501+i*400+j*2, 601+i*400+j*2], '-mat', *[101,102,103,104,105,106], '-dir', *[1,2,3,4,5,6], '-orient', *vecx1, *vecyp);
        element('zeroLength', (18*i+16)*1000+j+1, *[1502+i*400+j*2, 602+i*400+j*2], '-mat', *[101,102,103,104,105,106], '-dir', *[1,2,3,4,5,6], '-orient', *vecx2, *vecyp);
        element('zeroLength', (18*i+17)*1000+j+1, *[1601+i*400+j*2, 701+i*400+j*2], '-mat', *[101,102,103,104,105,106], '-dir', *[1,2,3,4,5,6], '-orient', *vecx1, *vecyp);
        element('zeroLength', (18*i+18)*1000+j+1, *[1602+i*400+j*2, 702+i*400+j*2], '-mat', *[101,102,103,104,105,106], '-dir', *[1,2,3,4,5,6], '-orient', *vecx2, *vecyp);
        
# external braces
for i in range(0,2):
    element('elasticBeamColumn', 37000+1000*i+1, *[(i+1)*100+3, 1301], A_eb, Es, Gs, Jx_eb, Iy_eb, Iz_eb, ebTransfTag, '-mass', mass_eb, '-releasez', 1, 'releasey', 1);
    element('elasticBeamColumn', 37000+1000*i+2, *[(i+1)*100+4, 1301], A_eb, Es, Gs, Jx_eb, Iy_eb, Iz_eb, ebTransfTag, '-mass', mass_eb, '-releasez', 1, 'releasey', 1);
    element('elasticBeamColumn', 37000+1000*i+3, *[(i+3)*100+3, 1302], A_eb, Es, Gs, Jx_eb, Iy_eb, Iz_eb, ebTransfTag, '-mass', mass_eb, '-releasez', 1, 'releasey', 1);
    element('elasticBeamColumn', 37000+1000*i+4, *[(i+3)*100+4, 1302], A_eb, Es, Gs, Jx_eb, Iy_eb, Iz_eb, ebTransfTag, '-mass', mass_eb, '-releasez', 1, 'releasey', 1);

allNodeTags=getNodeTags();
alleleTags=getEleTags();

# render the model
vfo.createODB(model="tableCS400W", loadcase="windDir0", Nmodes=6, deltaT=1)
vfo.plot_model()

# eigen ANALYSIS---------------------------------------------------------------
eigenValues = eigen(12);
omega = np.sqrt(eigenValues);
freq = omega/(2*math.pi);

# vfo.plot_modeshape(modenumber=1, scale=5); #plot mode shape 1
# vfo.plot_modeshape(modenumber=2, scale=5); #plot mode shape 2
# vfo.plot_modeshape(modenumber=3, scale=5); #plot mode shape 3
# vfo.plot_modeshape(modenumber=4, scale=5); #plot mode shape 4
# vfo.plot_modeshape(modenumber=5, scale=5); #plot mode shape 5
# vfo.plot_modeshape(modenumber=6, scale=5); #plot mode shape 6

# vfo.plot_modeshape(modenumber=7, scale=5); #plot mode shape 7
# vfo.plot_modeshape(modenumber=8, scale=5); #plot mode shape 8
# vfo.plot_modeshape(modenumber=9, scale=5); #plot mode shape 9
# vfo.plot_modeshape(modenumber=10, scale=5); #plot mode shape 10
# vfo.plot_modeshape(modenumber=11, scale=5); #plot mode shape 11
# vfo.plot_modeshape(modenumber=12, scale=5); #plot mode shape 12

#%% load wind tunnel test DATA
import h5py
filename = "../../../RWDI/Wind Tunnel Data/tilt_n30deg.hdf5"

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
U=47.0;
dt=dtNorm*L/U;
rho_air=1.226;
p=0.5*rho_air*U*U*Cp;
x=L*np.array([0.125/2+0.25/2,0.25,0.25,0.25/2+0.125/2]);
y=L*np.array([0.125/2+0.5/2,0.5/2+0.75/2,0.75/2+1/2,1/2+1.25/2,1.25/2+1/2,1/2+0.75/2,0.75/2+0.125/2]);
A_trib=np.outer(x, y);
A_trib=np.reshape(A_trib,(1,28),order='F');
#A_trib=np.repeat(A_trib,np.shape(p)[0],axis=0);
Force=np.multiply(p,A_trib);
Force=Force.T.tolist()

nodesTapEd=[[1201,1202,1203,1801,1802,1803],[1801,1802,1803,901,902,903],[801,802,803,1401,1402,1403],[1401,1402,1403,501,502,503],
            list(range(1204,1209))+list(range(1804,1809)),list(range(1804,1809))+list(range(904,909)),list(range(804,809))+list(range(1404,1409)),list(range(1404,1409))+list(range(504,509)),
            list(range(1209,1216))+list(range(1809,1816)),list(range(1809,1816))+list(range(909,916)),list(range(809,816))+list(range(1409,1416)),list(range(1409,1416))+list(range(509,516)),
            list(range(1216,1225))+list(range(1816,1825)),list(range(1816,1825))+list(range(916,925)),list(range(816,825))+list(range(1416,1425)),list(range(1416,1425))+list(range(516,525)),
            list(range(1225,1234))+list(range(1825,1834)),list(range(1825,1834))+list(range(925,934)),list(range(825,834))+list(range(1425,1434)),list(range(1425,1434))+list(range(525,534)),
            list(range(1234,1241))+list(range(1834,1841)),list(range(1834,1841))+list(range(934,941)),list(range(834,841))+list(range(1434,1441)),list(range(1434,1441))+list(range(534,541)),
            list(range(1241,1245))+list(range(1841,1845)),list(range(1841,1845))+list(range(941,945)),list(range(841,845))+list(range(1441,1445)),list(range(1441,1445))+list(range(541,545))];
nodesTapIn=[[1101,1102,1103],[1001,1002,1003],[701,702,703],[601,602,603],
            list(range(1104,1109)),list(range(1004,1009)),list(range(704,709)),list(range(604,609)),
            list(range(1109,1116)),list(range(1009,1016)),list(range(709,716)),list(range(609,616)),
            list(range(1116,1125)),list(range(1016,1025)),list(range(716,725)),list(range(616,625)),
            list(range(1125,1134)),list(range(1025,1034)),list(range(725,734)),list(range(625,634)),
            list(range(1134,1141)),list(range(1034,1041)),list(range(734,741)),list(range(634,641)),
            list(range(1141,1145)),list(range(1041,1045)),list(range(741,745)),list(range(641,645))];
for i in range(0,28):
    timeSeries('Path',i,'-dt',dt,'-values',*Force[i],'-prependZero');
    pattern('Plain',i,i);
    fact=0.25/len(nodesTapEd[27-i]);
    for j in nodesTapEd[27-i]:
        load(j, *[fact*math.sin(30/180*math.pi), 0.0, -fact*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    fact=0.5/len(nodesTapIn[27-i]);
    for j in nodesTapIn[27-i]:
        load(j, *[fact*math.sin(30/180*math.pi), 0.0, -fact*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);

# define RECORDERS ------------------------------------------------------------
nodeRec=list(range(1001,1023))+list(range(1101,1123))+list(range(1801,1823));
eleRec=list(range(701,724))+list(range(801,824));
springRec=list(range(15001,15023))+list(range(16001,16023))+list(range(17001,17023))+list(range(18001,18023))+list(range(33001,33023))+list(range(34001,34023))+list(range(35001,35023))+list(range(36001,36023));
recorder('Node', '-file', f'{dataDir}/tableCS400Wnodes.out', '-time', '-node', *nodeRec, '-dof', *[1, 2, 3, 4, 5, 6,], 'disp');
recorder('Element', '-file', f'{dataDir}/tableCS400Weles.out', '-time', '-ele', *eleRec, 'localForces');
recorder('Element', '-file', f'{dataDir}/tableCS400Wspring.out', '-time', '-ele', *[15001], 'deformation');
recorder('Element', '-file', f'{dataDir}/tableCS400WlocalForces.out', '-time', '-ele', *[15001], 'localForces');
recorder('Element', '-file', f'{dataDir}/tableCS400WbasicStiffness.out', '-time', '-ele', *[15001], 'basicStiffness');
recorder('Element', '-file', f'{dataDir}/tableCS400WdefANDfor.out', '-time', '-ele', *springRec, 'deformationsANDforces');

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
ok = analyze(1000, 0.02);
print('Finished')

#%% output forces on joints at the last time step, used for verification-------
# element resisting forces for purlins
ef813end=eleForce(813);
ef813endLoc=eleResponse(813, 'localForces')
ef814end=eleForce(814);
ef814endLoc=eleResponse(814, 'localForces')
nf1113end=np.array(ef813endLoc[6:12])+np.array(ef814endLoc[0:6]);

# nodal displacement
nd1001end=nodeDisp(1001);
nd1101end=nodeDisp(1101);
nd1801end=nodeDisp(1801);
nd1002end=nodeDisp(1002);
nd1102end=nodeDisp(1102);
nd1802end=nodeDisp(1802);
nd1003end=nodeDisp(1003);
nd1103end=nodeDisp(1103);
nd1803end=nodeDisp(1803);
nd1004end=nodeDisp(1004);
nd1104end=nodeDisp(1104);
nd1804end=nodeDisp(1804);

nd1011end=nodeDisp(1011);
nd1111end=nodeDisp(1111);
nd1811end=nodeDisp(1811);
nd1012end=nodeDisp(1012);
nd1112end=nodeDisp(1112);
nd1812end=nodeDisp(1812);
nd1013end=nodeDisp(1013);
nd1113end=nodeDisp(1113);
nd1813end=nodeDisp(1813);
nd1014end=nodeDisp(1014);
nd1114end=nodeDisp(1114);
nd1814end=nodeDisp(1814);

wipe()
#%% defomed shape and animation------------------------------------------------
vfo.plot_deformedshape(model="tableCS400W", loadcase="windDir0", scale=20)
#ani = vfo.animate_deformedshape(model="tableCS400W", loadcase="windDir0", speedup=4, scale=50, gifname="tableCS400W_Dynamic")

#%% plot response of springs
file_name='./Data/tableCS400WdefANDfor.out';
springRes=np.loadtxt(file_name);
for i in range(len(springRec)):
    springResPlot(springRes[:,i*12+1:i*12+13],str(springRec[i]));

#%% calculate time series of forces on joints----------------------------------
file_name = './Data/tableCS400Weles.out'
eleForces = np.loadtxt(file_name)
ef813=eleForces[:,35*12+1:36*12+1];
ef814=eleForces[:,36*12+1:37*12+1];
nf1113=ef813[:,6:12]+ef814[:,0:6];

#%% calculate time series of dispalcements-------------------------------------
file_name = './Data/tableCS400Wnodes.out'
nodeDisps = np.loadtxt(file_name)
nd1001=nodeDisps[:,nodeRec.index(1001)*6+1:(nodeRec.index(1001)+1)*6+1];
nd1101=nodeDisps[:,nodeRec.index(1101)*6+1:(nodeRec.index(1101)+1)*6+1];
nd1801=nodeDisps[:,nodeRec.index(1801)*6+1:(nodeRec.index(1801)+1)*6+1];
nd1002=nodeDisps[:,nodeRec.index(1002)*6+1:(nodeRec.index(1002)+1)*6+1];
nd1102=nodeDisps[:,nodeRec.index(1102)*6+1:(nodeRec.index(1102)+1)*6+1];
nd1802=nodeDisps[:,nodeRec.index(1802)*6+1:(nodeRec.index(1802)+1)*6+1];
nd1003=nodeDisps[:,nodeRec.index(1003)*6+1:(nodeRec.index(1003)+1)*6+1];
nd1103=nodeDisps[:,nodeRec.index(1103)*6+1:(nodeRec.index(1103)+1)*6+1];
nd1803=nodeDisps[:,nodeRec.index(1803)*6+1:(nodeRec.index(1803)+1)*6+1];
nd1004=nodeDisps[:,nodeRec.index(1004)*6+1:(nodeRec.index(1004)+1)*6+1];
nd1104=nodeDisps[:,nodeRec.index(1104)*6+1:(nodeRec.index(1104)+1)*6+1];
nd1804=nodeDisps[:,nodeRec.index(1804)*6+1:(nodeRec.index(1804)+1)*6+1];

nd1011=nodeDisps[:,nodeRec.index(1011)*6+1:(nodeRec.index(1011)+1)*6+1];
nd1111=nodeDisps[:,nodeRec.index(1111)*6+1:(nodeRec.index(1111)+1)*6+1];
nd1811=nodeDisps[:,nodeRec.index(1811)*6+1:(nodeRec.index(1811)+1)*6+1];
nd1012=nodeDisps[:,nodeRec.index(1012)*6+1:(nodeRec.index(1012)+1)*6+1];
nd1112=nodeDisps[:,nodeRec.index(1112)*6+1:(nodeRec.index(1112)+1)*6+1];
nd1812=nodeDisps[:,nodeRec.index(1812)*6+1:(nodeRec.index(1812)+1)*6+1];
nd1013=nodeDisps[:,nodeRec.index(1013)*6+1:(nodeRec.index(1013)+1)*6+1];
nd1113=nodeDisps[:,nodeRec.index(1113)*6+1:(nodeRec.index(1113)+1)*6+1];
nd1813=nodeDisps[:,nodeRec.index(1813)*6+1:(nodeRec.index(1813)+1)*6+1];
nd1014=nodeDisps[:,nodeRec.index(1014)*6+1:(nodeRec.index(1014)+1)*6+1];
nd1114=nodeDisps[:,nodeRec.index(1114)*6+1:(nodeRec.index(1114)+1)*6+1];
nd1814=nodeDisps[:,nodeRec.index(1814)*6+1:(nodeRec.index(1814)+1)*6+1];

nd1001LocY=nd1001[:,2]*math.cos(30/180*math.pi)-nd1001[:,0]*math.sin(30/180*math.pi);
nd1101LocY=nd1101[:,2]*math.cos(30/180*math.pi)-nd1101[:,0]*math.sin(30/180*math.pi);
nd1801LocY=nd1801[:,2]*math.cos(30/180*math.pi)-nd1801[:,0]*math.sin(30/180*math.pi);
nd1002LocY=nd1002[:,2]*math.cos(30/180*math.pi)-nd1002[:,0]*math.sin(30/180*math.pi);
nd1102LocY=nd1102[:,2]*math.cos(30/180*math.pi)-nd1102[:,0]*math.sin(30/180*math.pi);
nd1802LocY=nd1802[:,2]*math.cos(30/180*math.pi)-nd1802[:,0]*math.sin(30/180*math.pi);
nd1003LocY=nd1003[:,2]*math.cos(30/180*math.pi)-nd1003[:,0]*math.sin(30/180*math.pi);
nd1103LocY=nd1103[:,2]*math.cos(30/180*math.pi)-nd1103[:,0]*math.sin(30/180*math.pi);
nd1803LocY=nd1803[:,2]*math.cos(30/180*math.pi)-nd1803[:,0]*math.sin(30/180*math.pi);
nd1004LocY=nd1004[:,2]*math.cos(30/180*math.pi)-nd1004[:,0]*math.sin(30/180*math.pi);
nd1104LocY=nd1104[:,2]*math.cos(30/180*math.pi)-nd1104[:,0]*math.sin(30/180*math.pi);
nd1804LocY=nd1804[:,2]*math.cos(30/180*math.pi)-nd1804[:,0]*math.sin(30/180*math.pi);

nd1011LocY=nd1011[:,2]*math.cos(30/180*math.pi)-nd1011[:,0]*math.sin(30/180*math.pi);
nd1111LocY=nd1111[:,2]*math.cos(30/180*math.pi)-nd1111[:,0]*math.sin(30/180*math.pi);
nd1811LocY=nd1811[:,2]*math.cos(30/180*math.pi)-nd1811[:,0]*math.sin(30/180*math.pi);
nd1012LocY=nd1012[:,2]*math.cos(30/180*math.pi)-nd1012[:,0]*math.sin(30/180*math.pi);
nd1112LocY=nd1112[:,2]*math.cos(30/180*math.pi)-nd1112[:,0]*math.sin(30/180*math.pi);
nd1812LocY=nd1812[:,2]*math.cos(30/180*math.pi)-nd1812[:,0]*math.sin(30/180*math.pi);
nd1013LocY=nd1013[:,2]*math.cos(30/180*math.pi)-nd1013[:,0]*math.sin(30/180*math.pi);
nd1113LocY=nd1113[:,2]*math.cos(30/180*math.pi)-nd1113[:,0]*math.sin(30/180*math.pi);
nd1813LocY=nd1813[:,2]*math.cos(30/180*math.pi)-nd1813[:,0]*math.sin(30/180*math.pi);
nd1014LocY=nd1014[:,2]*math.cos(30/180*math.pi)-nd1014[:,0]*math.sin(30/180*math.pi);
nd1114LocY=nd1114[:,2]*math.cos(30/180*math.pi)-nd1114[:,0]*math.sin(30/180*math.pi);
nd1814LocY=nd1814[:,2]*math.cos(30/180*math.pi)-nd1814[:,0]*math.sin(30/180*math.pi);

#%% plots
timeVec=nodeDisps[:,0];
localForcePlot(nodeDisps[:,0],nf1113,'1113')
globalDispPlot(timeVec,nd1113,'1113')

localYdispPlot(timeVec,nd1001LocY,nd1801LocY,nd1101LocY,'1001','1801','1101')
localYdispPlot(timeVec,nd1002LocY,nd1802LocY,nd1102LocY,'1002','1802','1102')
localYdispPlot(timeVec,nd1003LocY,nd1803LocY,nd1103LocY,'1003','1803','1103')
localYdispPlot(timeVec,nd1004LocY,nd1804LocY,nd1104LocY,'1004','1804','1104')
localYdispPlot(timeVec,nd1011LocY,nd1811LocY,nd1111LocY,'1011','1811','1111')
localYdispPlot(timeVec,nd1012LocY,nd1812LocY,nd1112LocY,'1012','1812','1112')
localYdispPlot(timeVec,nd1013LocY,nd1813LocY,nd1113LocY,'1013','1813','1113')
localYdispPlot(timeVec,nd1014LocY,nd1814LocY,nd1114LocY,'1014','1814','1114')

#%% temporary, modify this after simplify the storage of nodal displacements
import matplotlib.pyplot as plt
big_fig_size = (6,10);
plt_line_width = 0.5; 
fig_font_size = 8;

fig = plt.figure(figsize=(6,10))
ax0 = fig.add_subplot(611)
ax1 = fig.add_subplot(612)
ax2 = fig.add_subplot(613)
ax3 = fig.add_subplot(614)
ax4 = fig.add_subplot(615)
ax5 = fig.add_subplot(616)
plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
ax0.tick_params(direction="in")
ax1.tick_params(direction="in")
ax2.tick_params(direction="in")
ax3.tick_params(direction="in")
ax4.tick_params(direction="in")
ax5.tick_params(direction="in")
ax0.plot(timeVec,(nd1012LocY-nd1011LocY)*39.3701, linewidth=plt_line_width)
ax1.plot(timeVec,(nd1812LocY-nd1811LocY)*39.3701, linewidth=plt_line_width)
ax2.plot(timeVec,(nd1112LocY-nd1111LocY)*39.3701, linewidth=plt_line_width)
ax3.plot(timeVec,(nd1013LocY-nd1014LocY)*39.3701, linewidth=plt_line_width)
ax4.plot(timeVec,(nd1813LocY-nd1814LocY)*39.3701, linewidth=plt_line_width)
ax5.plot(timeVec,(nd1113LocY-nd1114LocY)*39.3701, linewidth=plt_line_width)
ax0.set_ylabel('N1012 - N1011 (in)',fontsize=fig_font_size)
ax1.set_ylabel('N1812 - N1811 (in)',fontsize=fig_font_size)
ax2.set_ylabel('N1112 - N1111 (in)',fontsize=fig_font_size)
ax3.set_ylabel('N1013 - N1014 (in)',fontsize=fig_font_size)
ax4.set_ylabel('N1813 - N1814 (in)',fontsize=fig_font_size)
ax5.set_ylabel('N1113 - N1114 (in)',fontsize=fig_font_size)
ax5.set_xlabel('Time (s)',fontsize=fig_font_size)
plt.savefig('./Data/nodeDispHorMidLocY.tif', transparent=False, bbox_inches='tight', dpi=100)

fig = plt.figure(figsize=(6,10))
ax0 = fig.add_subplot(611)
ax1 = fig.add_subplot(612)
ax2 = fig.add_subplot(613)
ax3 = fig.add_subplot(614)
ax4 = fig.add_subplot(615)
ax5 = fig.add_subplot(616)
plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
ax0.tick_params(direction="in")
ax1.tick_params(direction="in")
ax2.tick_params(direction="in")
ax3.tick_params(direction="in")
ax4.tick_params(direction="in")
ax5.tick_params(direction="in")
ax0.plot(timeVec,(nd1002LocY-nd1001LocY)*39.3701, linewidth=plt_line_width)
ax1.plot(timeVec,(nd1802LocY-nd1801LocY)*39.3701, linewidth=plt_line_width)
ax2.plot(timeVec,(nd1102LocY-nd1101LocY)*39.3701, linewidth=plt_line_width)
ax3.plot(timeVec,(nd1003LocY-nd1004LocY)*39.3701, linewidth=plt_line_width)
ax4.plot(timeVec,(nd1803LocY-nd1804LocY)*39.3701, linewidth=plt_line_width)
ax5.plot(timeVec,(nd1103LocY-nd1104LocY)*39.3701, linewidth=plt_line_width)
ax0.set_ylabel('N1002 - N1001 (in)',fontsize=fig_font_size)
ax1.set_ylabel('N1802 - N1801 (in)',fontsize=fig_font_size)
ax2.set_ylabel('N1102 - N1101 (in)',fontsize=fig_font_size)
ax3.set_ylabel('N1003 - N1004 (in)',fontsize=fig_font_size)
ax4.set_ylabel('N1803 - N1804 (in)',fontsize=fig_font_size)
ax5.set_ylabel('N1103 - N1104 (in)',fontsize=fig_font_size)
ax5.set_xlabel('Time (s)',fontsize=fig_font_size)
plt.savefig('./Data/nodeDispHorEdgeLocY.tif', transparent=False, bbox_inches='tight', dpi=100)