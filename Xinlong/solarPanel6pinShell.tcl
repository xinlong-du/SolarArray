# Lateral buckling of two simply supported C purlins connected by six solar panels
# subjected to major axis bending (uniform bending with Cb=1)
# Units: N, mm, tonne=1000kg, s, N/mm2, tonne/mm3
# Xinlong Du, UC Berkeley, 2023
# xinlongdu@berkeley.edu
# ----------------------------------------------------------------------------
set systemTime [clock seconds] 
puts "Starting Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"
set startTime [clock clicks -milliseconds];
#---------------------------------------------------------------------------
wipe; # clear opensees model
source DisplayPlane.tcl;		# procedure for displaying a plane in model
source DisplayModel3D.tcl;		# procedure for displaying 3D perspectives of model
source Csection.tcl;   # C-section with round corners
model basic -ndm 3 -ndf 6;# 3 dimensions, 7 dof per node
set dir solarPanel;  #set dir lateral buckling of C section
file mkdir $dir;          # create data directory

# define GEOMETRY
#-------------------------------------------------------------
set in2mm 25.4;

for {set i 0} {$i<6} {incr i 1} {
    node [expr 101+3*$i] [expr   (0.0+42.26*$i)*$in2mm] -50.0 [expr (21.0*$in2mm-48.6907)]
    node [expr 103+3*$i] [expr (41.26+42.26*$i)*$in2mm] -50.0 [expr (21.0*$in2mm-48.6907)]
    node [expr 201+3*$i] [expr   (0.0+42.26*$i)*$in2mm] -50.0 [expr (63.0*$in2mm-48.6907)]
    node [expr 203+3*$i] [expr (41.26+42.26*$i)*$in2mm] -50.0 [expr (63.0*$in2mm-48.6907)]

    node [expr 301+3*$i] [expr   (0.0+42.26*$i)*$in2mm] -50.0 [expr 21.0*$in2mm]
    node [expr 303+3*$i] [expr (41.26+42.26*$i)*$in2mm] -50.0 [expr 21.0*$in2mm]
    node [expr 401+3*$i] [expr   (0.0+42.26*$i)*$in2mm] -50.0 [expr 63.0*$in2mm]
    node [expr 403+3*$i] [expr (41.26+42.26*$i)*$in2mm] -50.0 [expr 63.0*$in2mm]

    node [expr 501+3*$i] [expr   (0.0+42.26*$i)*$in2mm] 0.0 [expr 0.0*$in2mm]
    node [expr 502+3*$i] [expr (20.63+42.26*$i)*$in2mm] 0.0 [expr 0.0*$in2mm]
    node [expr 503+3*$i] [expr (41.26+42.26*$i)*$in2mm] 0.0 [expr 0.0*$in2mm]
    node [expr 601+3*$i] [expr   (0.0+42.26*$i)*$in2mm] 0.0 [expr 21.0*$in2mm]
    node [expr 602+3*$i] [expr (20.63+42.26*$i)*$in2mm] 0.0 [expr 21.0*$in2mm]
    node [expr 603+3*$i] [expr (41.26+42.26*$i)*$in2mm] 0.0 [expr 21.0*$in2mm]
    node [expr 701+3*$i] [expr   (0.0+42.26*$i)*$in2mm] 0.0 [expr 42.0*$in2mm]
    node [expr 702+3*$i] [expr (20.63+42.26*$i)*$in2mm] 0.0 [expr 42.0*$in2mm]
    node [expr 703+3*$i] [expr (41.26+42.26*$i)*$in2mm] 0.0 [expr 42.0*$in2mm]
    node [expr 801+3*$i] [expr   (0.0+42.26*$i)*$in2mm] 0.0 [expr 63.0*$in2mm]
    node [expr 802+3*$i] [expr (20.63+42.26*$i)*$in2mm] 0.0 [expr 63.0*$in2mm]
    node [expr 803+3*$i] [expr (41.26+42.26*$i)*$in2mm] 0.0 [expr 63.0*$in2mm]
    node [expr 901+3*$i] [expr   (0.0+42.26*$i)*$in2mm] 0.0 [expr 84.0*$in2mm]
    node [expr 902+3*$i] [expr (20.63+42.26*$i)*$in2mm] 0.0 [expr 84.0*$in2mm]
    node [expr 903+3*$i] [expr (41.26+42.26*$i)*$in2mm] 0.0 [expr 84.0*$in2mm]

    node [expr 1001+3*$i] [expr   (0.0+42.26*$i)*$in2mm] 0.0 [expr 21.0*$in2mm]
    node [expr 1003+3*$i] [expr (41.26+42.26*$i)*$in2mm] 0.0 [expr 21.0*$in2mm]
    node [expr 1101+3*$i] [expr   (0.0+42.26*$i)*$in2mm] 0.0 [expr 63.0*$in2mm]
    node [expr 1103+3*$i] [expr (41.26+42.26*$i)*$in2mm] 0.0 [expr 63.0*$in2mm]
}

