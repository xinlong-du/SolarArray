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
# SECTION properties for purlin C-Section 8CS2.5x059 in AISI Manual (2002)
A_pu = 0.822*in2m**2;     #cross-sectional area
Iz_pu = 7.79*in2m**4;     #second moment of area about the local z-axis
Iy_pu = 0.674*in2m**4;    #second moment of area about the local y-axis
Jx_pu = 0.000954*in2m**4;  #torsional moment of inertia of section
mass_pu = A_pu*rho_s;     #mass per unit length

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
i=0;
for j in range (0,11):
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

node(110,  -69.2423*in2m, 0.0, 52.1209*in2m)
node(111, -105.5808*in2m, 0.0, 31.0611*in2m)
node(210,  -69.2423*in2m, 265.3600*in2m, 52.1209*in2m)
node(211, -105.5808*in2m, 265.3600*in2m, 31.0611*in2m)

# define BOUNDARY CONDITIONS---------------------------------------------------
fix(110, 1, 1, 1, 0, 0, 0);
fix(210, 1, 0, 1, 0, 0, 0);
fix(111, 1, 1, 1, 0, 0, 0);  
fix(211, 1, 0, 1, 0, 0, 0);

# define ELEMENTS--------------------------------------------------------------
rafterTransfTag = 2;
vecxz = [0.0, 0.0, -1.0];
geomTransf('Linear', rafterTransfTag, *vecxz);

purlinTransfTag = 3;
vecxz = [0.0-(-88.0), 0.0, 92.25-41.25]; #local z' direction (nodes 104 - 107)
geomTransf('Linear', purlinTransfTag, *vecxz);

# purlins
nPurlin1 = [601,603,604,606,607,111,609,610,612,613,615,616,618,619,621,622,624,625,211,627,628,630,631,633]; #nodes of purlin # 1
nPurlin2 = [801,803,804,806,807,110,809,810,812,813,815,816,818,819,821,822,824,825,210,827,828,830,831,833]; #nodes of purlin # 2

for i in range (0,23):
    # purlin # 1
    #                            elemID   nodeI  nodeJ
    element('elasticBeamColumn', i+501, *[nPurlin1[i], nPurlin1[i+1]], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, purlinTransfTag, '-mass', mass_pu);
    # purlin # 2
    element('elasticBeamColumn', i+601, *[nPurlin2[i], nPurlin2[i+1]], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, purlinTransfTag, '-mass', mass_pu);

# modules and module frames
i=0;
for j in range (0,11):
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
# gravity loads
#module frame, 0.1 is used to account for 10 steps in analyze(10)
g_mfCorne=-0.1*mass_mf*g*(84.0/4/2+41.26/2/2)*in2m;  #nodes at corner
g_mfMidEW=-0.1*mass_mf*g*(41.26/2)*in2m;             #nodes at middle of E-W direction
g_mfMidNS=-0.1*mass_mf*g*(84.0/4)*in2m;              #nodes at middle of N-S direction

#module, 0.1 is used to account for 10 steps in analyze(10)
g_m=84.0*in2m*41.26*in2m*h*rho_m*g;
g_mCo=-0.1*g_m/32;     #corner, 4 in total
g_mEd=-0.1*g_m/32*2;   #edge, 8 in total
g_mIn=-0.1*g_m/32*4;   #internal, 3 in total

# wind pressure
#pMax=-1165.6;
pMax=1131.9;
f_m=84.0*in2m*41.26*in2m*pMax;
f_mCo=0.1*f_m/32;     #corner, 4 in total
f_mEd=0.1*f_m/32*2;   #edge, 8 in total
f_mIn=0.1*f_m/32*4;   #internal, 3 in total

timeSeries('Linear',10000);
pattern('Plain', 10000, 10000);

for i in range (0,1):
    for j in range (0,11):
        load(501+i*700+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi)+g_mCo+g_mfCorne, 0.0, 0.0, 0.0]);
        load(502+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi)+g_mEd+g_mfMidEW, 0.0, 0.0, 0.0]);
        load(503+i*700+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi)+g_mCo+g_mfCorne, 0.0, 0.0, 0.0]);
        load(601+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi)+g_mEd+g_mfMidNS, 0.0, 0.0, 0.0]);
        load(602+i*700+j*3, *[f_mIn*math.sin(30/180*math.pi), 0.0, -f_mIn*math.cos(30/180*math.pi)+g_mIn, 0.0, 0.0, 0.0]);
        load(603+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi)+g_mEd+g_mfMidNS, 0.0, 0.0, 0.0]);
        load(701+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi)+g_mEd+g_mfMidNS, 0.0, 0.0, 0.0]);
        load(702+i*700+j*3, *[f_mIn*math.sin(30/180*math.pi), 0.0, -f_mIn*math.cos(30/180*math.pi)+g_mIn, 0.0, 0.0, 0.0]);
        load(703+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi)+g_mEd+g_mfMidNS, 0.0, 0.0, 0.0]);
        load(801+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi)+g_mEd+g_mfMidNS, 0.0, 0.0, 0.0]);
        load(802+i*700+j*3, *[f_mIn*math.sin(30/180*math.pi), 0.0, -f_mIn*math.cos(30/180*math.pi)+g_mIn, 0.0, 0.0, 0.0]);
        load(803+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi)+g_mEd+g_mfMidNS, 0.0, 0.0, 0.0]);
        load(901+i*700+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi)+g_mCo+g_mfCorne, 0.0, 0.0, 0.0]);
        load(902+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi)+g_mEd+g_mfMidEW, 0.0, 0.0, 0.0]);
        load(903+i*700+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi)+g_mCo+g_mfCorne, 0.0, 0.0, 0.0]);

