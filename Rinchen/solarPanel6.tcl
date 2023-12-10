# Lateral buckling of two simply supported C purlins connected by six solar panels
# subjected to major axis bending (uniform bending with Cb=1)
# Units: N, mm, kg, s, N/mm2, kg/mm3
# Xinlong Du, UC Berkeley, 2023
# xinlongdu@berkeley.edu
# ----------------------------------------------------------------------------
set systemTime [clock seconds] 
puts "Starting Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"
set startTime [clock clicks -milliseconds];
#---------------------------------------------------------------------------
wipe; # clear opensees model
source Csection.tcl;   # C-section with round corners
model basic -ndm 3 -ndf 7;# 3 dimensions, 7 dof per node
set dir solarPanel;  #set dir lateral buckling of C section
file mkdir $dir;          # create data directory

# define GEOMETRY
#-------------------------------------------------------------
set in2mm 25.4;

for {set i 0} {$i<6} {incr i 1} {
    #node [expr 501+3*$i] [expr   (0.0+42.26*$i)*$in2mm] 0.0 [expr 0.0*$in2mm]
    #node [expr 502+3*$i] [expr (20.63+42.26*$i)*$in2mm] 0.0 [expr 0.0*$in2mm]
    #node [expr 503+3*$i] [expr (41.26+42.26*$i)*$in2mm] 0.0 [expr 0.0*$in2mm]
    node [expr 601+3*$i] [expr   (0.0+42.26*$i)*$in2mm] 0.0 [expr 21.0*$in2mm]
    #node [expr 602+3*$i] [expr (20.63+42.26*$i)*$in2mm] 0.0 [expr 21.0*$in2mm]
    node [expr 603+3*$i] [expr (41.26+42.26*$i)*$in2mm] 0.0 [expr 21.0*$in2mm]
    #node [expr 701+3*$i] [expr   (0.0+42.26*$i)*$in2mm] 0.0 [expr 42.0*$in2mm]
    #node [expr 702+3*$i] [expr (20.63+42.26*$i)*$in2mm] 0.0 [expr 42.0*$in2mm]
    #node [expr 703+3*$i] [expr (41.26+42.26*$i)*$in2mm] 0.0 [expr 42.0*$in2mm]
    node [expr 801+3*$i] [expr   (0.0+42.26*$i)*$in2mm] 0.0 [expr 63.0*$in2mm]
    #node [expr 802+3*$i] [expr (20.63+42.26*$i)*$in2mm] 0.0 [expr 63.0*$in2mm]
    node [expr 803+3*$i] [expr (41.26+42.26*$i)*$in2mm] 0.0 [expr 63.0*$in2mm]
    #node [expr 901+3*$i] [expr   (0.0+42.26*$i)*$in2mm] 0.0 [expr 84.0*$in2mm]
    #node [expr 902+3*$i] [expr (20.63+42.26*$i)*$in2mm] 0.0 [expr 84.0*$in2mm]
    #node [expr 903+3*$i] [expr (41.26+42.26*$i)*$in2mm] 0.0 [expr 84.0*$in2mm]
}

node 600 [expr   -5.0*$in2mm] 0.0 [expr 21.0*$in2mm]
node 619 [expr 257.56*$in2mm] 0.0 [expr 21.0*$in2mm]
node 800 [expr   -5.0*$in2mm] 0.0 [expr 63.0*$in2mm]
node 819 [expr 257.56*$in2mm] 0.0 [expr 63.0*$in2mm]

# define BOUNDARY CONDITIONS (single point constraint)
#----------------------------------------------------------
# NodeID,dispX,dispY,dispZ,rotX,RotY,RotZ, Warping 
fix 600 0 1 1 1 0 0 0; #temp, need to be modified
fix 609 1 0 0 0 0 0 0;
fix 619 0 1 1 1 0 0 0;
fix 800 0 1 1 1 0 0 0;
fix 809 1 0 0 0 0 0 0;
fix 819 0 1 1 1 0 0 0; 			
#-------------------------------------------------------
set startNode1  600
set middleNode1 609
set endNode1    619
set startNode2  800
set middleNode2 809
set endNode2    819

# Define ELEMENTS & SECTIONS
#-------------------------------------------------------------
set ColSecTagFiber 1;# assign a tag number to the column section
set SecTagTorsion 70;# assign a tag number for torsion 
set BeamSecTag 3
 
