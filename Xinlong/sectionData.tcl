#This file contains various procedures which creates section data (nodes and segment information) for
#determining section properties of thin-walled open sections
#---------------------------------------------------------------------------------------------------
#Program developed by :
# Rinchen
# PhD student
# University of Sydney
# Dated: September 2015
#-----------------------------------
# Open-Sections included:
#	Plain C-sections without lips
#       Plain C-sections with lips
#       C-section with round corners lips
#       C-section with round corners with lips rotated by 90 degrees
#       I-sections
#       C-section with top lip turned upwards
#       C-section with bottom lip turned downwards
#	PI-Section
#------------------------------------------------------------------------------------------------------
source C:/ActiveTcl/lib/tcllib1.18/math/math.tcl; #Xinlong # address to folder where math library is stored
	
	package require math::linearalgebra
	namespace eval compute {
	namespace import ::math::linearalgebra::*	
	}
#
#============================================================================================================
#This procedure returns the node coordinate and element information matrix for plain C section without lips
#------------------------------------------------------------------------------------------------------------
proc plainCSectionWithoutLipInfo {D Bt Bb tw tf} {
#
#define coordinates
#                
#       2-----(1)-----1 (Node1x,Node1y)
#       |             
#       |            
#       |             
#       |             
#	|	
#      (2)
#	|
#	|	
#       |             
#       |             
#       |             
#       |             
#       3-------(3)------ 4 (Node4x,Node4y)
#              
#  Cross-section of C-section
#
set NoOfNodes 4; 
set NoOfElements [expr $NoOfNodes-1]

#  Define centreline coordinates of nodes with origin at node 3 

	set Node1x [expr $Bt-$tw/2];	set Node1y [expr $D-$tf];
	set Node2x 0.0;			set Node2y [expr $D-$tf];
	set Node3x 0.0;			set Node3y 0.0;
	set Node4x [expr $Bb-$tw/2];	set Node4y 0.0;
	
#---------------------------------------------------------------------------
#construct nodal coordinate matrix based on the cross-section information
set NodeCoord [math::linearalgebra::mkMatrix $NoOfNodes 3 0.0]; #No of rows, No of columns default value
for {set i 0} {$i<$NoOfNodes} {incr i 1} {
	math::linearalgebra::setelem NodeCoord $i 0 [expr $i+1];
}
#x-coordinates of nodes: MatrixName, ColumnNo, NodeCoord, min, max
math::linearalgebra::setcol NodeCoord 1 $Node1x 0 0;
math::linearalgebra::setcol NodeCoord 1 $Node2x 1 1;
math::linearalgebra::setcol NodeCoord 1 $Node3x 2 2;
math::linearalgebra::setcol NodeCoord 1 $Node4x 3 3;
#y-coordinates of nodes
math::linearalgebra::setcol NodeCoord 2 $Node1y 0 0;
math::linearalgebra::setcol NodeCoord 2 $Node2y 1 1;
math::linearalgebra::setcol NodeCoord 2 $Node3y 2 2;
math::linearalgebra::setcol NodeCoord 2 $Node4y 3 3;
#------------------------------------------------------------------
#construction Element info matrix: mkMatrix, rows, columns, initial value=0.0
set Segment [math::linearalgebra::mkMatrix $NoOfElements 4 0.0]
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	math::linearalgebra::setelem Segment $i 0 [expr $i+1];
}
#Define element connection (node i) in column1: colNo,startNodei, min, max
math::linearalgebra::setcol Segment 1 1 0 0;
math::linearalgebra::setcol Segment 1 2 1 1;
math::linearalgebra::setcol Segment 1 3 2 2;
#Define element connection (node j) in column 2:colNo, endNodej, min, max
math::linearalgebra::setcol Segment 2 2 0 0;
math::linearalgebra::setcol Segment 2 3 1 1;
math::linearalgebra::setcol Segment 2 4 2 2;
#Define thickness for each element in column 3: colNo, eleThickness, min, max
math::linearalgebra::setcol Segment 3 $tf 0 0;
math::linearalgebra::setcol Segment 3 $tw 1 1;
math::linearalgebra::setcol Segment 3 $tf 2 2;