# Define RECORDERS ------------------------------------------------------------
allNodeTags=getNodeTags();
alleleTags=getEleTags();

eleRec=list(range(501,513))+list(range(601,613));
recorder('Element', '-file', f'{dataDir}/test6PeleForce.out', '-time', '-ele', *eleRec, 'localForces');
recorder('Node', '-file', f'{dataDir}/test6PnodeDisp.out', '-time', '-node', *allNodeTags, '-dof', *[1, 2, 3, 4, 5, 6,], 'disp');

# define ANALYSIS PARAMETERS---------------------------------------------------
constraints('Plain');  # how it handles boundary conditions
numberer('RCM');	   # renumber dof's to minimize band-width 
system('UmfPack'); # how to store and solve the system of equations in the analysis
test('NormDispIncr', 1.0e-08, 1000); # determine if convergence has been achieved at the end of an iteration step
algorithm('Linear');
integrator('LoadControl', 1)
analysis('Static');	# define type of analysis static or transient
analyze(10);
print('Finished')

# postprocessing---------------------------------------------------------------
# forces and displacements at mid span
efLocEnd512=eleResponse(512, 'localForces')
efLocEnd612=eleResponse(612, 'localForces')

efLocEnd5xx=[None]*13;
efLocEnd6xx=[None]*13;
for i in range (0,13):
    efLocEnd5xx[i]=eleResponse(i+506, 'localForces');
    efLocEnd6xx[i]=eleResponse(i+606, 'localForces');
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
    coordNdPurlin1[i]=nodeCoord(nPurlin1[i+5],2);

coordNdPurlin1m=[x - coordNdPurlin1[0] for x in coordNdPurlin1];
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12,12))
ax = fig.add_axes([0, 0, 1, 1])
ax.plot(coordNdPurlin1m,moLocEnd5xx,linewidth=0.5)
plt.rc('xtick', labelsize=8)    # fontsize of the tick labels
plt.rc('ytick', labelsize=8)    # fontsize of the tick labels
ax.tick_params(direction="in")
ax.set_xlim(0.0, coordNdPurlin1m[13])
#ax.set_ylim(-13500,100)
plt.xticks([0.0,0.25*coordNdPurlin1m[13],0.5*coordNdPurlin1m[13],0.75*coordNdPurlin1m[13],coordNdPurlin1m[13]])
#plt.yticks(np.arange(-13500, 100, 100))
plt.grid()
#plt.show()
plt.ylabel('Mz (N-m)',fontsize=8)
plt.xlabel('Y (m)',fontsize=8);
file_name = 'momentPin1'
plt.savefig('./'+file_name+'.tif', transparent=False, bbox_inches='tight', dpi=100)

ax.set_ylim(-3500,-1000)
plt.yticks(np.arange(-3500, -1000, 50))
file_name = 'momentPin2'
plt.savefig('./'+file_name+'.tif', transparent=False, bbox_inches='tight', dpi=100)

#%% calculate Cb
Mmax=4321.3;
Ma=1350.0;
Mb=(3171.7+3087.2)/2;
Mc=1425.0;
Cb=12.5*Mmax/(2.5*Mmax+3*Ma+4*Mb+3*Mc);

#%%
ndGloEnd516=nodeDisp(516);
ndGloEnd518=nodeDisp(518);
ndGloEnd616=nodeDisp(616);
ndGloEnd618=nodeDisp(618);
ndGloEnd716=nodeDisp(716);
ndGloEnd718=nodeDisp(718);
ndGloEnd816=nodeDisp(816);
ndGloEnd818=nodeDisp(818);
ndLocYend516=39.3701*ndGloEnd516[2]*math.cos(30/180*math.pi)-39.3701*ndGloEnd516[0]*math.sin(30/180*math.pi); #m to in
ndLocYend616=39.3701*ndGloEnd616[2]*math.cos(30/180*math.pi)-39.3701*ndGloEnd616[0]*math.sin(30/180*math.pi); #m to in
ndLocYend716=39.3701*ndGloEnd716[2]*math.cos(30/180*math.pi)-39.3701*ndGloEnd716[0]*math.sin(30/180*math.pi); #m to in
ndLocYend816=39.3701*ndGloEnd816[2]*math.cos(30/180*math.pi)-39.3701*ndGloEnd816[0]*math.sin(30/180*math.pi); #m to in

#required strength for Cb=1
reqMoment=max([abs(number) for number in moLocEnd5xx]);
reqMomentLTB=reqMoment*0.0002248*39.3701/Cb/0.9; #N-m to kip-in. converts Cb=1.7 to Cb=1. phi_b=0.9
reqMomentYLD=reqMoment*0.0002248*39.3701/0.95;   #N-m to kip-in. phi_b=0.95

#available strength for beam charts in AISI Manual
ubLength=265.36; #in
avaMoment=79; #=required strength, Section 12CS3.5x105

#wipe()
#vfo.plot_deformedshape(model="solarPanel", loadcase="static", scale=10)
#------------------------------------------------------------------------------