node 100 [expr   -5.0*$in2mm] -50.0 [expr (21.0*$in2mm-48.6907)]
node 119 [expr 257.56*$in2mm] -50.0 [expr (21.0*$in2mm-48.6907)]
node 200 [expr   -5.0*$in2mm] -50.0 [expr (63.0*$in2mm-48.6907)]
node 219 [expr 257.56*$in2mm] -50.0 [expr (63.0*$in2mm-48.6907)]

# define BOUNDARY CONDITIONS (single point constraint)
#----------------------------------------------------------
# NodeID,dispX,dispY,dispZ,rotX,RotY,RotZ, Warping 
fix 100 0 1 1 1 0 0; #temp, need to be modified
fix 109 1 0 0 0 0 0;
fix 119 0 1 1 1 0 0;
fix 200 0 1 1 1 0 0;
fix 209 1 0 0 0 0 0;
fix 219 0 1 1 1 0 0; 			
#-------------------------------------------------------
set startNode1  100
set middleNode1 109
set endNode1    119
set startNode2  200
set middleNode2 209
set endNode2    219

# Define ELEMENTS & SECTIONS
#-------------------------------------------------------------
set ColSecTagFiber 1;# assign a tag number to the column section
set SecTagTorsion 70;# assign a tag number for torsion 
set BeamSecTag 3
 
# define MATERIALS
#----------------------------------------------------------------
set IDsteel 1; # Identifier for material
set Fy 379.0; # Yield stress -Use very large yield stress for elastic buckling analysis
set Es 200000.0; # Elastic modulus
set Bs 0.001;		# strain-hardening ratio 
set G [expr $Es/(2*(1+0.3))]; # Shear modulus
uniaxialMaterial Steel01 $IDsteel $Fy $Es $Bs;	# build steel01 material

set Em 70000.0;       #Glass Young's modulus for module
set nu_m 0.22;              #Glass Poisson's ratio
set rho_m [expr 2500.0e-12];#Glass mass density
set Emf 68000.3;      #Aluminum Young's modules (module frame)
set Gmf [expr $Emf/2./(1+0.3)];#Shear modulus of aluminum
set rho_mf [expr 2690.0e-12];  #Aluminum mass density
puts "rho_m $rho_m"
puts "rho_mf $rho_mf"

# define SECTION DIMENSION AND FIBER DIVISION
#----------------------------------------------------------------
# SECTION properties for module frames
set A_mf 168.07;    #cross-sectional area
set Iz_mf 21828.0;  #second moment of area about the local z-axis
set Iy_mf 9841.7;   #second moment of area about the local y-axis
#torsional moment of inertia of section: hollow section     + open section
set Jx_mf [expr (4*319.8657*319.8657*(1.37+1.67+1.67+1.42)/4/74.21+11.96*2.01**3/3+4.96*1.36**3/3+17.86*1.42**3/3)];
set mass_mf [expr $A_mf*$rho_mf];     #mass per unit length

# SECTION properties for rigid offsets
set A_ro  [expr $A_mf*100.0];    #cross-sectional area
set Iz_ro [expr $Iz_mf*10000.0]; #second moment of area about the local z-axis
set Iy_ro [expr $Iz_mf*10000.0]; #second moment of area about the local y-axis
set Jx_ro [expr $Jx_mf*10000.0];

# SECTION properties for module
set moduleSecTag 100;
set h 4.96; #depth of module
section ElasticMembranePlateSection $moduleSecTag $Em $nu_m $h $rho_m;

set D 100.0;    # Depth
set B 50.0;     # Flange width
set L 16.5;   # Lip
set t 3.5;    # section thickness
set r 3.0;    # corner radius (to inside face)
set nfdw 50;    # number of fibers along web depth
set nfbf 40;    # number of fibers along flange
set nfL 10;   # number of fibers along lip
set nfC 4;    # number of fibers along circumferance of corners
set nft 1;    # number of fibers through thickness

