# -----------------------------------------------------------------------------
# Solar PV rack 2x6 CS-400W
# Units: m, N, kg, s, N/m2, kg/m3
# Xinlong Du, 2022
#
# -----------------------------------------------------------------------------
from openseespy.opensees import *
import numpy as np
import math
import h5py

# visulization
import vfo.vfo as vfo

# SET UP ----------------------------------------------------------------------
wipe();
model('basic', '-ndm', 3, '-ndf', 6);
dataDir = 'Data';
#os.mkdir(dataDir);
in2m=0.0254; #convert inch to meter
g=9.8;       #gravitational acceleration (m/s2), 1.2 is for 1.2D+1.0W

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
# SECTION properties for purlin C-Section 12CS3.5x105 in AISI Manual (2002)
A_pu = 2.09*in2m**2;     #cross-sectional area
Iz_pu = 43.8*in2m**4;     #second moment of area about the local z-axis
Iy_pu = 3.07*in2m**4;    #second moment of area about the local y-axis
Jx_pu = 0.00769*in2m**4;  #torsional moment of inertia of section
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

node(600, -105.5808*in2m, (-99.2500-5.0)*in2m, 31.0611*in2m)
node(619, -105.5808*in2m, (153.3100+5.0)*in2m, 31.0611*in2m)
node(800,  -69.2423*in2m, (-99.2500-5.0)*in2m, 52.1209*in2m)
node(819,  -69.2423*in2m, (153.3100+5.0)*in2m, 52.1209*in2m)

# define BOUNDARY CONDITIONS---------------------------------------------------
fix(600, 1, 1, 1, 0, 0, 0);
fix(619, 1, 0, 1, 0, 0, 0);
fix(800, 1, 1, 1, 0, 0, 0);  
fix(819, 1, 0, 1, 0, 0, 0);

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

allNodeTags=getNodeTags();
alleleTags=getEleTags();
# render the model
vfo.createODB(model="solarPanel", loadcase="static", Nmodes=6, deltaT=1)
vfo.plot_model()

# eigen analysis---------------------------------------------------------------
eigenValues = eigen(12);
omega = np.sqrt(eigenValues);
freq = omega/(2*math.pi);

# vfo.plot_modeshape(modenumber=1, scale=1); #plot mode shape 1
# vfo.plot_modeshape(modenumber=2, scale=1); #plot mode shape 2
# vfo.plot_modeshape(modenumber=3, scale=1); #plot mode shape 3
# vfo.plot_modeshape(modenumber=4, scale=1); #plot mode shape 4
# vfo.plot_modeshape(modenumber=5, scale=1); #plot mode shape 5
# vfo.plot_modeshape(modenumber=6, scale=1); #plot mode shape 6

# gravity analysis-------------------------------------------------------------
#module frame, 0.1 is used to account for 10 steps in analyze(10)
g_mfCorne=-0.1*mass_mf*g*(84.0/4/2+41.26/2/2)*in2m;  #nodes at corner
g_mfMidEW=-0.1*mass_mf*g*(41.26/2)*in2m;             #nodes at middle of E-W direction
g_mfMidNS=-0.1*mass_mf*g*(84.0/4)*in2m;              #nodes at middle of N-S direction

#module, 0.1 is used to account for 10 steps in analyze(10)
g_m=84.0*in2m*41.26*in2m*h*rho_m*g;
g_mCo=-0.1*g_m/32;     #corner, 4 in total
g_mEd=-0.1*g_m/32*2;   #edge, 8 in total
g_mIn=-0.1*g_m/32*4;   #internal, 3 in total

timeSeries('Linear',10000);
pattern('Plain', 10000, 10000);

