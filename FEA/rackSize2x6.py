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
g=9.8*1.2;       #gravitational acceleration (m/s2), 1.2 is for 1.2D+1.0W

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
# SECTION properties for purlin C-Section 6CS2.5x065 in AISI Manual (2002)
A_pu = 0.776*in2m**2;     #cross-sectional area
Iz_pu = 4.36*in2m**4;     #second moment of area about the local z-axis
Iy_pu = 0.677*in2m**4;    #second moment of area about the local y-axis
Jx_pu = 0.00109*in2m**4;  #torsional moment of inertia of section
mass_pu = A_pu*rho_s;     #mass per unit length

# SECTION properties for purlin C-Section 8CS3.5x065 in AISI Manual (2002)
# A_pu = 1.040*in2m**2;     #cross-sectional area
# Iz_pu = 10.6*in2m**4;     #second moment of area about the local z-axis
# Iy_pu = 1.680*in2m**4;    #second moment of area about the local y-axis
# Jx_pu = 0.00146*in2m**4;  #torsional moment of inertia of section
# mass_pu = A_pu*rho_s;     #mass per unit length

# SECTION properties for purlin C-Section 4CS2.5x059 in AISI Manual (2002)
# A_pu = 0.538*in2m**2;     #cross-sectional area
# Iz_pu = 1.35*in2m**4;     #second moment of area about the local z-axis
# Iy_pu = 0.331*in2m**4;    #second moment of area about the local y-axis
# Jx_pu = 0.000625*in2m**4;  #torsional moment of inertia of section
# mass_pu = A_pu*rho_s;     #mass per unit length

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
node(101, -93.9523*in2m, -114.9700*in2m, -4.1151*in2m)
node(102, -57.9523*in2m, -114.9700*in2m, -4.1151*in2m)
node(103, -93.9523*in2m, -114.9700*in2m, 37.8004*in2m)
node(104, -57.9523*in2m, -114.9700*in2m, 58.6392*in2m)
node(201, -93.9523*in2m,  169.0300*in2m, -4.1151*in2m)
node(202, -57.9523*in2m,  169.0300*in2m, -4.1151*in2m)
node(203, -93.9523*in2m,  169.0300*in2m, 37.8004*in2m)
node(204, -57.9523*in2m,  169.0300*in2m, 58.6392*in2m)

for i in range (0,7):
    node(301+i, -93.9523*in2m, (-80.9700+36.0*i)*in2m, -4.1151*in2m)
    node(401+i, -57.9523*in2m, (-80.9700+36.0*i)*in2m, -4.1151*in2m)