# define FIBER SECTION, TORSION SECTION & TRANSFORMATION
#-----------------------------------------------------------------
set shearCoord [Csection $ColSecTagFiber $IDsteel $D $B $L $t $r $nfdw $nfbf $nfL $nfC $nft];
set z0 [lindex $shearCoord 0 0];  #z-coord of shear center w.r.t centroid of section
set y0 [lindex $shearCoord 1 0];  #y-coord of shear center w.r.t centroid of section
set J  [lindex $shearCoord 2 0];  #Torsional constant
set GJ [expr $G*$J];
uniaxialMaterial Elastic $SecTagTorsion $GJ ; # create torsion section
section Aggregator $BeamSecTag $SecTagTorsion T -section $ColSecTagFiber ;

set numIntgrPts 5; # number of integration points along each element
set BeamTransfTag 1;# associate a tag to column transformation			   
geomTransf Corotational $BeamTransfTag 0 0 1;# define geometric transformation: performs a corotational geometric
set rafterTransfTag 2;# associate a tag to module frame transformation, parallel to rafter			   
geomTransf Corotational $rafterTransfTag 1 0 0;# define geometric transformation: performs a corotational geometric
#transformation of beam stiffness and resisting force from the basic system to the global-coordinate system
puts $y0;
puts $z0;
set cy 0.0;
set cz $z0;
set omg 0.0;
puts $cy;
puts $cz;
# Define ELEMENTS
#-------------------------------------------------------------
set nPurlin1 {100 101 103 104 106 107 109 110 112 113 115 116 118 119}; #nodes of purlin # 1
set nPurlin2 {200 201 203 204 206 207 209 210 212 213 215 216 218 219}; #nodes of purlin # 2
set nPurlMf1 {301 303 304 306 307 309 310 312 313 315 316 318}; #nodes of purlin # 1
set nPurlMf2 {401 403 404 406 407 409 410 412 413 415 416 418}; #nodes of purlin # 2
set nModFra1 {601 603 604 606 607 609 610 612 613 615 616 618}; #nodes of module frame connecting to purlin # 1
set nModFra2 {801 803 804 806 807 809 810 812 813 815 816 818}; #nodes of module frame connecting to purlin # 2
set nMfPurl1 {1001 1003 1004 1006 1007 1009 1010 1012 1013 1015 1016 1018}; #nodes of module frame connecting to purlin # 1
set nMfPurl2 {1101 1103 1104 1106 1107 1109 1110 1112 1113 1115 1116 1118}; #nodes of module frame connecting to purlin # 2

# purlins
for {set i 0} {$i<13} {incr i 1} {
set elem1ID [expr $i+100];
set node1I [lindex $nPurlin1 $i];
set node1J [lindex $nPurlin1 [expr $i+1]];
set elem2ID [expr $i+200];
set node2I [lindex $nPurlin2 $i];
set node2J [lindex $nPurlin2 [expr $i+1]];
element dispBeamColumn $elem1ID $node1I $node1J $numIntgrPts $BeamSecTag $BeamTransfTag  $y0  $z0  $omg;
element dispBeamColumn $elem2ID $node2I $node2J $numIntgrPts $BeamSecTag $BeamTransfTag  $y0  $z0  $omg;	
} 

# rigid offset
for {set i 0} {$i<12} {incr i 1} {
set elem1ID [expr $i+300];
set node1I [lindex $nPurlin1 [expr $i+1]];
set node1J [lindex $nPurlMf1 $i];
set elem2ID [expr $i+400];
set node2I [lindex $nPurlin2 [expr $i+1]];
set node2J [lindex $nPurlMf2 $i];
set elem3ID [expr $i+500];
set node3I [lindex $nMfPurl1 $i];
set node3J [lindex $nPurlMf1 $i];
set elem4ID [expr $i+600];
set node4I [lindex $nMfPurl2 $i];
set node4J [lindex $nPurlMf2 $i];
element elasticBeamColumn $elem1ID $node1I $node1J $A_ro $Emf $Gmf $Jx_ro $Iy_ro $Iz_ro $rafterTransfTag 0.0 0.0 0.0 0.0;
element elasticBeamColumn $elem2ID $node2I $node2J $A_ro $Emf $Gmf $Jx_ro $Iy_ro $Iz_ro $rafterTransfTag 0.0 0.0 0.0 0.0;  
element elasticBeamColumn $elem3ID $node3I $node3J $A_ro $Emf $Gmf $Jx_ro $Iy_ro $Iz_ro $rafterTransfTag 0.0 0.0 0.0 0.0;
element elasticBeamColumn $elem4ID $node4I $node4J $A_ro $Emf $Gmf $Jx_ro $Iy_ro $Iz_ro $rafterTransfTag 0.0 0.0 0.0 0.0;
set node5 [lindex $nModFra1 $i];
set node6 [lindex $nModFra2 $i];
equalDOF $node3I $node5 1 2 3;
equalDOF $node4I $node6 1 2 3;
} 

