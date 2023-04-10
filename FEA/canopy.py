# -----------------------------------------------------------------------------
# Solar canopy
# Units: m, N, kg, s, N/m2, kg/m3
# Xinlong Du, 2023
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
# SECTION properties for purlin C-Section C10x3.5x1.25 (.12" Thickness)
A_pu = 2.19*in2m**2;      #cross-sectional area
Iz_pu = 32.6*in2m**4;     #second moment of area about the local z-axis
Iy_pu = 3.64*in2m**4;     #second moment of area about the local y-axis
Jx_pu = 0.0105*in2m**4;   #torsional moment of inertia of section
mass_pu = A_pu*rho_s;     #mass per unit length

# SECTION properties for rafter (top beam) HSS 20x4x5/16
A_r = 13.4*in2m**2;       #cross-sectional area
Iz_r = 560.0*in2m**4      #second moment of area about the local z-axis
Iy_r = 41.2*in2m**4;      #second moment of area about the local y-axis
Jx_r = 134.0*in2m**4;     #torsional moment of inertia of section
mass_r = A_r*rho_s;       #mass per unit length
    
# SECTION properties for post HSS 12x4x1/2
A_po = 13.5*in2m**2;      #cross-sectional area
Iz_po = 210.0*in2m**4;    #second moment of area about the local z-axis
Iy_po = 35.3*in2m**4;     #second moment of area about the local y-axis
Jx_po = 105.0*in2m**4;    #torsional moment of inertia of section
mass_po = A_po*rho_s;     #mass per unit length

# SECTION properties for module frames
A_mf = 112.6*0.001**2;     #cross-sectional area
Iz_mf = 12932.0*0.001**4;  #second moment of area about the local z-axis
Iy_mf = Iz_mf/5.0;         #second moment of area about the local y-axis (temp)
Jx_mf = Jx_pu/5.0;         #torsional moment of inertia of section (temp)
mass_mf = A_mf*rho_mf;     #mass per unit length

# SECTION properties for module
moduleSecTag = 1;
h = 5.42*0.001; #depth of module
section('ElasticMembranePlateSection', moduleSecTag, Em, nu_m, h, rho_m)

# define NODES-----------------------------------------------------------------
# post foundations
node(1, 0.0,           0.0,              0.0)
node(2, 0.0,           324.0*in2m,       0.0)
node(3, 0.0,           648.0*in2m,       0.0)

# rafters (top beams)
for i in range (0,3):
    node(10001+10000*i, -233.0002*in2m,     324*i*in2m,    55.3912*in2m)
    node(10002+10000*i, -191.3133*in2m,     324*i*in2m,    60.5097*in2m)
    node(10003+10000*i, -148.1375*in2m,     324*i*in2m,    65.8110*in2m)
    node(10004+10000*i, -106.4506*in2m,     324*i*in2m,    70.9295*in2m)
    node(10005+10000*i, -63.2748*in2m,      324*i*in2m,    76.2308*in2m)
    node(10006+10000*i, -21.5879*in2m,      324*i*in2m,    81.3493*in2m)
    node(10007+10000*i,  0.0000*in2m,       324*i*in2m,    84.0000*in2m)
    node(10008+10000*i,  21.5879*in2m,      324*i*in2m,    86.6507*in2m)
    node(10009+10000*i,  63.2748*in2m,      324*i*in2m,    91.7692*in2m)
    node(10010+10000*i,  106.4506*in2m,     324*i*in2m,    97.0705*in2m)
    node(10011+10000*i,  148.1375*in2m,     324*i*in2m,    102.1890*in2m)
    node(10012+10000*i,  191.3133*in2m,     324*i*in2m,    107.4903*in2m)
    node(10013+10000*i,  233.0002*in2m,     324*i*in2m,    112.6088*in2m)

# purlins and modules
for i in range (0,6):
    for j in range (0,20):
        node(101+400*i+2*j, (-253.8437+84.8627*i)*in2m,     (-110.2500+43.5*j)*in2m,     (52.8319+10.4198*i)*in2m)
        node(102+400*i+2*j, (-253.8437+84.8627*i)*in2m,      (-68.2500+43.5*j)*in2m,     (52.8319+10.4198*i)*in2m)
        node(201+400*i+2*j, (-233.0002+84.8627*i)*in2m,     (-110.2500+43.5*j)*in2m,     (55.3912+10.4198*i)*in2m)
        node(202+400*i+2*j, (-233.0002+84.8627*i)*in2m,      (-68.2500+43.5*j)*in2m,     (55.3912+10.4198*i)*in2m)
        node(301+400*i+2*j, (-191.3133+84.8627*i)*in2m,     (-110.2500+43.5*j)*in2m,     (60.5097+10.4198*i)*in2m)
        node(302+400*i+2*j, (-191.3133+84.8627*i)*in2m,      (-68.2500+43.5*j)*in2m,     (60.5097+10.4198*i)*in2m)
        node(401+400*i+2*j, (-170.4698+84.8627*i)*in2m,     (-110.2500+43.5*j)*in2m,     (63.0689+10.4198*i)*in2m)
        node(402+400*i+2*j, (-170.4698+84.8627*i)*in2m,      (-68.2500+43.5*j)*in2m,     (63.0689+10.4198*i)*in2m)

