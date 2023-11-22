#Flexural-Torsional Buckling of Channel column 
#---------------------------------------------------------------------------------------------
set systemTime [clock seconds] 
puts "Starting Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"
set startTime [clock clicks -milliseconds];
# ----------------------------------------------------------------------------
wipe;				# clear opensees model
source Csection.tcl;         # C section facing right
model basic -ndm 3 -ndf 7;	# 3 dimensions, 7 dof per node
set dir FlexuralTorsionalBuckling
file mkdir $dir;                # create data directory

# define GEOMETRY
#-------------------------------------------------------------
#Nodes, NodeNumber, xCoord, yCoord, zCoord
node 1	0	0	0
node 2	200	0	0
node 3	400	0	0
node 4	600	0	0
node 5	800	0	0
node 6	1000	0	0
node 7	1200	0	0
node 8	1400	0	0
node 9	1600	0	0
node 10	1800	0	0
node 11	2000	0	0
node 12	2200	0	0
node 13	2400	0	0
node 14	2600	0	0
node 15	2800	0	0
node 16	3000	0	0
node 17	3200	0	0
node 18	3400	0	0
node 19	3600	0	0
node 20	3800	0	0
node 21	4000	0	0
node 22	4200	0	0
node 23	4400	0	0
node 24	4600	0	0
node 25	4800	0	0
node 26	5000	0	0
node 27	5200	0	0
node 28	5400	0	0
node 29	5600	0	0
node 30	5800	0	0
node 31	6000	0	0

# define BOUNDARY CONDITIONS (single point constraint)
#----------------------------------------------------------
# NodeID,dispX,dispY,dispZ,rotX,RotY,RotZ, Warping  
fix 1 0 1 1 1 0 0 0;    
fix 16 1 0 0 0 0 0 0;
fix 31 0 1 1 1 0 0 0;
#-------------------------------------------------------------
set startNode 1
set middleNode 16
set endNode 31

# define MATERIALS
#----------------------------------------------------------------
set IDsteel 1;                  # assign material tag
set Fy 30000;                  # assign a super large yielding stress to enforce elastic buckling
set Es 200000.0;
set Bs 0.001;		# strain-hardening ratio (Et/Es)
#set R0 15;                      # 10<R0<20 recommended; controls the transition from elastic to plastic region on stress-strain curve
set poisson 0.3;
set G [expr $Es/(2*(1+$poisson))];
set BeamSecTagFiber 1;# assign a tag number to the beam section fiber
set SecTagTorsion 70; # assign a tag number to the torsion information of the beam
set BeamSecTag 3;

uniaxialMaterial Steel01 $IDsteel $Fy $Es $Bs;	# build steel01 material
#
# define SECTION DIMENSION AND FIBER DIVISION
#----------------------------------------------------------------
set D 100.0;		# Depth
set B 75.0; 		# Flange width
set L 16.5;		# Lip
set t 3.0;		# section thickness
set r 3.0;		# corner radius (to inside face)
set nfdw 50;		# number of fibers along web depth
set nfbf 40;		# number of fibers along flange
set nfL 10;		# number of fibers along lip
set nfC 4;		# number of fibers along circumferance of corners
set nft 1;		# number of fibers along thickness direction(=1)
set oC 0.0;		# sectorial coordinate at the centroid

# define FIBER SECTION, TORSION SECTION & TRANSFORMATION
#-----------------------------------------------------------------
set shearCoord [Csection $BeamSecTagFiber $IDsteel $D $B $L $t $r $nfdw $nfbf $nfL $nfC $nft];
set z0 [lindex $shearCoord 0 0];  #z-coord of shear center w.r.t centroid of section
set y0 [lindex $shearCoord 1 0];  #y-coord of shear center w.r.t centroid of section
set J  [lindex $shearCoord 2 0];  #Torsional constant
set GJ [expr $G*$J];
uniaxialMaterial Elastic $SecTagTorsion $GJ;
section Aggregator $BeamSecTag $SecTagTorsion T -section $BeamSecTagFiber;   # add elastic torsion

set numIntgrPts 5;   # number of integration points along the element
set BeamTransfTag 1;    # associate a tag to beam transformation  
geomTransf Corotational $BeamTransfTag 0 0 1;# define geometric transformation: performs a corotational geometric transformation of \
beam stiffness and resisting force from the basic system to the global-coordinate system
set cy 0.0;
set cz -63.46;
set omg 0.0;
# Define ELEMENTS -------------------------------------------------------------
for {set i 1} {$i<$endNode} {incr i 1} {
set elemID $i
set nodeI $i
set nodeJ [expr $i+1]
element dispBeamColumn $elemID $nodeI $nodeJ $numIntgrPts $BeamSecTag $BeamTransfTag  $y0  $z0  $omg  $cy  $cz;		
} 

# define initial Perturbation Load
#------------------------------------------------------------- 
pattern Plain 1 Linear {
  # NodeID, Fx, Fy, Fz, Mx, My, Mz, Bx
  load $middleNode 0 0 0 48.5 0 0 0;
  }
constraints Plain;  # Constraint handler -how it handles boundary conditions
numberer Plain;	    # Renumbers DoF to minimize band-width (optimization)
system BandGeneral; # System of equations solver
test NormDispIncr 1.0e-8 50 0;
algorithm NewtonLineSearch;# use Newton's solution algorithm: updates tangent stiffness at every iteration
integrator LoadControl 1.0 ;
analysis Static; 
analyze 10; 

loadConst -time 0.0; # maintains the load constant for the reminder of the analysis and resets the current time to 0

# define RECORDERS
#-------------------------------------------------------------
recorder Node -file $dir/CB_Nx300.out -time -node $middleNode -dof 1 2 3 4 5 6 7 disp;# record displacements at the middle node

# define second stage main Load (Axial force at the two ends)
#------------------------------------------------------------- 
set N 1000.0;
set my [expr -$N*$z0];
set mz [expr -$N*$y0];
pattern Plain 2 Linear {
  # NodeID, Fx, Fy, Fz, Mx, My, Mz, Bx
  load $startNode $N 0 0 0 $my -$mz 0;
  load $endNode -$N 0 0 0 -$my $mz 0;
 }

# define ANALYSIS PARAMETERS
#------------------------------------------------------------------------------------
constraints Plain; # how it handles boundary conditions
numberer Plain;	   # renumber dof's to minimize band-width 
system BandGeneral;# how to store and solve the system of equations in the analysis
test NormDispIncr 1.0e-08 50 ; # determine if convergence has been achieved at the end of an iteration step
algorithm Newton;
set Dincr 0.0005;#0.0001
set IDctrlNode $middleNode
set IDctrlDOF 4
integrator DisplacementControl $IDctrlNode $IDctrlDOF $Dincr;# Node number, dof number, 1st disp. increment
analysis Static	;# define type of analysis static or transient
variable algorithmTypeStatic Newton
set ok [analyze 3000];
#--------------------------------------------------------------------------------
set finishTime [clock clicks -milliseconds];
puts "Time taken: [expr ($finishTime-$startTime)/1000] sec"
set systemTime [clock seconds] 
puts "Finished Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"