for {set i 0} {$i<6} {incr i 1} {
    #                    elemID               node1          node2          node3          node4 counter-clockwise
    #if 0 {
    element ShellNLDKGQ [expr 1001+$i] [expr 501+$i*3] [expr 502+$i*3] [expr 602+$i*3] [expr 601+$i*3] $moduleSecTag;
    element ShellNLDKGQ [expr 2001+$i] [expr 601+$i*3] [expr 602+$i*3] [expr 702+$i*3] [expr 701+$i*3] $moduleSecTag;
    element ShellNLDKGQ [expr 3001+$i] [expr 701+$i*3] [expr 702+$i*3] [expr 802+$i*3] [expr 801+$i*3] $moduleSecTag;
    element ShellNLDKGQ [expr 4001+$i] [expr 801+$i*3] [expr 802+$i*3] [expr 902+$i*3] [expr 901+$i*3] $moduleSecTag;
    element ShellNLDKGQ [expr 5001+$i] [expr 502+$i*3] [expr 503+$i*3] [expr 603+$i*3] [expr 602+$i*3] $moduleSecTag;
    element ShellNLDKGQ [expr 6001+$i] [expr 602+$i*3] [expr 603+$i*3] [expr 703+$i*3] [expr 702+$i*3] $moduleSecTag;
    element ShellNLDKGQ [expr 7001+$i] [expr 702+$i*3] [expr 703+$i*3] [expr 803+$i*3] [expr 802+$i*3] $moduleSecTag;
    element ShellNLDKGQ [expr 8001+$i] [expr 802+$i*3] [expr 803+$i*3] [expr 903+$i*3] [expr 902+$i*3] $moduleSecTag;
    #}

    #if 0 {
    element elasticBeamColumn [expr 9001+$i]  [expr 901+$i*3] [expr 801+$i*3] $A_mf $Emf $Gmf $Jx_mf $Iy_mf $Iz_mf $rafterTransfTag 0.0 0.0 0.0 0.0;
    element elasticBeamColumn [expr 10001+$i] [expr 801+$i*3] [expr 701+$i*3] $A_mf $Emf $Gmf $Jx_mf $Iy_mf $Iz_mf $rafterTransfTag 0.0 0.0 0.0 0.0;
    element elasticBeamColumn [expr 11001+$i] [expr 701+$i*3] [expr 601+$i*3] $A_mf $Emf $Gmf $Jx_mf $Iy_mf $Iz_mf $rafterTransfTag 0.0 0.0 0.0 0.0;
    element elasticBeamColumn [expr 12001+$i] [expr 601+$i*3] [expr 501+$i*3] $A_mf $Emf $Gmf $Jx_mf $Iy_mf $Iz_mf $rafterTransfTag 0.0 0.0 0.0 0.0;
    element elasticBeamColumn [expr 13001+$i] [expr 903+$i*3] [expr 803+$i*3] $A_mf $Emf $Gmf $Jx_mf $Iy_mf $Iz_mf $rafterTransfTag 0.0 0.0 0.0 0.0;
    element elasticBeamColumn [expr 14001+$i] [expr 803+$i*3] [expr 703+$i*3] $A_mf $Emf $Gmf $Jx_mf $Iy_mf $Iz_mf $rafterTransfTag 0.0 0.0 0.0 0.0;
    element elasticBeamColumn [expr 15001+$i] [expr 703+$i*3] [expr 603+$i*3] $A_mf $Emf $Gmf $Jx_mf $Iy_mf $Iz_mf $rafterTransfTag 0.0 0.0 0.0 0.0;
    element elasticBeamColumn [expr 16001+$i] [expr 603+$i*3] [expr 503+$i*3] $A_mf $Emf $Gmf $Jx_mf $Iy_mf $Iz_mf $rafterTransfTag 0.0 0.0 0.0 0.0;
    element elasticBeamColumn [expr 17001+$i] [expr 901+$i*3] [expr 902+$i*3] $A_mf $Emf $Gmf $Jx_mf $Iy_mf $Iz_mf $BeamTransfTag 0.0 0.0 0.0 0.0;
    element elasticBeamColumn [expr 18001+$i] [expr 902+$i*3] [expr 903+$i*3] $A_mf $Emf $Gmf $Jx_mf $Iy_mf $Iz_mf $BeamTransfTag 0.0 0.0 0.0 0.0;
    element elasticBeamColumn [expr 19001+$i] [expr 501+$i*3] [expr 502+$i*3] $A_mf $Emf $Gmf $Jx_mf $Iy_mf $Iz_mf $BeamTransfTag 0.0 0.0 0.0 0.0;
    element elasticBeamColumn [expr 20001+$i] [expr 502+$i*3] [expr 503+$i*3] $A_mf $Emf $Gmf $Jx_mf $Iy_mf $Iz_mf $BeamTransfTag 0.0 0.0 0.0 0.0;
    #}
}