# define BOUNDARY CONDITIONS---------------------------------------------------
fix(1, 1, 1, 1, 1, 1, 1);  
fix(2, 1, 1, 1, 1, 1, 1);
fix(3, 1, 1, 1, 1, 1, 1);  

# define ELEMENTS--------------------------------------------------------------
postTransfTag = 1;
vecxz = [0.0, 1.0, 0.0];
geomTransf('Linear', postTransfTag, *vecxz);

rafterTransfTag = 2;
vecxz = [0.0, -1.0, 0.0];
geomTransf('Linear', rafterTransfTag, *vecxz);

purlinTransfTag = 3;
vecxz = [-233.0002-233.0002, 324-324, 55.3912-112.6088]; #local z' direction (nodes 10001 - 10013)
geomTransf('Linear', purlinTransfTag, *vecxz);

# post                       ID  nodeI nodeJ
element('elasticBeamColumn', 1, *[1, 10007], A_po, Es, Gs, Jx_po, Iy_po, Iz_po, postTransfTag, '-mass', mass_po);
element('elasticBeamColumn', 2, *[2, 20007], A_po, Es, Gs, Jx_po, Iy_po, Iz_po, postTransfTag, '-mass', mass_po);
element('elasticBeamColumn', 3, *[3, 30007], A_po, Es, Gs, Jx_po, Iy_po, Iz_po, postTransfTag, '-mass', mass_po);

# rafter
for i in range (1,4):
    for j in range (1,13):
        element('elasticBeamColumn', 100*i+j, *[10000*i+j, 10000*i+j+1], A_r, Es, Gs, Jx_r, Iy_r, Iz_r, rafterTransfTag, '-mass', mass_r);

# purlins
nPurlin=[[0]*43]*12; #nodes of purlins
rowPurlin=[201,301,601,701,1001,1101,1401,1501,1801,1901,2201,2301];
nRafter=list(range(1,14));
nRafter.remove(7)
for i in range (0,12):
    nPurlin[i] = list(range(rowPurlin[i],rowPurlin[i]+40));
    nPurlin[i].insert(35,30000+nRafter[i])
    nPurlin[i].insert(20,20000+nRafter[i])
    nPurlin[i].insert(5,10000+nRafter[i])

for i in range (0,12):
    for j in range (0,42):
        #                            elemID         nodeI          nodeJ
        element('elasticBeamColumn', i*100+400+j, *[nPurlin[i][j], nPurlin[i][j+1]], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, purlinTransfTag, '-mass', mass_pu);

# modules and module frames
for i in range (0,6):
    for j in range (0,20):
        #                    elemID               node1          node2          node3          node4 counter-clockwise
        element('ShellMITC4',(11*i+1)*10000+j,  *[101+i*400+j*2, 201+i*400+j*2, 202+i*400+j*2, 102+i*400+j*2], moduleSecTag)
        element('ShellMITC4',(11*i+2)*10000+j,  *[201+i*400+j*2, 301+i*400+j*2, 302+i*400+j*2, 202+i*400+j*2], moduleSecTag)
        element('ShellMITC4',(11*i+3)*10000+j,  *[301+i*400+j*2, 401+i*400+j*2, 402+i*400+j*2, 302+i*400+j*2], moduleSecTag)
    
        element('elasticBeamColumn', (11*i+4)*10000+j, *[101+i*400+j*2, 201+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (11*i+5)*10000+j, *[201+i*400+j*2, 301+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (11*i+6)*10000+j, *[301+i*400+j*2, 401+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (11*i+7)*10000+j, *[401+i*400+j*2, 402+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (11*i+8)*10000+j, *[402+i*400+j*2, 302+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (11*i+9)*10000+j, *[302+i*400+j*2, 202+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (11*i+10)*10000+j, *[202+i*400+j*2, 102+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
        element('elasticBeamColumn', (11*i+11)*10000+j, *[102+i*400+j*2, 101+i*400+j*2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);

# render the model
#vfo.createODB(model="solarPanel")
vfo.plot_model()

# eigen analysis---------------------------------------------------------------
eigenValues = eigen(12);
omega = np.sqrt(eigenValues);
freq = omega/(2*math.pi);

vfo.plot_modeshape(modenumber=1, scale=500); #plot mode shape 1
vfo.plot_modeshape(modenumber=2, scale=50); #plot mode shape 2
vfo.plot_modeshape(modenumber=3, scale=50); #plot mode shape 3
vfo.plot_modeshape(modenumber=4, scale=50); #plot mode shape 4
vfo.plot_modeshape(modenumber=5, scale=50); #plot mode shape 5
vfo.plot_modeshape(modenumber=6, scale=50); #plot mode shape 6

# define loads-----------------------------------------------------------------
F = 1000.0; 
timeSeries('Linear',1);
pattern('Plain', 1, 1);
load(701, *[0.0,  F, 0.0, 0.0, 0.0, 0.0]);

# Define RECORDERS ------------------------------------------------------------
recorder('Node', '-file', f'{dataDir}/ElasDispEndDB40.out', '-time', '-node', *[701], '-dof', *[1, 2, 3, 4, 5, 6,], 'disp');

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
analyze(5);
print('Finished')
wipe()
#------------------------------------------------------------------------------
# set finishTime [clock clicks -milliseconds];
# puts "Time taken: [expr ($finishTime-$startTime)/1000] sec"
# set systemTime [clock seconds] 
# puts "Finished Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"