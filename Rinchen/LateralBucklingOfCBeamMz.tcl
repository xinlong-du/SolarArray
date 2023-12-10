# Lateral buckling of simply supported C beam subjected to major axis bending
# Units: N, mm
# ----------------------------------------------------------------------------
set systemTime [clock seconds] 
puts "Starting Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"
set startTime [clock clicks -milliseconds];
#---------------------------------------------------------------------------
wipe; # clear opensees model
source Csection.tcl;   # C-section with round corners
model basic -ndm 3 -ndf 7;# 3 dimensions, 7 dof per node
set dir LateralBuckling;  #set dir lateral buckling of C section
file mkdir $dir;          # create data directory

# define GEOMETRY
#-------------------------------------------------------------
set in2mm 25.4;
set eleLen 13.128;
#Nodes, NodeNumber, xCoord, yCoord, zCoord
node 1	[expr $eleLen*0.0*$in2mm]	0	0
node 2	[expr $eleLen*1.0*$in2mm]	0	0
node 3	[expr $eleLen*2.0*$in2mm]	0	0
node 4	[expr $eleLen*3.0*$in2mm]	0	0
node 5	[expr $eleLen*4.0*$in2mm]	0	0
node 6	[expr $eleLen*5.0*$in2mm]	0	0
node 7	[expr $eleLen*6.0*$in2mm]	0	0
node 8	[expr $eleLen*7.0*$in2mm]	0	0
node 9	[expr $eleLen*8.0*$in2mm]	0	0
node 10	[expr $eleLen*9.0*$in2mm]	0	0
node 11	[expr $eleLen*10.0*$in2mm]	0	0
node 12	[expr $eleLen*11.0*$in2mm]	0	0
node 13	[expr $eleLen*12.0*$in2mm]	0	0
node 14	[expr $eleLen*13.0*$in2mm]	0	0
node 15	[expr $eleLen*14.0*$in2mm]	0	0
node 16	[expr $eleLen*15.0*$in2mm]	0	0
node 17	[expr $eleLen*16.0*$in2mm]	0	0
node 18	[expr $eleLen*17.0*$in2mm]	0	0
node 19	[expr $eleLen*18.0*$in2mm]	0	0
node 20	[expr $eleLen*19.0*$in2mm]	0	0
node 21	[expr $eleLen*20.0*$in2mm]	0	0

# define BOUNDARY CONDITIONS (single point constraint)
#----------------------------------------------------------
# NodeID,dispX,dispY,dispZ,rotX,RotY,RotZ, Warping 
fix 1 0 1 1 1 0 0 0;
fix 11 1 0 0 0 0 0 0;
fix 21 0 1 1 1 0 0 0; 			
#-------------------------------------------------------
set startNode 1
set middleNode 11
set endNode 21

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
  load $middleNode 0 0 0 242.5 0 0 0;#+242.5 for positive branch;  
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
recorder Node -file $dir/8CS2.5x059Mz262inP.out -time -node $middleNode -dof 1 2 3 4 5 6 7 disp;

# define second stage main Load (Moment at the two ends)
#------------------------------------------------------------- 
pattern Plain 2 Linear {
  # NodeID, Fx, Fy, Fz, Mx, My, Mz, Bx
  load $startNode 0 0 0 0 0 [expr -4448.2216*25.4] 0; #the applied reference load is 1 kip-in
  load $endNode   0 0 0 0 0 [expr  4448.2216*25.4] 0;
}
# define ANALYSIS PARAMETERS
#------------------------------------------------------------------------------------
constraints Plain;           # how it handles boundary conditions
numberer Plain;		     # renumber dof's to minimize band-width 
system BandGeneral;	     # how to store and solve the system of equations in the analysis
test NormDispIncr 1.0e-8 50 0; # determine if convergence has been achieved at the end of an iteration step
algorithm NewtonLineSearch 0.8;
set Dincr -0.0001; #Displacement increment/decrement 
set IDctrlNode $middleNode
set IDctrlDOF 4;
set Dmax 10
integrator ArcLength 1.0 1.0; #Use this for positive branch
#                              node        dof        init   Jd min    max
#integrator DisplacementControl $IDctrlNode $IDctrlDOF $Dincr 1  $Dincr $Dincr; #use this for negative branch
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