#---------------------------------------------
return [list $NodeCoord $Segment]
}
#
#============================================================================================================       
#This procedure returns the node coordinate and element information matrix for plain C section
#------------------------------------------------------------------------------------------------------------
proc plainCSectionInfo {D B L t} {
#
#define coordinates
#                
#       3-----(2)-----2
#       |             |
#       |            (1)
#       |             |
#       |             1(Node1x,Node1y)
#	|	
#      (3)
#	|
#	|	
#       |             6(Node6x,Node6y)
#       |             |
#       |            (5) 
#       |             |
#       4-----(4)---- 5
#              
#  Cross-section of C-section
#
set NoOfNodes 6; 
set NoOfElements [expr $NoOfNodes-1]

#  Define centraline coordinates of nodes with origin at node 4

	set Node1x [expr $B-$t];	set Node1y [expr $D-$t-($L-0.5*$t)];
	set Node2x [expr $B-$t];	set Node2y [expr $D-$t];
	set Node3x 0.0;			set Node3y [expr $D-$t];
	set Node4x 0.0;			set Node4y 0.0;
	set Node5x [expr $B-$t];	set Node5y 0.0;
	set Node6x [expr $B-$t];	set Node6y [expr $L-0.5*$t];
	
#---------------------------------------------------------------------------
#construct nodal coordinate matrix based on the cross-section information
set NodeCoord [math::linearalgebra::mkMatrix $NoOfNodes 3 0.0]; #No of rows, No of columns default value
for {set i 0} {$i<$NoOfNodes} {incr i 1} {
	math::linearalgebra::setelem NodeCoord $i 0 [expr $i+1];
}
#x-coordinates of nodes: MatrixName, ColumnNo, NodeCoord, min, max
math::linearalgebra::setcol NodeCoord 1 $Node1x 0 0;
math::linearalgebra::setcol NodeCoord 1 $Node2x 1 1;
math::linearalgebra::setcol NodeCoord 1 $Node3x 2 2;
math::linearalgebra::setcol NodeCoord 1 $Node4x 3 3;
math::linearalgebra::setcol NodeCoord 1 $Node5x 4 4;
math::linearalgebra::setcol NodeCoord 1 $Node6x 5 5;
#y-coordinates of nodes
math::linearalgebra::setcol NodeCoord 2 $Node1y 0 0;
math::linearalgebra::setcol NodeCoord 2 $Node2y 1 1;
math::linearalgebra::setcol NodeCoord 2 $Node3y 2 2;
math::linearalgebra::setcol NodeCoord 2 $Node4y 3 3;
math::linearalgebra::setcol NodeCoord 2 $Node5y 4 4;
math::linearalgebra::setcol NodeCoord 2 $Node6y 5 5;
#------------------------------------------------------------------
#construction Element info matrix: mkMatrix, rows, column initial value=0.0
set Segment [math::linearalgebra::mkMatrix $NoOfElements 4 0.0]
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	math::linearalgebra::setelem Segment $i 0 [expr $i+1];
}
#Define element connection (node i) in column1: colNo,startNodei, min, max
math::linearalgebra::setcol Segment 1 1 0 0;
math::linearalgebra::setcol Segment 1 2 1 1;
math::linearalgebra::setcol Segment 1 3 2 2;
math::linearalgebra::setcol Segment 1 4 3 3;
math::linearalgebra::setcol Segment 1 5 4 4;
#Define element connection (node j) in column 2:colNo, endNodej, min, max
math::linearalgebra::setcol Segment 2 2 0 0;
math::linearalgebra::setcol Segment 2 3 1 1;
math::linearalgebra::setcol Segment 2 4 2 2;
math::linearalgebra::setcol Segment 2 5 3 3;
math::linearalgebra::setcol Segment 2 6 4 4;