# Define DISPLAY -------------------------------------------------------------
DisplayModel3D DeformedShape;  # options: DeformedShape NodeNumbers ModeShape

# define initial Perturbation Load
#------------------------------------------------------------- 
pattern Plain 1 Linear {
  # NodeID, Fx, Fy, Fz, Mx, My, Mz, Bx
  load $middleNode1 0 0 0 -24.25 0 0;#+242.5 for positive branch; 
  load $middleNode2 0 0 0 -24.25 0 0;#+242.5 for positive branch;  
  }

constraints Plain;  # Constraint handler -how it handles boundary conditions
numberer Plain;	    # Renumbers DoF to minimize band-width (optimization)
system BandGeneral; # System of equations solver
test NormDispIncr 1.0e-8 50;
algorithm NewtonLineSearch 0.6;# use Newton's solution algorithm: updates tangent stiffness at every iteration
integrator LoadControl 1.0 ;
analysis Static; 
analyze 10; 

loadConst -time 0.0; # maintains the load constant for the reminder of the analysis and resets the current time to 0

# define RECORDERS
#-------------------------------------------------------------
recorder Node -file $dir/solarPanel1yield2OffsetPinShellTwNmoN2.out -time -node $middleNode1 -dof 1 2 3 4 5 6 disp;
recorder Node -file $dir/solarPanel2yield2OffsetPinShellTwNmoN2.out -time -node $middleNode2 -dof 1 2 3 4 5 6 disp;

# define second stage main Load (Moment at the two ends)
#------------------------------------------------------------- 
pattern Plain 2 Linear {
  # NodeID, Fx, Fy, Fz, Mx, My, Mz, Bx
  load $startNode1 0 0 0 0 0 [expr -4448.2216*25.4]; #the applied reference load is 1 kip-in
  load $endNode1   0 0 0 0 0 [expr  4448.2216*25.4];
  load $startNode2 0 0 0 0 0 [expr -4448.2216*25.4]; #the applied reference load is 1 kip-in
  load $endNode2   0 0 0 0 0 [expr  4448.2216*25.4];
}

#recorder plot $dir/solarPanel1yield2OffsetPinTwPmoP.out Displ-X 1200 10 300 300 -columns 5 1; # a window to plot the nodal displacements versus time