# define MATERIALS
#----------------------------------------------------------------
set IDsteel 1; # Identifier for material
set Fy 50000.0; # Yield stress -Use very large yield stress for elastic buckling analysis
set Es 200000.0; # Elastic modulus
set Bs 0.001;		# strain-hardening ratio 
set G [expr $Es/(2*(1+0.3))]; # Shear modulus
uniaxialMaterial Steel01 $IDsteel $Fy $Es $Bs;	# build steel01 material

# define SECTION DIMENSION AND FIBER DIVISION
#----------------------------------------------------------------
set D [expr 8.0*$in2mm];		# Depth
set B [expr 2.5*$in2mm]; 		# Flange width
set L [expr 0.773*$in2mm];		# Lip
set t [expr 0.059*$in2mm];		# section thickness for C-section	
set r [expr 0.1875*$in2mm];		# corner radius (to inside face)
set nfdw 50;		# number of fibers along web depth
set nfbf 40;		# number of fibers along flange
set nfL 10;		# number of fibers along lip
set nfC 4;		# number of fibers along circumferance of corners
set nft 1;		# number of fibers through thickness

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
set nPurlin1 {600 601 603 604 606 607 609 610 612 613 615 616 618 619}; #nodes of purlin # 1
set nPurlin2 {800 801 803 804 806 807 809 810 812 813 815 816 818 819}; #nodes of purlin # 2

for {set i 0} {$i<13} {incr i 1} {
set elem1ID [expr $i+100];
set node1I [lindex $nPurlin1 $i];
set node1J [lindex $nPurlin1 [expr $i+1]];
set elem2ID [expr $i+200];
set node2I [lindex $nPurlin2 $i];
set node2J [lindex $nPurlin2 [expr $i+1]];
element dispBeamColumn $elem1ID $node1I $node1J $numIntgrPts $BeamSecTag $BeamTransfTag  $y0  $z0  $omg  $cy  $cz;
element dispBeamColumn $elem2ID $node2I $node2J $numIntgrPts $BeamSecTag $BeamTransfTag  $y0  $z0  $omg  $cy  $cz;	
} 

# define initial Perturbation Load
#------------------------------------------------------------- 
pattern Plain 1 Linear {
  # NodeID, Fx, Fy, Fz, Mx, My, Mz, Bx
  load $middleNode1 0 0 0 -242.5 0 0 0;#+242.5 for positive branch; 
  load $middleNode2 0 0 0 -242.5 0 0 0;#+242.5 for positive branch;  
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
recorder Node -file $dir/solarPurlin1N.out -time -node $middleNode1 -dof 1 2 3 4 5 6 7 disp;
recorder Node -file $dir/solarPurlin2N.out -time -node $middleNode2 -dof 1 2 3 4 5 6 7 disp;

# define second stage main Load (Moment at the two ends)
#------------------------------------------------------------- 
pattern Plain 2 Linear {
  # NodeID, Fx, Fy, Fz, Mx, My, Mz, Bx
  load $startNode1 0 0 0 0 0 [expr -4448.2216*25.4] 0; #the applied reference load is 1 kip-in
  load $endNode1   0 0 0 0 0 [expr  4448.2216*25.4] 0;
  load $startNode2 0 0 0 0 0 [expr -4448.2216*25.4] 0; #the applied reference load is 1 kip-in
  load $endNode2   0 0 0 0 0 [expr  4448.2216*25.4] 0;
}
# define ANALYSIS PARAMETERS
#------------------------------------------------------------------------------------
constraints Plain;           # how it handles boundary conditions
numberer Plain;		     # renumber dof's to minimize band-width 
system BandGeneral;	     # how to store and solve the system of equations in the analysis
test NormDispIncr 1.0e-8 50 0; # determine if convergence has been achieved at the end of an iteration step
algorithm NewtonLineSearch 0.8;
set Dincr -0.0001; #Displacement increment/decrement 
set IDctrlNode $middleNode1;
set IDctrlDOF 4;
set Dmax 10
#integrator ArcLength 1.0 1.0; #Use this for curve with peak
#                              node        dof        init   Jd min    max
integrator DisplacementControl $IDctrlNode $IDctrlDOF $Dincr 1  $Dincr $Dincr
analysis Static	;			# define type of analysis static or transient
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
			integrator DisplacementControl  $IDctrlNode $IDctrlDOF $Dincr;	# bring back to original increment
		}; # end if 
          };	# end while loop
  };      # end if ok !0
#-----------------------------------------------------------------------
set finishTime [clock clicks -milliseconds];
puts "Time taken: [expr ($finishTime-$startTime)/1000] sec"
set systemTime [clock seconds] 
puts "Finished Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"