for i in range (0,1):
    for j in range (0,6):
        load(501+i*700+j*3, *[0.0, 0.0, g_mCo+g_mfCorne, 0.0, 0.0, 0.0]);
        load(502+i*700+j*3, *[0.0, 0.0, g_mEd+g_mfMidEW, 0.0, 0.0, 0.0]);
        load(503+i*700+j*3, *[0.0, 0.0, g_mCo+g_mfCorne, 0.0, 0.0, 0.0]);
        load(601+i*700+j*3, *[0.0, 0.0, g_mEd+g_mfMidNS, 0.0, 0.0, 0.0]);
        load(602+i*700+j*3, *[0.0, 0.0, g_mIn, 0.0, 0.0, 0.0]);
        load(603+i*700+j*3, *[0.0, 0.0, g_mEd+g_mfMidNS, 0.0, 0.0, 0.0]);
        load(701+i*700+j*3, *[0.0, 0.0, g_mEd+g_mfMidNS, 0.0, 0.0, 0.0]);
        load(702+i*700+j*3, *[0.0, 0.0, g_mIn, 0.0, 0.0, 0.0]);
        load(703+i*700+j*3, *[0.0, 0.0, g_mEd+g_mfMidNS, 0.0, 0.0, 0.0]);
        load(801+i*700+j*3, *[0.0, 0.0, g_mEd+g_mfMidNS, 0.0, 0.0, 0.0]);
        load(802+i*700+j*3, *[0.0, 0.0, g_mIn, 0.0, 0.0, 0.0]);
        load(803+i*700+j*3, *[0.0, 0.0, g_mEd+g_mfMidNS, 0.0, 0.0, 0.0]);
        load(901+i*700+j*3, *[0.0, 0.0, g_mCo+g_mfCorne, 0.0, 0.0, 0.0]);
        load(902+i*700+j*3, *[0.0, 0.0, g_mEd+g_mfMidEW, 0.0, 0.0, 0.0]);
        load(903+i*700+j*3, *[0.0, 0.0, g_mCo+g_mfCorne, 0.0, 0.0, 0.0]);

# define ANALYSIS PARAMETERS
constraints('Plain');  # how it handles boundary conditions
numberer('RCM');	   # renumber dof's to minimize band-width 
system('UmfPack'); # how to store and solve the system of equations in the analysis
test('NormDispIncr', 1.0e-08, 1000); # determine if convergence has been achieved at the end of an iteration step
algorithm('Linear');
integrator('LoadControl', 1)
analysis('Static');	# define type of analysis static or transient
analyze(10);
print('Finished')

# wind analysis----------------------------------------------------------------
# load wind tunnel test DATA
CpList=[None]*12;
dtNormList=[None]*12;
filename = "../../../RWDI/Wind Tunnel Data/tilt_n30deg.hdf5"
with h5py.File(filename, "r") as f:
    # get the key of interest; may or may NOT be a group
    a_group_key0 = list(f.keys())[0]
    a_group_key30 = list(f.keys())[1]
    a_group_key60 = list(f.keys())[2]
    a_group_key90 = list(f.keys())[3]
    # get the object names in the group and returns as a list
    objNames = list(f[a_group_key0])
    # preferred methods to get dataset values
    CpList[0] = f[a_group_key0]['Row1'][()]  # returns as a numpy array
    CpList[1] = f[a_group_key30]['Row1'][()]
    CpList[2] = f[a_group_key60]['Row1'][()]
    CpList[3] = f[a_group_key90]['Row1'][()]
    dtNormList[0] = f[a_group_key0]['dtNorm'][()]
    dtNormList[1] = f[a_group_key30]['dtNorm'][()]
    dtNormList[2] = f[a_group_key60]['dtNorm'][()]
    dtNormList[3] = f[a_group_key90]['dtNorm'][()]

filename = "../../../RWDI/Wind Tunnel Data/tilt_p30deg.hdf5"
with h5py.File(filename, "r") as f:
    # get the key of interest; may or may NOT be a group
    a_group_key180 = list(f.keys())[0]
    a_group_key150 = list(f.keys())[1]
    a_group_key120 = list(f.keys())[2]
    # get the object names in the group and returns as a list
    objNames = list(f[a_group_key180])
    # preferred methods to get dataset values
    CpList[6] = f[a_group_key180]['Row7'][()]
    CpList[5] = f[a_group_key150]['Row7'][()]
    CpList[4] = f[a_group_key120]['Row7'][()]
    dtNormList[6] = f[a_group_key180]['dtNorm'][()]
    dtNormList[5] = f[a_group_key150]['dtNorm'][()]
    dtNormList[4] = f[a_group_key120]['dtNorm'][()]

