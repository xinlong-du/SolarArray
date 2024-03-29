# -----------------------------------------------------------------------------
# Solar PV table (two 2x11 CS-400W)
# Units: m, N, kg, s, N/m2, kg/m3
# Xinlong Du, 2023
# -----------------------------------------------------------------------------
from openseespy.opensees import *
import numpy as np
import math
import h5py

# visulization
import vfo.vfo as vfo

from plotFunctions import localForcePlot
from plotFunctions import globalDispPlot
from plotFunctions import localYdispPlot
from plotFunctions import springResPlot

def runDynamicAnalysis(Cp,U,dtNorm,dirID,spdID):
    #%% SET UP ----------------------------------------------------------------------
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
    E0=7.0e6;
    b=0.0001;
    uniaxialMaterial('Steel01', 1, Fy, E0, b)
    
    E=2.55e7;
    Fy=-1.0e6;
    gap=-1.8e-3;
    eta=0.99999;
    uniaxialMaterial('ElasticPPGap', 2, E, Fy, gap, eta)
    
    uniaxialMaterial('Parallel', 101, *[1,2])
    
    # material for dispY-----------------------------------------------------------
    Fy=2000.0;
    E0=6.0e6;
    b=0.45;
    uniaxialMaterial('Steel01', 3, Fy, E0, b)
    
    E=7.7e7;
    Fy=-1.0e6;
    gap=-2.7e-4;
    eta=0.99999;
    uniaxialMaterial('ElasticPPGap', 4, E, Fy, gap, eta)
    
    uniaxialMaterial('Parallel', 102, *[3,4])
    
    # material for dispZ-----------------------------------------------------------
    Fy=1600.0;
    E0=7.0e6;
    b=0.001;
    uniaxialMaterial('Steel01', 103, Fy, E0, b)
    
    # material for rotX-----------------------------------------------------------
    Fy=17.0;
    E0=2.9e4;
    b=0.13;
    uniaxialMaterial('Steel01', 5, Fy, E0, b)
    
    E=1.0e4;
    Fy=1.0e7;
    gap=0.0088;
    eta=0.99999;
    uniaxialMaterial('ElasticPPGap', 6, E, Fy, gap, eta)
    
    E=3.5e4;
    Fy=-1.0e3;
    gap=-0.0075;
    eta=0.99999;
    uniaxialMaterial('ElasticPPGap', 7, E, Fy, gap, eta)
    
    uniaxialMaterial('Parallel', 104, *[5,6,7])
    
    # material for rotY-----------------------------------------------------------
    Fy=28.0;
    E0=8.9e3;
    b=0.005;
    uniaxialMaterial('Steel01', 9, Fy, E0, b)
    
    E=5.6e3;
    Fy=30.0;
    gap=0.027;
    eta=0.1;
    uniaxialMaterial('ElasticPPGap', 10, E, Fy, gap, eta)
    
    E=5.0e3;
    Fy=-30;
    gap=-0.017;
    eta=0.09;
    uniaxialMaterial('ElasticPPGap', 11, E, Fy, gap, eta)
    
    uniaxialMaterial('Parallel', 105, *[9,10,11])
    
    # material for rotZ-----------------------------------------------------------
    Fy=15.0;
    E0=5.0e3;
    b=0.2;
    uniaxialMaterial('Steel01', 12, Fy, E0, b)
    
    E=8.1e3;
    Fy=1.0e7;
    gap=0.02;
    eta=0.99999;
    uniaxialMaterial('ElasticPPGap', 13, E, Fy, gap, eta)
    
    alpha=0.05;
    ko=100;
    n=2;
    gamma=0.7;
    beta=0.5;
    Ao=5;
    deltaA=-200;
    deltaNu=1600;
    deltaEta=0.1;
    uniaxialMaterial('BoucWen', 14, alpha, ko, n, gamma, beta, Ao, deltaA, deltaNu, deltaEta)
    
    uniaxialMaterial('Parallel', 106, *[12,13,14])
    
    # define NODES-----------------------------------------------------------------
    yRack=[22.5300*in2m, 285.0900*in2m];
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
        for j in range (0,12):
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
            node(1001+700*i+3*j,(-105.5808+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (31.0611+43.2185*i)*in2m)
            node(1002+700*i+3*j,(-105.5808+74.5730*i)*in2m, (-78.6200+42.26*j)*in2m, (31.0611+43.2185*i)*in2m)
            node(1003+700*i+3*j,(-105.5808+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (31.0611+43.2185*i)*in2m)
            node(1101+700*i+3*j, (-69.2423+74.5730*i)*in2m, (-99.2500+42.26*j)*in2m, (52.1209+43.2185*i)*in2m)
            node(1102+700*i+3*j, (-69.2423+74.5730*i)*in2m, (-78.6200+42.26*j)*in2m, (52.1209+43.2185*i)*in2m)
            node(1103+700*i+3*j, (-69.2423+74.5730*i)*in2m, (-57.9900+42.26*j)*in2m, (52.1209+43.2185*i)*in2m)
    
    # intersection of external braces
    node(1901, 0.0, 153.8100*in2m, 51.6250*in2m)
    
    # define BOUNDARY CONDITIONS---------------------------------------------------
    fix(101, 1, 1, 1, 1, 1, 1);  
    fix(105, 1, 1, 1, 1, 1, 1);
    fix(201, 1, 1, 1, 1, 1, 1);  
    fix(205, 1, 1, 1, 1, 1, 1);
    
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
    nPurlin=[[0]*38]*4; #nodes of purlins
    rowPurlin=[1001,1101,1701,1801];
    nRafter=[11,10,9,8];
    for i in range (0,4):
        nPurlin[i] = list(range(rowPurlin[i],rowPurlin[i]+36));
        nPurlin[i].insert(28,200+nRafter[i])
        nPurlin[i].insert(8,100+nRafter[i])
    
    for i in range (0,4):
        for j in range (0,37):
            #                            elemID         nodeI          nodeJ
            element('elasticBeamColumn', i*100+501+j, *[nPurlin[i][j], nPurlin[i][j+1]], A_pu, Es, Gs, Jx_pu, Iy_pu, Iz_pu, purlinTransfTag, '-mass', mass_pu);
    
    # modules and module frames
    for i in range (0,2):
        for j in range (0,12):
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
            element('zeroLength', (24*i+21)*1000+j+1, *[1001+i*700+j*3, 601+i*700+j*3], '-mat', *[101,102,103,104,105,106], '-dir', *[1,2,3,4,5,6], '-orient', *vecx1, *vecyp);
            element('zeroLength', (24*i+22)*1000+j+1, *[1003+i*700+j*3, 603+i*700+j*3], '-mat', *[101,102,103,104,105,106], '-dir', *[1,2,3,4,5,6], '-orient', *vecx2, *vecyp);
            element('zeroLength', (24*i+23)*1000+j+1, *[1101+i*700+j*3, 801+i*700+j*3], '-mat', *[101,102,103,104,105,106], '-dir', *[1,2,3,4,5,6], '-orient', *vecx1, *vecyp);
            element('zeroLength', (24*i+24)*1000+j+1, *[1103+i*700+j*3, 803+i*700+j*3], '-mat', *[101,102,103,104,105,106], '-dir', *[1,2,3,4,5,6], '-orient', *vecx2, *vecyp);
            
    # external braces
    for i in range(0,2):
        element('elasticBeamColumn', 49000+1000*i+1, *[(i+1)*100+3, 1901], A_eb, Es, Gs, Jx_eb, Iy_eb, Iz_eb, ebTransfTag, '-mass', mass_eb, '-releasez', 1, 'releasey', 1);
        element('elasticBeamColumn', 49000+1000*i+2, *[(i+1)*100+4, 1901], A_eb, Es, Gs, Jx_eb, Iy_eb, Iz_eb, ebTransfTag, '-mass', mass_eb, '-releasez', 1, 'releasey', 1);
    
    allNodeTags=getNodeTags();
    alleleTags=getEleTags();
    
    # render the model
    vfo.createODB(model="tableCS400W", loadcase="windDir0", Nmodes=6, deltaT=1)
    vfo.plot_model()
    
    # eigen ANALYSIS---------------------------------------------------------------
    eigenValues = eigen(12);
    omega = np.sqrt(eigenValues);
    freq = omega/(2*math.pi);
    
    vfo.plot_modeshape(modenumber=1, scale=5); #plot mode shape 1
    vfo.plot_modeshape(modenumber=2, scale=5); #plot mode shape 2
    vfo.plot_modeshape(modenumber=3, scale=5); #plot mode shape 3
    vfo.plot_modeshape(modenumber=4, scale=5); #plot mode shape 4
    # vfo.plot_modeshape(modenumber=5, scale=5); #plot mode shape 5
    # vfo.plot_modeshape(modenumber=6, scale=5); #plot mode shape 6
    
    #%% gravity loads
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
    
    for i in range (0,2):
        for j in range (0,12):
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
    
    # define ANALYSIS PARAMETERS---------------------------------------------------
    constraints('Plain');  # how it handles boundary conditions
    numberer('RCM');	   # renumber dof's to minimize band-width 
    system('UmfPack'); # how to store and solve the system of equations in the analysis
    test('NormDispIncr', 1.0e-08, 1000); # determine if convergence has been achieved at the end of an iteration step
    algorithm('KrylovNewton');
    integrator('LoadControl', 1)
    analysis('Static');	# define type of analysis static or transient
    analyze(10);
    print('Gravity Finished')
    
    #wipe()
    #vfo.plot_deformedshape(model="tableCS400W", loadcase="windDir0", scale=20)
    loadConst('-time', 0.0)

    #%% define LOADS---------------------------------------------------------------
    L=169.25*in2m;
    dt=dtNorm*L/U;
    rho_air=1.226;
    p=0.5*rho_air*U*U*Cp[1000:None,:];
    f_m=84.0*in2m*41.26*in2m*p;
    
    p_m=[None]*24; #use a mean pressure for each module
    p_m[0]=(f_m[:,0]+f_m[:,1])/2.0;
    p_m[1]=(f_m[:,2]+f_m[:,3])/2.0;
    p_m[2]=(f_m[:,0]+f_m[:,1])/2.0;
    p_m[3]=(f_m[:,2]+f_m[:,3])/2.0;
    
    p_m[4]=(f_m[:,4]+f_m[:,5])/2.0;
    p_m[5]=(f_m[:,6]+f_m[:,7])/2.0;
    p_m[6]=(f_m[:,4]+f_m[:,5])/2.0;
    p_m[7]=(f_m[:,6]+f_m[:,7])/2.0;
    
    p_m[8]=(f_m[:,8]+f_m[:,9])/2.0;
    p_m[9]=(f_m[:,10]+f_m[:,11])/2.0;
    p_m[10]=(f_m[:,8]+f_m[:,9])/2.0;
    p_m[11]=(f_m[:,10]+f_m[:,11])/2.0;
    p_m[12]=(f_m[:,8]+f_m[:,9])/2.0;
    p_m[13]=(f_m[:,10]+f_m[:,11])/2.0;
    p_m[14]=(f_m[:,8]+f_m[:,9])/2.0;
    p_m[15]=(f_m[:,10]+f_m[:,11])/2.0;
    
    p_m[16]=(f_m[:,12]+f_m[:,13])/2.0;
    p_m[17]=(f_m[:,14]+f_m[:,15])/2.0;
    p_m[18]=(f_m[:,12]+f_m[:,13])/2.0;
    p_m[19]=(f_m[:,14]+f_m[:,15])/2.0;
    p_m[20]=(f_m[:,12]+f_m[:,13])/2.0;
    p_m[21]=(f_m[:,14]+f_m[:,15])/2.0;
    p_m[22]=(f_m[:,12]+f_m[:,13])/2.0;
    p_m[23]=(f_m[:,14]+f_m[:,15])/2.0;
    
    p_mList=[l.tolist() for l in p_m];
    f_mCo=1.0/32;     #corner, 4 in total for one module
    f_mEd=1.0/32*2;   #edge, 8 in total
    f_mIn=1.0/32*4;   #internal, 3 in total
    
    # +Tilt
    k=0;
    for j in range (0,12):
        for i in range (1,-1,-1):
            timeSeries('Path',k,'-dt',dt,'-values',*p_mList[k],'-prependZero');
            pattern('Plain',k,k);
            load(501+i*700+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(502+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(503+i*700+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(601+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(602+i*700+j*3, *[f_mIn*math.sin(30/180*math.pi), 0.0, -f_mIn*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(603+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(701+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(702+i*700+j*3, *[f_mIn*math.sin(30/180*math.pi), 0.0, -f_mIn*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(703+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(801+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(802+i*700+j*3, *[f_mIn*math.sin(30/180*math.pi), 0.0, -f_mIn*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(803+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(901+i*700+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(902+i*700+j*3, *[f_mEd*math.sin(30/180*math.pi), 0.0, -f_mEd*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            load(903+i*700+j*3, *[f_mCo*math.sin(30/180*math.pi), 0.0, -f_mCo*math.cos(30/180*math.pi), 0.0, 0.0, 0.0]);
            k=k+1;
    
    # define RECORDERS ------------------------------------------------------------
    nodeRec=list(range(1701,1737))+list(range(1801,1837))+list(range(1301,1337))+list(range(1401,1437))+list(range(1501,1537));
    eleRec=list(range(701,738))+list(range(801,838));
    springRec=list(range(45001,45013))+list(range(46001,46013))+list(range(47001,47013))+list(range(48001,48013));
    recorder('Node', '-file', f'{dataDir}/testAllCases3/'+'dir'+dirID+'spd'+spdID+'nodeDisp.out', '-time', '-node', *nodeRec, '-dof', *[1, 2, 3, 4, 5, 6,], 'disp');
    recorder('Element', '-file', f'{dataDir}/testAllCases3/'+'dir'+dirID+'spd'+spdID+'eleForce.out', '-time', '-ele', *eleRec, 'localForces');
    recorder('Element', '-file', f'{dataDir}/testAllCases3/'+'dir'+dirID+'spd'+spdID+'springResp.out', '-time', '-ele', *springRec, 'deformationsANDforces');
    
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
    ok = analyze(750, 0.02);
    print('Finished')
    
    #%% output forces on joints at the last time step, used for verification-------
    # element resisting forces for purlins
    ef813end=eleForce(813);
    ef813endLoc=eleResponse(813, 'localForces')
    ef814end=eleForce(814);
    ef814endLoc=eleResponse(814, 'localForces')
    nf1813end=np.array(ef813endLoc[6:12])+np.array(ef814endLoc[0:6]);
    
    wipe()
    #%% defomed shape and animation------------------------------------------------
    #vfo.plot_deformedshape(model="tableCS400W", loadcase="windDir0", scale=20)
    #ani = vfo.animate_deformedshape(model="tableCS400W", loadcase="windDir0", speedup=4, scale=50, gifname="tableCS400W_Dynamic")
    
    #%% plot response of springs
    # file_name='./Data/tableCS400WdefANDfor.out';
    # springRes=np.loadtxt(file_name);
    # for i in range(len(springRec)):
    #     springResPlot(springRes[:,i*12+1:i*12+13],str(springRec[i]));
    
    #%% calculate time series of forces on joints----------------------------------
    # file_name = './Data/tableCS400Weles.out'
    # eleForces = np.loadtxt(file_name)
    # ef813=eleForces[:,35*12+1:36*12+1];
    # ef814=eleForces[:,36*12+1:37*12+1];
    # nf1813=ef813[:,6:12]+ef814[:,0:6];

#%% load wind tunnel test DATA
#this is for the south most row (first row for pressure, last row for suction)
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
    # switch columns of Cp to account for different pressure tap ID numbering for positive and negative tilts
    # the code for applying wind forces are for positive tilt, so need to switch columns for negative tilts
    idx=[3,2,1,0,7,6,5,4,11,10,9,8,15,14,13,12,19,18,17,16,23,22,21,20,27,26,25,24];
    Cp0 = f[a_group_key0]['Row1'][()]  # returns as a numpy array
    CpList[0] = Cp0[:,idx]
    Cp1 = f[a_group_key30]['Row1'][()]
    CpList[1] = Cp1[:,idx]
    Cp2 = f[a_group_key60]['Row1'][()]
    CpList[2] = Cp2[:,idx]
    Cp3 = f[a_group_key90]['Row1'][()]
    CpList[3] = Cp3[:,idx]
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

#%% load wind speed information
filename='../../WindAnalysis/FiguresDeg30TX/CTspdPb30.txt';
dirSpdDura=np.loadtxt(filename);
dirSpd=0.44704/1.52/1.18*dirSpdDura[:,0]; #convert mph to 3-sec m/s to hourly m/s to 3m-height m/s
dirList=['0','30','60','90','120','150','180','210','240','270','300','330'];

#%% run analysis
for i in range(0,12):
    UList=dirSpd[i*10:i*10+10];
    Cp=CpList[i];
    dtNorm=dtNormList[i];
    dirID=dirList[i];
    for j in range(0,10):
        U=UList[j]; 
        runDynamicAnalysis(Cp,U,dtNorm,dirID,str(j))