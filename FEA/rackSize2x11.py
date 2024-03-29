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

# define NODES-----------------------------------------------------------------
yRack=[0.0, 265.3600*in2m];
for i in range(1,3):
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
    for j in range (0,11):
        node(501+400*i+2*j, (-123.7500+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (20.5313+43.2185*i)*in2m)
        node(502+400*i+2*j, (-123.7500+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (20.5313+43.2185*i)*in2m)
        node(601+400*i+2*j, (-105.5808+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (31.0611+43.2185*i)*in2m)
        node(602+400*i+2*j, (-105.5808+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (31.0611+43.2185*i)*in2m)
        node(701+400*i+2*j,  (-69.2423+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (52.1209+43.2185*i)*in2m)
        node(702+400*i+2*j,  (-69.2423+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (52.1209+43.2185*i)*in2m)
        node(801+400*i+2*j,  (-51.0730+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (62.6508+43.2185*i)*in2m)
        node(802+400*i+2*j,  (-51.0730+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (62.6508+43.2185*i)*in2m)
        node(1401+400*i+2*j, (-87.4115+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (41.5910+43.2185*i)*in2m)
        node(1402+400*i+2*j, (-87.4115+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (41.5910+43.2185*i)*in2m)

# intersection of external braces
node(1301, 0.0, 132.6800*in2m, 51.6250*in2m)

# define BOUNDARY CONDITIONS---------------------------------------------------
fix(101, 1, 1, 1, 1, 1, 1);  
fix(105, 1, 1, 1, 1, 1, 1);
fix(201, 1, 1, 1, 1, 1, 1);  
fix(205, 1, 1, 1, 1, 1, 1);

# define ELEMENTS--------------------------------------------------------------
postTransfTag = 1;
vecxz = [1.0, 0.0, 0.0];
geomTransf('Linear', postTransfTag, *vecxz);

rafterTransfTag = 2;
vecxz = [0.0, 0.0, -1.0];
geomTransf('Linear', rafterTransfTag, *vecxz);

purlinTransfTag = 3;
vecxz = [0.0-(-88.0), 0.0, 92.25-41.25]; #local z' direction (nodes 104 - 107)
geomTransf('Linear', purlinTransfTag, *vecxz);

ibTransfTag = 4;
vecxz = [0.0, 1.0, 0.0];
geomTransf('Linear', ibTransfTag, *vecxz);

ebTransfTag = 5;
vecxz = [1.0, 0.0, 0.0];
geomTransf('Linear', ebTransfTag, *vecxz);

for i in range(0,2):
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
rowPurlin=[601,701,1001,1101];
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

# modules and module frames
for i in range (0,2):
    for j in range (0,11):
        #                    elemID               node1          node2          node3          node4 counter-clockwise
        element('ShellMITC4',(14*i+1)*1000+j+1,  *[501+i*400+j*2,  601+i*400+j*2,  602+i*400+j*2,  502+i*400+j*2], moduleSecTag)
        element('ShellMITC4',(14*i+2)*1000+j+1,  *[601+i*400+j*2, 1401+i*400+j*2, 1402+i*400+j*2,  602+i*400+j*2], moduleSecTag)
        element('ShellMITC4',(14*i+3)*1000+j+1,  *[1401+i*400+j*2, 701+i*400+j*2,  702+i*400+j*2, 1402+i*400+j*2], moduleSecTag)
        element('ShellMITC4',(14*i+4)*1000+j+1,  *[701+i*400+j*2,  801+i*400+j*2,  802+i*400+j*2,  702+i*400+j*2], moduleSecTag)
    
        element('elasticBeamColumn', (14*i+5)*1000+j+1,  *[801+i*400+j*2,  701+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (14*i+6)*1000+j+1,  *[701+i*400+j*2, 1401+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (14*i+7)*1000+j+1,  *[1401+i*400+j*2, 601+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (14*i+8)*1000+j+1,  *[601+i*400+j*2,  501+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (14*i+9)*1000+j+1,  *[802+i*400+j*2,  702+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (14*i+10)*1000+j+1, *[702+i*400+j*2, 1402+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (14*i+11)*1000+j+1, *[1402+i*400+j*2, 602+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (14*i+12)*1000+j+1, *[602+i*400+j*2,  502+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (14*i+13)*1000+j+1, *[801+i*400+j*2,  802+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (14*i+14)*1000+j+1, *[501+i*400+j*2,  502+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);

# external braces
for i in range(0,2):
    element('elasticBeamColumn', 29000+1000*i+1, *[(i+1)*100+3, 1301], A_eb, Es, Gs, Jx_eb, Iy_eb, Iz_eb, ebTransfTag, '-mass', mass_eb, '-releasez', 1, 'releasey', 1);
    element('elasticBeamColumn', 29000+1000*i+2, *[(i+1)*100+4, 1301], A_eb, Es, Gs, Jx_eb, Iy_eb, Iz_eb, ebTransfTag, '-mass', mass_eb, '-releasez', 1, 'releasey', 1);

allNodeTags=getNodeTags();
alleleTags=getEleTags();
# render the model
#vfo.createODB(model="solarPanel")
vfo.plot_model()

# eigen analysis---------------------------------------------------------------
eigenValues = eigen(12);
omega = np.sqrt(eigenValues);
freq = omega/(2*math.pi);

vfo.plot_modeshape(modenumber=1, scale=5); #plot mode shape 1
vfo.plot_modeshape(modenumber=2, scale=5); #plot mode shape 2
vfo.plot_modeshape(modenumber=3, scale=5); #plot mode shape 3
vfo.plot_modeshape(modenumber=4, scale=5); #plot mode shape 4
vfo.plot_modeshape(modenumber=5, scale=5); #plot mode shape 5
vfo.plot_modeshape(modenumber=6, scale=5); #plot mode shape 6

# vfo.plot_modeshape(modenumber=7, scale=5); #plot mode shape 7
# vfo.plot_modeshape(modenumber=8, scale=5); #plot mode shape 8
# vfo.plot_modeshape(modenumber=9, scale=5); #plot mode shape 9
# vfo.plot_modeshape(modenumber=10, scale=5); #plot mode shape 10
# vfo.plot_modeshape(modenumber=11, scale=5); #plot mode shape 11
# vfo.plot_modeshape(modenumber=12, scale=5); #plot mode shape 12

# define loads-----------------------------------------------------------------
F = 1.0; 
timeSeries('Linear',1);
pattern('Plain', 1, 1);
load(801, *[0.0,  F, 0.0, 0.0, 0.0, 0.0]);

# Define RECORDERS ------------------------------------------------------------
recorder('Node', '-file', f'{dataDir}/tableCS400Wnode801.out', '-time', '-node', *[801], '-dof', *[1, 2, 3, 4, 5, 6,], 'disp');

# define ANALYSIS PARAMETERS---------------------------------------------------
constraints('Plain');  # how it handles boundary conditions
numberer('Plain');	   # renumber dof's to minimize band-width 
system('BandGeneral'); # how to store and solve the system of equations in the analysis
test('NormDispIncr', 1.0e-08, 1000); # determine if convergence has been achieved at the end of an iteration step
algorithm('Linear');
integrator('LoadControl', 0.1)
#Dincr = -0.01; #-0.00002
                                  #Node,  dof, 1st incr, Jd,  min,   max
#integrator('DisplacementControl', EndNode, 1,   Dincr,    1,  Dincr, -0.01);
analysis('Static');	# define type of analysis static or transient
analyze(100);
print('Finished')
wipe()