for i in range(7,12):
    CpList[i]=CpList[12-i]; #may need deep copy
    dtNormList[i]=dtNormList[12-i];

dirList=['0','30','60','90','120','150','180','210','240','270','300','330'];

# specify wind direction and speed for analysis
i=0;        #direction
Uasce=80.0; #mph, 3-sec gust at 10m height
U=Uasce*0.44704/1.52/1.15; #convert mph to m/s, to hourly mean, to 3m height
Cp=CpList[i];
dtNorm=dtNormList[i];
dirID=dirList[i];

L=169.25*in2m;
dt=dtNorm*L/U;
rho_air=1.226;
p=0.5*rho_air*U*U*Cp[1000:None,:];

f_m=84.0*in2m*41.26*in2m*p;
f_mList=f_m.T.tolist();
f_mCo=1.0/32;     #corner, 8 in total for one module
f_mEd=1.0/32*2;   #edge, 8 in total
f_mIn=1.0/32*4;   #internal, 2 in total

# tap ID 13
tap=12;
timeSeries('Path',tap,'-dt',dt,'-values',*f_mList[tap],'-prependZero');
pattern('Plain',tap,tap);

for j in range (0,3):
    load(701+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(702+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(703+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(801+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(802+j*3, *[f_mIn*math.sin(30/180*math.pi), 0.0, -f_mIn*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(803+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(901+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(902+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(903+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);

# tap ID 14
tap=13;
timeSeries('Path',tap,'-dt',dt,'-values',*f_mList[tap],'-prependZero');
pattern('Plain',tap,tap);

for j in range (0,3):
    load(501+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(502+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(503+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(601+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(602+j*3, *[f_mIn*math.sin(30/180*math.pi), 0.0, -f_mIn*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(603+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(701+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(702+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(703+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);

# tap ID 17
tap=16;
timeSeries('Path',tap,'-dt',dt,'-values',*f_mList[tap],'-prependZero');
pattern('Plain',tap,tap);

for j in range (3,6):
    load(701+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(702+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(703+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(801+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(802+j*3, *[f_mIn*math.sin(30/180*math.pi), 0.0, -f_mIn*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(803+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(901+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(902+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(903+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    
# tap ID 18
tap=17;
timeSeries('Path',tap,'-dt',dt,'-values',*f_mList[tap],'-prependZero');
pattern('Plain',tap,tap);

for j in range (3,6):
    load(501+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(502+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(503+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(601+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(602+j*3, *[f_mIn*math.sin(30/180*math.pi), 0.0, -f_mIn*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(603+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(701+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(702+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
    load(703+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);

# Define RECORDERS ------------------------------------------------------------
eleRec=list(range(501,513))+list(range(601,613));
recorder('Element', '-file', f'{dataDir}/test6PeleForce.out', '-time', '-ele', *eleRec, 'localForces');
recorder('Node', '-file', f'{dataDir}/test6PnodeDisp.out', '-time', '-node', *allNodeTags, '-dof', *[1, 2, 3, 4, 5, 6,], 'disp');

# define DAMPING
rayleigh(0.0,0.0,0.0,2*0.02/(eigenValues[0]**0.5));

# define ANALYSIS PARAMETERS---------------------------------------------------
wipeAnalysis();
constraints('Plain');  # how it handles boundary conditions
numberer('RCM');	   # renumber dof's to minimize band-width 
system('UmfPack');     # how to store and solve the system of equations in the analysis
test('NormDispIncr', 1.0e-08, 1000); # determine if convergence has been achieved at the end of an iteration step
algorithm('KrylovNewton');
integrator('Newmark', 0.5, 0.25);
analysis('Transient'); # define type of analysis static or transient
ok = analyze(500, 0.02);
print('Finished')

wipe()
vfo.plot_deformedshape(model="solarPanel", loadcase="static", scale=10)
#------------------------------------------------------------------------------