i=0;
for j in range (0,6):
    node(501+700*i+3*j, (-123.7500+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (20.5313+43.2185*i)*in2m)
    node(502+700*i+3*j, (-123.7500+74.5730*i)*in2m, (-78.6200+42.26*j)*in2m, (20.5313+43.2185*i)*in2m)
    node(503+700*i+3*j, (-123.7500+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (20.5313+43.2185*i)*in2m)
    node(601+700*i+3*j, (-105.5808+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (31.0611+43.2185*i)*in2m)
    node(602+700*i+3*j, (-105.5808+74.5730*i)*in2m, (-78.6200+42.26*j)*in2m, (31.0611+43.2185*i)*in2m)
    node(603+700*i+3*j, (-105.5808+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (31.0611+43.2185*i)*in2m)
    node(701+700*i+3*j,  (-87.4115+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (41.5910+43.2185*i)*in2m)
    node(702+700*i+3*j,  (-87.4115+74.5730*i)*in2m, (-78.6200+42.26*j)*in2m, (41.5910+43.2185*i)*in2m)
    node(703+700*i+3*j,  (-87.4115+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (41.5910+43.2185*i)*in2m)
    node(801+700*i+3*j,  (-69.2423+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (52.1209+43.2185*i)*in2m)
    node(802+700*i+3*j,  (-69.2423+74.5730*i)*in2m, (-78.6200+42.26*j)*in2m, (52.1209+43.2185*i)*in2m)
    node(803+700*i+3*j,  (-69.2423+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (52.1209+43.2185*i)*in2m)
    node(901+700*i+3*j,  (-51.0730+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (62.6508+43.2185*i)*in2m)
    node(902+700*i+3*j,  (-51.0730+74.5730*i)*in2m, (-78.6200+42.26*j)*in2m, (62.6508+43.2185*i)*in2m)
    node(903+700*i+3*j,  (-51.0730+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (62.6508+43.2185*i)*in2m)

node(600, -105.5808*in2m, (-99.2500-15.72)*in2m, 31.0611*in2m)
node(619, -105.5808*in2m, (153.3100+15.72)*in2m, 31.0611*in2m)
node(800,  -69.2423*in2m, (-99.2500-15.72)*in2m, 52.1209*in2m)
node(819,  -69.2423*in2m, (153.3100+15.72)*in2m, 52.1209*in2m)

# define BOUNDARY CONDITIONS---------------------------------------------------
fix(101, 1, 1, 1, 0, 0, 0);
fix(201, 1, 0, 1, 0, 0, 0);
fix(102, 1, 1, 1, 0, 0, 0);  
fix(202, 1, 0, 1, 0, 0, 0);
for i in range (1,7):
    fix(300+i, 0, 0, 1, 0, 0, 0);
    fix(400+i, 0, 0, 1, 0, 0, 0);

# define ELEMENTS--------------------------------------------------------------
rafterTransfTag = 2;
vecxz = [0.0, 0.0, -1.0];
geomTransf('Linear', rafterTransfTag, *vecxz);

purlinTransfTag = 3;
vecxz = [0.0-(-88.0), 0.0, 92.25-41.25]; #local z' direction (nodes 104 - 107)
geomTransf('Linear', purlinTransfTag, *vecxz);

# purlins
nPurlin1 = [600,601,603,604,606,607,609,610,612,613,615,616,618,619]; #nodes of purlin # 1
nPurlin2 = [800,801,803,804,806,807,809,810,812,813,815,816,818,819]; #nodes of purlin # 2
for i in range (0,13):
    # purlin # 1
    #                            elemID   nodeI  nodeJ
    element('elasticBeamColumn', i+500, *[nPurlin1[i], nPurlin1[i+1]], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, purlinTransfTag, '-mass', mass_pu);
    # purlin # 2
    element('elasticBeamColumn', i+600, *[nPurlin2[i], nPurlin2[i+1]], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, purlinTransfTag, '-mass', mass_pu);

# modules and module frames
i=0;
for j in range (0,6):
    #                    elemID               node1          node2          node3          node4 counter-clockwise
    element('ShellMITC4',(24*i+1)*1000+j+1, *[501+i*700+j*3, 601+i*700+j*3, 602+i*700+j*3, 502+i*700+j*3], moduleSecTag)
    element('ShellMITC4',(24*i+2)*1000+j+1, *[601+i*700+j*3, 701+i*700+j*3, 702+i*700+j*3, 602+i*700+j*3], moduleSecTag)
    element('ShellMITC4',(24*i+3)*1000+j+1, *[701+i*700+j*3, 801+i*700+j*3, 802+i*700+j*3, 702+i*700+j*3], moduleSecTag)
    element('ShellMITC4',(24*i+4)*1000+j+1, *[801+i*700+j*3, 901+i*700+j*3, 902+i*700+j*3, 802+i*700+j*3], moduleSecTag)
    element('ShellMITC4',(24*i+5)*1000+j+1, *[502+i*700+j*3, 602+i*700+j*3, 603+i*700+j*3, 503+i*700+j*3], moduleSecTag)
    element('ShellMITC4',(24*i+6)*1000+j+1, *[602+i*700+j*3, 702+i*700+j*3, 703+i*700+j*3, 603+i*700+j*3], moduleSecTag)
    element('ShellMITC4',(24*i+7)*1000+j+1, *[702+i*700+j*3, 802+i*700+j*3, 803+i*700+j*3, 703+i*700+j*3], moduleSecTag)
    element('ShellMITC4',(24*i+8)*1000+j+1, *[802+i*700+j*3, 902+i*700+j*3, 903+i*700+j*3, 803+i*700+j*3], moduleSecTag)
    
    element('elasticBeamColumn', (24*i+9)*1000+j+1,  *[901+i*700+j*3,  801+i*700+j*3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', (24*i+10)*1000+j+1, *[801+i*700+j*3,  701+i*700+j*3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', (24*i+11)*1000+j+1, *[701+i*700+j*3,  601+i*700+j*3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', (24*i+12)*1000+j+1, *[601+i*700+j*3,  501+i*700+j*3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', (24*i+13)*1000+j+1, *[903+i*700+j*3,  803+i*700+j*3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', (24*i+14)*1000+j+1, *[803+i*700+j*3,  703+i*700+j*3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', (24*i+15)*1000+j+1, *[703+i*700+j*3,  603+i*700+j*3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', (24*i+16)*1000+j+1, *[603+i*700+j*3,  503+i*700+j*3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', (24*i+17)*1000+j+1, *[901+i*700+j*3,  902+i*700+j*3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', (24*i+18)*1000+j+1, *[902+i*700+j*3,  903+i*700+j*3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', (24*i+19)*1000+j+1, *[501+i*700+j*3,  502+i*700+j*3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', (24*i+20)*1000+j+1, *[502+i*700+j*3,  503+i*700+j*3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);

# reaction frame
for i in range (1,3):
    element('elasticBeamColumn', i*100+1, *[i*100+1, i*100+2], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', i*100+2, *[i*100+1, i*100+3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', i*100+3, *[i*100+2, i*100+4], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, purlinTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', i*100+4, *[600+(i-1)*19, i*100+3], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', i*100+5, *[i*100+3, 800+(i-1)*19], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', i*100+6, *[800+(i-1)*19, i*100+4], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);

for i in range (1,7):
    element('elasticBeamColumn', 300+i, *[300+i, 301+i], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
    element('elasticBeamColumn', 400+i, *[400+i, 401+i], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);

element('elasticBeamColumn', 300, *[101, 301], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
element('elasticBeamColumn', 308, *[307, 201], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
element('elasticBeamColumn', 400, *[102, 401], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);
element('elasticBeamColumn', 408, *[407, 202], A_mf, Emf, Gmf, Jx_mf, Iy_mf, Iz_mf, rafterTransfTag, '-mass', mass_mf);

# render the model
vfo.createODB(model="solarPanel", loadcase="static", Nmodes=6, deltaT=1)
vfo.plot_model()

# eigen analysis---------------------------------------------------------------
eigenValues = eigen(12);
omega = np.sqrt(eigenValues);
freq = omega/(2*math.pi);

vfo.plot_modeshape(modenumber=1, scale=2); #plot mode shape 1
vfo.plot_modeshape(modenumber=2, scale=2); #plot mode shape 2
# vfo.plot_modeshape(modenumber=3, scale=1); #plot mode shape 3
# vfo.plot_modeshape(modenumber=4, scale=1); #plot mode shape 4
# vfo.plot_modeshape(modenumber=5, scale=1); #plot mode shape 5
# vfo.plot_modeshape(modenumber=6, scale=1); #plot mode shape 6

# define loads-----------------------------------------------------------------
# actuator force
f_m=1.0; #Newton
f_p=-1.0;

timeSeries('Linear',10000);
pattern('Plain', 10000, 10000);
load(607, *[f_m*math.sin(30/180*math.pi), 0.0, -f_m*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
load(807, *[f_p*math.sin(30/180*math.pi), 0.0, -f_p*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
load(612, *[f_p*math.sin(30/180*math.pi), 0.0, -f_p*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
load(812, *[f_m*math.sin(30/180*math.pi), 0.0, -f_m*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);

# Define RECORDERS ------------------------------------------------------------
allNodeTags=getNodeTags();
alleleTags=getEleTags();

eleRec=list(range(501,513))+list(range(601,613));
recorder('Element', '-file', f'{dataDir}/testAllCases2/test6PeleForceTwist.out', '-time', '-ele', *eleRec, 'localForces');
recorder('Node', '-file', f'{dataDir}/testAllCases2/test6PnodeDispTwist.out', '-time', '-node', *[607,807,612,812], '-dof', *[1, 2, 3, 4, 5, 6,], 'disp');

# define ANALYSIS PARAMETERS---------------------------------------------------
constraints('Plain');  # how it handles boundary conditions
numberer('RCM');	   # renumber dof's to minimize band-width 
system('UmfPack'); # how to store and solve the system of equations in the analysis
test('NormDispIncr', 1.0e-08, 1000); # determine if convergence has been achieved at the end of an iteration step
algorithm('Linear');
#integrator('LoadControl', 1)
nodeTag=609;
dof=3;
incr=-0.000001;
integrator('DisplacementControl', nodeTag, dof, incr)
analysis('Static');	# define type of analysis static or transient
analyze(53);
print('Finished')

# postprocessing---------------------------------------------------------------
# forces and displacements at mid span
efLocEnd506=eleResponse(506, 'localForces')
efLocEnd606=eleResponse(606, 'localForces')

efLocEnd5xx=[None]*13;
efLocEnd6xx=[None]*13;
for i in range (0,13):
    efLocEnd5xx[i]=eleResponse(i+500, 'localForces');
    efLocEnd6xx[i]=eleResponse(i+600, 'localForces');
#%%
moLocEnd5xx=[None]*14;
moLocEnd6xx=[None]*14;
for i in range (0,13):
    moLocEnd5xx[i]=efLocEnd5xx[i][5];
    moLocEnd6xx[i]=efLocEnd6xx[i][5];
moLocEnd5xx[13]=-efLocEnd5xx[12][11];
moLocEnd6xx[13]=-efLocEnd6xx[12][11];

coordNdPurlin1=[None]*14;
for i in range (0,14):
    coordNdPurlin1[i]=nodeCoord(nPurlin1[i],2);

coordNdPurlin1m=[x - coordNdPurlin1[0] for x in coordNdPurlin1];
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12,12))
ax = fig.add_axes([0, 0, 1, 1])
ax.plot(coordNdPurlin1m,moLocEnd5xx,linewidth=0.5)
plt.rc('xtick', labelsize=8)    # fontsize of the tick labels
plt.rc('ytick', labelsize=8)    # fontsize of the tick labels
ax.tick_params(direction="in")
ax.set_xlim(0.0, coordNdPurlin1m[13])
ax.set_ylim(-3100,100)
plt.xticks([0.0,0.25*coordNdPurlin1m[13],0.5*coordNdPurlin1m[13],0.75*coordNdPurlin1m[13],coordNdPurlin1m[13]])
plt.yticks(np.arange(-3000, 100, 100))
plt.grid()
#plt.show()
plt.ylabel('Mz (N-m)',fontsize=8)
plt.xlabel('Y (m)',fontsize=8);
file_name = 'momentPin1'
plt.savefig('./'+file_name+'.tif', transparent=False, bbox_inches='tight', dpi=100)

ax.set_ylim(-13500,-9500)
plt.yticks(np.arange(-13500, -9500, 100))
file_name = 'momentPin2'
plt.savefig('./'+file_name+'.tif', transparent=False, bbox_inches='tight', dpi=100)

#%% calculate Cb
Mmax=3000.0;
Ma=1500.0;
Mb=3000.0;
Mc=1500.0;
Cb=12.5*Mmax/(2.5*Mmax+3*Ma+4*Mb+3*Mc);

#%%
ndGloEnd509=nodeDisp(509);
ndGloEnd608=nodeDisp(608);
ndGloEnd609=nodeDisp(609);
ndGloEnd610=nodeDisp(610);
ndGloEnd611=nodeDisp(611);
ndGloEnd709=nodeDisp(709);
ndGloEnd809=nodeDisp(809);
ndGloEnd810=nodeDisp(810);
ndLocYend509=39.3701*ndGloEnd509[2]*math.cos(30/180*math.pi)-39.3701*ndGloEnd509[0]*math.sin(30/180*math.pi); #m to in
ndLocYend608=39.3701*ndGloEnd608[2]*math.cos(30/180*math.pi)-39.3701*ndGloEnd608[0]*math.sin(30/180*math.pi); #m to in
ndLocYend609=39.3701*ndGloEnd609[2]*math.cos(30/180*math.pi)-39.3701*ndGloEnd609[0]*math.sin(30/180*math.pi); #m to in
ndLocYend610=39.3701*ndGloEnd610[2]*math.cos(30/180*math.pi)-39.3701*ndGloEnd610[0]*math.sin(30/180*math.pi); #m to in
ndLocYend611=39.3701*ndGloEnd611[2]*math.cos(30/180*math.pi)-39.3701*ndGloEnd611[0]*math.sin(30/180*math.pi); #m to in
ndLocYend709=39.3701*ndGloEnd709[2]*math.cos(30/180*math.pi)-39.3701*ndGloEnd709[0]*math.sin(30/180*math.pi); #m to in

#required strength for Cb=1
reqMoment=max([abs(number) for number in moLocEnd5xx]);
reqMomentLTB=reqMoment*0.0002248*39.3701/Cb/0.9; #N-m to kip-in. 1.67 converts Cb=1.67 to Cb=1. 0.9 is for phi_b=0.9

#available strength for beam charts in AISI Manual
ubLength=260.0; #in
avaMoment=79; #=required strength, Section 12CS3.5x105

wipe()
vfo.plot_deformedshape(model="solarPanel", loadcase="static", scale=10)
#------------------------------------------------------------------------------