math::linearalgebra::setcol Segment 3 $t 0 0;
math::linearalgebra::setcol Segment 3 $t 1 1;
math::linearalgebra::setcol Segment 3 $t 2 2;
math::linearalgebra::setcol Segment 3 $t 3 3;
math::linearalgebra::setcol Segment 3 $t 4 4;
#---------------------------------------------
return [list $NodeCoord $Segment]
}
#
#============================================================================================================
#This procedure returns the node coordinate and element information matrix for C section with round corners  
#------------------------------------------------------------------------------------------------------------
proc roundCornerCSectionInfo {D B L t r} {
#
#define coordinates
#                
#         7-----(6)-----6
#	/		  \
#      11		   2	
#      |             	   |
#      |            	  (1)
#      |                   |
#      |             	   1(Node1x,Node1y)
#      |	
#     (11)
#      |
#      |	
#      |                  22(Node22x,Node22y)
#      |                   |
#      |                  (21) 
#      |               	   |
#      12		  21
#       \		 /
#        16----(16)----17
#              
#  Cross-section of C-section 
#
set NoOfNodes 22; # input number of nodes
set NoOfElements [expr $NoOfNodes-1];
set nfC 4; #4 segments at the corner
#
#  Define centraline coordinates of nodes with origin at bottom left corner
	set rm [expr $r+0.5*$t]
	set pi [expr 2*asin(1.0)];
	set theta [expr ($pi/2)/$nfC];
  
	#Top lip
	set Node1x [expr $B-$t];	set Node1y [expr $D-$t-($L-0.5*$t)];
	set Node2x [expr $B-$t];	set Node2y [expr $D-$t-$rm];
	
	#Top right corner
	set Node3x [expr $Node2x-$rm+$rm*cos($theta)];	set Node3y [expr $Node2y+$rm*sin($theta)];
	set Node4x [expr $Node2x-$rm+$rm*cos(2*$theta)];set Node4y [expr $Node2y+$rm*sin(2*$theta)];
	set Node5x [expr $Node2x-$rm+$rm*cos(3*$theta)];set Node5y [expr $Node2y+$rm*sin(3*$theta)];
	
	#Top flange
	set Node6x [expr $B-$t-$rm];	set Node6y [expr $D-$t];
	set Node7x $rm;			set Node7y [expr $D-$t];
	
	#Top left corner
	set Node8x [expr $rm-$rm*sin($theta)];		set Node8y $Node5y;
	set Node9x [expr $rm-$rm*sin(2*$theta)];	set Node9y $Node4y;
	set Node10x [expr $rm-$rm*sin(3*$theta)];	set Node10y $Node3y;
	
	#Web
	set Node11x 0.0;		set Node11y $Node2y;
	set Node12x 0.0;		set Node12y $rm;
	
	#Bottom left corner
	set Node13x [expr $rm-$rm*cos($theta)];		set Node13y [expr $rm-$rm*sin($theta)];
	set Node14x [expr $rm-$rm*cos(2*$theta)];	set Node14y [expr $rm-$rm*sin(2*$theta)];
	set Node15x [expr $rm-$rm*cos(3*$theta)];	set Node15y [expr $rm-$rm*sin(3*$theta)];

	#Bottom flange
	set Node16x $Node7x;	set Node16y 0.0;
	set Node17x $Node6x;	set Node17y 0.0;
	
	#Bottom right corner
	set Node18x $Node5x; 	set Node18y $Node15y;	
	set Node19x $Node4x; 	set Node19y $Node14y;	
	set Node20x $Node3x; 	set Node20y $Node13y;
	
	#Bottom lip
	set Node21x $Node2x; 	set Node21y $Node12y; 	
	set Node22x $Node1x; 	set Node22y [expr $L-0.5*$t];
#---------------------------------------------------------------------------	
#construct nodal coordinate matrix based on the cross-section information
set NodeCoord [math::linearalgebra::mkMatrix $NoOfNodes 3 0.0]
for {set i 0} {$i<$NoOfNodes} {incr i 1} {
	math::linearalgebra::setelem NodeCoord $i 0 [expr $i+1];
}
#x-coordinates of nodes: MatrixName, ColumnNo, NodeCoord, min, max
for {set i 0} {$i<$NoOfNodes} {incr i 1} {
	set j [expr $i+1]
math::linearalgebra::setcol NodeCoord 1 [expr "\$Node$j\x"] $i $i;	
}
#y-coordinates of nodes
for {set i 0} {$i<$NoOfNodes} {incr i 1} {
	set j [expr $i+1]
math::linearalgebra::setcol NodeCoord 2 [expr "\$Node$j\y"] $i $i;	
}
#----------------------------------------------------------------------------
#construction Element info matrix: mkMatrix, rows, column initial value=0.0
set Segment [math::linearalgebra::mkMatrix $NoOfElements 4 0.0]
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	math::linearalgebra::setelem Segment $i 0 [expr $i+1];
}
#Define element connection (node i) in column1: colNo,Nodei, min, max
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	set j [expr $i+1]
	math::linearalgebra::setcol Segment 1 $j $i $i;	
}
#Define element connection (node j) in column 2:colNo, Nodej, min, max
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	set j [expr $i+2]
	math::linearalgebra::setcol Segment 2 $j $i $i;	
}
#Assign uniform thickness to the section
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	math::linearalgebra::setcol Segment 3 $t $i $i;	
}
#-----------------------------------------------------------
return [list $NodeCoord $Segment]   
}
#
#
#================================================================================================================================
#This procedure returns the node coordinate and element information matrix for C section with round corners and lips turn upwards  
#---------------------------------------------------------------------------------------------------------------------------
proc roundCornerCSectionInfoLipTurnUp {D B L t r} {
#
#define coordinates
#			   1 1(Node1x,Node1y)
#			   |
#			  (1)
#			   |
#			   2
# 			  /
#         7-----(6)-----6
#	/		  
#      11		  	
#      |             	  
#      |            	  
#      |                   
#      |             	   
#      |	
#     (11)
#      |
#      |	
#      |                    22(Node22x,Node22y)
#      |                    |
#      |                   (21)
#      |               	   |
#      12		  21
#       \		 /
#        16----(16)----17
#			
#
#  Cross-section of C-section with lips turned upwards 
#
set NoOfNodes 22; # input number of nodes
set NoOfElements [expr $NoOfNodes-1];
set nfC 4; #4 segment at the corner
#
#  Define centraline coordinates of nodes with origin at bottom left corner
	set rm [expr $r+0.5*$t]
	set pi [expr 2*asin(1.0)];
	set theta [expr ($pi/2)/$nfC];
  
	#Top lip
	set Node1x [expr $B-$t]
	set Node1y [expr $D-$t+$L-$t/2]
	
	set Node2x [expr $B-$t]
	set Node2y [expr $D-$t+$rm]
 
	#Top right corner
	set Node3x [expr $Node2x-$rm+$rm*cos($theta)]
	set Node3y [expr $Node2y-$rm*sin($theta)]
	
	set Node4x [expr $Node2x-$rm+$rm*cos(2*$theta)]
	set Node4y [expr $Node2y-$rm*sin(2*$theta)]
	
	set Node5x [expr $Node2x-$rm+$rm*cos(3*$theta)]
	set Node5y [expr $Node2y-$rm*sin(3*$theta)]
	
	#Top flange
	set Node6x [expr $B-$t-$rm]
	set Node6y [expr $D-$t]
	
	set Node7x $rm
	set Node7y $Node6y
	
	#Top left corner
	set Node8x [expr $rm-$rm*sin($theta)]
	set Node8y [expr $Node7y-$rm+$rm*cos($theta)]
	
	set Node9x [expr $rm-$rm*sin(2*$theta)]
	set Node9y [expr $Node7y-$rm+$rm*cos(2*$theta)]
	
	set Node10x [expr $rm-$rm*sin(3*$theta)]
	set Node10y [expr $Node7y-$rm+$rm*cos(3*$theta)]
	
	#Web
	set Node11x 0.0
	set Node11y [expr $D-$t-$rm]
	
	set Node12x 0.0
	set Node12y $rm
	
	#Bottom left corner
	set Node13x [expr $rm-$rm*cos($theta)]
	set Node13y [expr $rm-$rm*sin($theta)]
	
	set Node14x [expr $rm-$rm*cos(2*$theta)]
	set Node14y [expr $rm-$rm*sin(2*$theta)]
	
	set Node15x [expr $rm-$rm*cos(3*$theta)]
	set Node15y [expr $rm-$rm*sin(3*$theta)]

	#Bottom flange
	set Node16x $Node7x
	set Node16y 0.0
	
	set Node17x $Node6x
	set Node17y 0.0
	
	#Bottom right corner
	set Node18x $Node5x
	set Node18y [expr $rm-$rm*cos($theta)]
	
	set Node19x $Node4x
	set Node19y [expr $rm-$rm*cos(2*$theta)]
	
	set Node20x $Node3x
	set Node20y [expr $rm-$rm*cos(3*$theta)]
	
	#Bottom lip
	set Node21x $Node2x
	set Node21y $rm
	
	set Node22x $Node1x
	set Node22y [expr $L-$t/2]
#---------------------------------------------------------------------------	
#construct nodal coordinate matrix based on the cross-section information
set NodeCoord [math::linearalgebra::mkMatrix $NoOfNodes 3 0.0]
for {set i 0} {$i<$NoOfNodes} {incr i 1} {
	math::linearalgebra::setelem NodeCoord $i 0 [expr $i+1];
}
#x-coordinates of nodes: MatrixName, ColumnNo, NodeCoord, min, max
for {set i 0} {$i<$NoOfNodes} {incr i 1} {
	set j [expr $i+1]
math::linearalgebra::setcol NodeCoord 1 [expr "\$Node$j\x"] $i $i;	
}
#y-coordinates of nodes
for {set i 0} {$i<$NoOfNodes} {incr i 1} {
	set j [expr $i+1]
math::linearalgebra::setcol NodeCoord 2 [expr "\$Node$j\y"] $i $i;
}
#----------------------------------------------------------------------------
#construction Element info matrix: mkMatrix, rows, column initial value=0.0
set Segment [math::linearalgebra::mkMatrix $NoOfElements 4 0.0]
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	math::linearalgebra::setelem Segment $i 0 [expr $i+1];
}
#Define element connection (node i) in column1: colNo,Nodei, min, max
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	set j [expr $i+1]
	math::linearalgebra::setcol Segment 1 $j $i $i;	
}
#Define element connection (node j) in column 2:colNo, Nodej, min, max
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	set j [expr $i+2]
	math::linearalgebra::setcol Segment 2 $j $i $i;	
}
#Assign uniform thickness to the section
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	math::linearalgebra::setcol Segment 3 $t $i $i;	
}
return [list $NodeCoord $Segment]   
}
#===========================================================================================================================
#This procedure returns the node coordinate and element information matrix for plain I section
#------------------------------------------------------------------------------------------------------------
proc plainISectionInfo {D B tf tw wLoc} {
#
#wLoc:0=<wLoc<=1; determines the location of web: 0 left; 1 right
#define coordinates
#                
#       3----(2)----2----(1)----1
#                   |            
#                   |            
#                   |            
#                   |            
#                  (3) 
#                   |            
#                   |            
#                   |             
#                   |            
#       4----(4)----5----(5)----6
#              
#        Cross-section of I-section
#
  set NoOfNodes 6; # input number of nodes
  set NoOfElements [expr $NoOfNodes-1]
#  
#  Define centraline coordinates of nodes with origin at node 4
	set Node1x $B;			set Node1y [expr $D-$tf]; 	
	set Node2x [expr $B*$wLoc]; 	set Node2y [expr $D-$tf]; 	
	set Node3x 0.0; 		set Node3y [expr $D-$tf]; 	
	set Node4x 0.0; 		set Node4y 0.0; 	
	set Node5x [expr $B*$wLoc]; 	set Node5y 0.0; 	
	set Node6x $B; 			set Node6y 0.0;	
#------------------------------------------------------------------------
#construct nodal coordinate matrix based on the cross-section information
set NodeCoord [math::linearalgebra::mkMatrix $NoOfNodes 3 0.0]
for {set i 0} {$i<$NoOfNodes} {incr i 1} {
	math::linearalgebra::setelem NodeCoord $i 0 [expr $i+1];
}
#x-coordinates of nodes: MatrixName, ColumnNo, NodeCoord, min, max
math::linearalgebra::setcol NodeCoord 1 $Node1x 0 0;
math::linearalgebra::setcol NodeCoord 1 $Node2x 1 1;
math::linearalgebra::setcol NodeCoord 1 $Node3x 2 2;
math::linearalgebra::setcol NodeCoord 1 $Node4x 3 3;
math::linearalgebra::setcol NodeCoord 1 $Node5x 4 4;
math::linearalgebra::setcol NodeCoord 1 $Node6x 5 5;
#y-coordinates of nodes
math::linearalgebra::setcol NodeCoord 2 $Node1y 0 0;
math::linearalgebra::setcol NodeCoord 2 $Node2y 1 1;
math::linearalgebra::setcol NodeCoord 2 $Node3y 2 2;
math::linearalgebra::setcol NodeCoord 2 $Node4y 3 3;
math::linearalgebra::setcol NodeCoord 2 $Node5y 4 4;
math::linearalgebra::setcol NodeCoord 2 $Node6y 5 5;
#--------------------------------------------------------------------
#construction Element info matrix: mkMatrix, rows, column initial value=0.0
set Segment [math::linearalgebra::mkMatrix $NoOfElements 4 0.0]
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	math::linearalgebra::setelem Segment $i 0 [expr $i+1]; # Defines segment No: 1 - No. of Segments
}
#Define element connection (node i) in column1: colNo,startNodei, min, max
math::linearalgebra::setcol Segment 1 1 0 0;
math::linearalgebra::setcol Segment 1 2 1 1;
math::linearalgebra::setcol Segment 1 2 2 2;
math::linearalgebra::setcol Segment 1 4 3 3;
math::linearalgebra::setcol Segment 1 5 4 4;
#Define element connection (node j) in column 2:colNo, endNodej, min, max
math::linearalgebra::setcol Segment 2 2 0 0;
math::linearalgebra::setcol Segment 2 3 1 1;
math::linearalgebra::setcol Segment 2 5 2 2;
math::linearalgebra::setcol Segment 2 5 3 3;
math::linearalgebra::setcol Segment 2 6 4 4;

math::linearalgebra::setcol Segment 3 $tf 0 0;
math::linearalgebra::setcol Segment 3 $tf 1 1;
math::linearalgebra::setcol Segment 3 $tw 2 2;
math::linearalgebra::setcol Segment 3 $tf 3 3;
math::linearalgebra::setcol Segment 3 $tf 4 4;
#----------------------------------------------
return [list $NodeCoord $Segment]
}