# define ANALYSIS PARAMETERS
#------------------------------------------------------------------------------------
constraints Plain;           # how it handles boundary conditions
numberer Plain;		     # renumber dof's to minimize band-width 
system BandGeneral;	     # how to store and solve the system of equations in the analysis
test NormDispIncr 1.0e-8 50 0; # determine if convergence has been achieved at the end of an iteration step
algorithm NewtonLineSearch 0.8;
set Dincr -0.000005; #Displacement increment/decrement 
set IDctrlNode $middleNode1;
set IDctrlDOF 4;
set Dmax 10
#integrator ArcLength 1.0 1.0; #Use this for curve with peak
#                              node        dof        init   Jd min    max
integrator DisplacementControl $IDctrlNode $IDctrlDOF $Dincr 1  $Dincr $Dincr
analysis Static	;			# define type of analysis static or transient
variable algorithmTypeStatic Newton
set ok [analyze 5000]; 
if {$ok != 0} {  
	# if analysis fails, we try some other stuff, performance is slower inside this loop
	set Dstep 0.0;
	set ok 0
	while {$Dstep <= 1.0 && $ok == 0} {
		set controlDisp [nodeDisp $IDctrlNode $IDctrlDOF ]
		set Dstep [expr $controlDisp/$Dmax]
		set ok [analyze 1];# this will return zero if no convergence problems were encountered
		if {$ok != 0} {;   # reduce step size if still fails to converge
			set Nk 4;  # reduce step size
			set DincrReduced [expr $Dincr/$Nk];
			integrator DisplacementControl  $IDctrlNode $IDctrlDOF $DincrReduced
			for {set ik 1} {$ik <=$Nk} {incr ik 1} {
				set ok [analyze 1];# this will return zero if no convergence problems were encountered
				if {$ok != 0} {
					puts "Trying Broyden .."
					algorithm Broyden 8
					set ok [analyze 1]
					algorithm $algorithmTypeStatic
				}
				if {$ok != 0} {
				        puts "Trying NewtonWithLineSearch .."
					algorithm NewtonLineSearch 0.8 
					set ok [analyze 1]
					algorithm $algorithmTypeStatic
				}
				if {$ok != 0} {;# stop if still fails to converge
				    return -1
				}; # end if
			}; # end for
			integrator DisplacementControl  $IDctrlNode $IDctrlDOF $Dincr;	# bring back to original increment
		}; # end if 
          };	# end while loop
  };      # end if ok !0
#-----------------------------------------------------------------------
#if 0 {
# define ANALYSIS PARAMETERS
#------------------------------------------------------------------------------------
constraints Plain;           # how it handles boundary conditions
numberer Plain;        # renumber dof's to minimize band-width 
system BandGeneral;      # how to store and solve the system of equations in the analysis
test NormDispIncr 1.0e-8 50 0; # determine if convergence has been achieved at the end of an iteration step
algorithm NewtonLineSearch 0.8;
set Dincr -0.0001; #Displacement increment/decrement 
set IDctrlNode $middleNode1;
set IDctrlDOF 4;
set Dmax 10
#integrator ArcLength 1.0 1.0; #Use this for curve with peak
#                              node        dof        init   Jd min    max
integrator DisplacementControl $IDctrlNode $IDctrlDOF $Dincr 1  $Dincr $Dincr
analysis Static ;     # define type of analysis static or transient
variable algorithmTypeStatic Newton
set ok [analyze 10000]; 
if {$ok != 0} {  
  # if analysis fails, we try some other stuff, performance is slower inside this loop
  set Dstep 0.0;
  set ok 0
  while {$Dstep <= 1.0 && $ok == 0} {
    set controlDisp [nodeDisp $IDctrlNode $IDctrlDOF ]
    set Dstep [expr $controlDisp/$Dmax]
    set ok [analyze 1];# this will return zero if no convergence problems were encountered
    if {$ok != 0} {;   # reduce step size if still fails to converge
      set Nk 4;  # reduce step size
      set DincrReduced [expr $Dincr/$Nk];
      integrator DisplacementControl  $IDctrlNode $IDctrlDOF $DincrReduced
      for {set ik 1} {$ik <=$Nk} {incr ik 1} {
        set ok [analyze 1];# this will return zero if no convergence problems were encountered
        if {$ok != 0} {
          puts "Trying Broyden .."
          algorithm Broyden 8
          set ok [analyze 1]
          algorithm $algorithmTypeStatic
        }
        if {$ok != 0} {
                puts "Trying NewtonWithLineSearch .."
          algorithm NewtonLineSearch 0.8 
          set ok [analyze 1]
          algorithm $algorithmTypeStatic
        }
        if {$ok != 0} {;# stop if still fails to converge
            return -1
        }; # end if
      }; # end for
      integrator DisplacementControl  $IDctrlNode $IDctrlDOF $Dincr;  # bring back to original increment
    }; # end if 
          };  # end while loop
  };      # end if ok !0
#-----------------------------------------------------------------------
#}
set finishTime [clock clicks -milliseconds];
puts "Time taken: [expr ($finishTime-$startTime)/1000] sec"
set systemTime [clock seconds] 
puts "Finished Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"





