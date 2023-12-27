# The Program creates fiber section for lipped C section with round corners and assign all relevant information 
# -------------------------------------------------------------------------------------------------------------- 
# Written by: Rinchen  
# Date: 3 Oct 2015
# PhD student: University of Sydney, Sydney NSW, Australia
#-------------------------------------------------------
# Input parameters: 
# secID - section ID number 
# matID - material ID number 
# D = Nominal height 
# B = Nominal width of flange 
# L=  Nominal length of lip
# t = Nominal thickness of section
# r = inside corner radius
# nfbf = number of fibers along Top/Bottom flange 
# nfdw = number of fibers along web 
# nfL = number of fibers along lip 
# nfC = number of fibers along the corner curve (only 4 considered)
# nft = number of fibers through thickness (=1 as the section is thin)
#---------------------------------------------------------------------------

proc Csection { secID matID D B L t r nfdw nfbf nfL nfC nft} {
#Csection $BeamSecTagFiber $IDsteel $D $B $L $t $r $zbar $nfdw $nfbf $nfL $nfC $nft
	
	source C:/ActiveTcl/lib/tcllib1.18/math/math.tcl; #Xinlong
	
	package require math::linearalgebra
	namespace eval compute {
	namespace import ::math::linearalgebra::*
	}
	
#load dependent files	
	source sectionData.tcl
	source SectionPropertiesCalculator.tcl
	source Interpolation.tcl
#-------------------------------------------------------------------------------
#define coordinates
#                
#         7--------------6
#	/		  \
#      11		   2	
#      |             	   |
#      |            	   |
#      |                   |
#      |             	   1
#      |	
#      |
#      |
#      |	
#      |                  22
#      |                   |
#      |                   | 
#      |               	   |
#      12		  21
#       \		 /
#        16------------17
#              
#  Cross-section of C-section 
#
# Calculate section properties
#-------------------------------------------------------------
set data [roundCornerCSectionInfo $D $B $L $t $r];#prepares data for calculation of section properties 
set NodeCoord [lindex [lindex $data] 0]; #NodeInfo
set Segment [lindex [lindex $data] 1]; #SegmentInfo
set corwarpInfo [SectionProperties $NodeCoord $Segment];#Calculates section properties
#
#Extracts centroid, and shear centre 
set xc0 [lindex $corwarpInfo 0 6]; #x-coord from extreme bottom left
set yc0 [lindex $corwarpInfo 1 6]; #y-coord from extreme bottom left
set xo [lindex $corwarpInfo 2 6];  #x-coord of shear center w.r.t centroid of section
set yo [lindex $corwarpInfo 3 6];  #y-coord of shear center w.r.t centroid of section
set J  [lindex $corwarpInfo 4 6]; # Torsional constant J 

#pack shearcentre into one list to be sent to main file
set shearCentre [math::linearalgebra::mkMatrix 3 1 0.0];
		math::linearalgebra::setrow shearCentre 0 $xo 0 0;
		math::linearalgebra::setrow shearCentre 1 $yo 0 0;
		math::linearalgebra::setrow shearCentre 2 $J 0 0;
###-----------------------------------------------------------------------------------------------------------------------
#Recalculate x-coordinate of centroid of section as xc0 based on centreline segment is not accurate enough for fiber section
#and fiber section is based on actual section having finite thickness
	
	set R  [expr $r+$t];#Outer radius
	set pi [expr 2*asin(1.0)];
	
	#Calculate coordinate of centroid from extreme left
	set zc [expr 4/(3*$pi)*($R*$R*$R-$r*$r*$r)/($R*$R-$r*$r)]
	set Areatrue [expr ($D-2*($r+$t))*$t+2*($B-2*($r+$t))*$t+2*($L-($r+$t))*$t+$pi*($R*$R-$r*$r)]; #Area of section
	set Qc [expr ($D-2*($r+$t))*$t*$t/2+2*($B-2*($r+$t))*$t*$B/2+2*($L-($r+$t))*$t*($B-$t/2)+2*$pi*($R*$R-$r*$r)/4*($R-$zc)+2*$pi*($R*$R-$r*$r)/4*($B-($r+$t)+$zc)];
	set zbar [expr $Qc/$Areatrue]; #z-coordinate of centroid from left
#--------------------------------------------------------------------------------------------------------------------------	
#Create fiber cross-section information	
#Coordinates for comptuting fiber size and centroid
	set y1 [expr $D/2.0]
	set y2 [expr $y1-$t]
	set y3 [expr $y2-$r]
	set y4 [expr $y1-$L]
		
	set z1 [expr -$zbar]
	set z2 [expr $z1+$t]
	set z3 [expr $z2+$r]
	set z4 [expr $B+$z1-($t+$r)]
	set z5 [expr $z4+$r]
	set z6 [expr $z5+$t]
	
	#Calculate length of each fiber at each region: lips, flange, corners and web
	set dfL [expr ($y3-$y4)/($nfL)] ;#length of each fibre in lip
	set theta [expr (0.5*$pi)/$nfC]; #angle(radians) subtended by each fiber at the corner
	set cArea [expr ($R*$R-$r*$r)*$theta/2.0];#area of each corner fiber
	set dbf [expr ($z4-$z3)/$nfbf]; #length of each fiber in flange
	set dwf [expr (2.0*$y3)/$nfdw];#length of each fiber in web
	
	set NoOfFiber [expr ($nfL+$nfbf)*2+$nfC*4+$nfdw]

#Assemble coordinate of centroid, area of each fiber
#--------------------------------------------------------------------------------------------
 #create matrix to store fiber information
 set Fib [math::linearalgebra::mkMatrix $NoOfFiber 5 0];
 
for {set i 0} {$i<$nfL} {incr i 1} {#Top lip
	#Fiber No, x,y, Area, warping(to be included later)
	math::linearalgebra::setrow Fib $i $i 0 0;
	math::linearalgebra::setrow Fib $i [expr ($z5+$z6)/2.0] 1 1;
	math::linearalgebra::setrow Fib $i [expr $y4+($dfL/2.0*(2*$i+1))] 2 2;
	math::linearalgebra::setrow Fib $i [expr $dfL*$t] 3 3;
	}
	
for {set i 0} {$i<$nfC} {incr i 1} {#Top right corner
	#Fiber No, x,y, Area, warping(to be included later)	
	set fibNo [expr $i+$nfL]
	math::linearalgebra::setrow Fib $fibNo $fibNo 0 0;
	math::linearalgebra::setrow Fib $fibNo [expr $z4+($r+$t/2)*cos($theta/2*(2*$i+1))] 1 1;
	math::linearalgebra::setrow Fib $fibNo [expr $y3+($r+$t/2)*sin($theta/2*(2*$i+1))] 2 2;
	math::linearalgebra::setrow Fib $fibNo $cArea 3 3;
	}
#
for {set i 0} {$i<$nfbf} {incr i 1} {#Top flange
	set fibNo [expr $i+$nfC+$nfL]
	math::linearalgebra::setrow Fib $fibNo $fibNo 0 0;
	math::linearalgebra::setrow Fib $fibNo [expr $z4-($dbf/2*(2*$i+1))] 1 1;
	math::linearalgebra::setrow Fib $fibNo [expr ($y1+$y2)/2] 2 2;
	math::linearalgebra::setrow Fib $fibNo [expr $dbf*$t] 3 3;
	}
#
for {set i 0} {$i<$nfC} {incr i 1} {#Top Left corner
	#Fiber No, x,y, Area, warping(to be included later)	
	set fibNo [expr $i+$nfC+$nfL+$nfbf]
	math::linearalgebra::setrow Fib $fibNo $fibNo 0 0;
	math::linearalgebra::setrow Fib $fibNo [expr $z3+($r+$t/2)*cos($pi/2+$theta/2*(2*$i+1))] 1 1;
	math::linearalgebra::setrow Fib $fibNo [expr $y3+($r+$t/2)*sin($pi/2+$theta/2*(2*$i+1))] 2 2;
	math::linearalgebra::setrow Fib $fibNo $cArea 3 3;
	}
for {set i 0} {$i<$nfdw} {incr i 1} {#Web
	set fibNo [expr $i+2*$nfC+$nfL+$nfbf]
	math::linearalgebra::setrow Fib $fibNo $fibNo 0 0;
	math::linearalgebra::setrow Fib $fibNo [expr ($z1+$z2)/2] 1 1;
	math::linearalgebra::setrow Fib $fibNo [expr $y3-($dwf/2*(2*$i+1))] 2 2;
	math::linearalgebra::setrow Fib $fibNo [expr $dwf*$t] 3 3;
	}
#	
for {set i 0} {$i<$nfC} {incr i 1} {#Bottom Left corner
	#Fiber No, x,y, Area, warping(to be included later)	
	set fibNo [expr $i+2*$nfC+$nfL+$nfbf+$nfdw]
	math::linearalgebra::setrow Fib $fibNo $fibNo 0 0;
	math::linearalgebra::setrow Fib $fibNo [expr $z3+($r+$t/2)*cos($pi+$theta/2*(2*$i+1))] 1 1;
	math::linearalgebra::setrow Fib $fibNo [expr -$y3+($r+$t/2)*sin($pi+$theta/2*(2*$i+1))] 2 2;
	math::linearalgebra::setrow Fib $fibNo $cArea 3 3;
	}
for {set i 0} {$i<$nfbf} {incr i 1} {#Bottom flange
	set fibNo [expr $i+3*$nfC+$nfL+$nfbf+$nfdw]
	math::linearalgebra::setrow Fib $fibNo $fibNo 0 0;
	math::linearalgebra::setrow Fib $fibNo [expr $z3+($dbf/2*(2*$i+1))] 1 1;
	math::linearalgebra::setrow Fib $fibNo [expr -($y1+$y2)/2] 2 2;
	math::linearalgebra::setrow Fib $fibNo [expr $dbf*$t] 3 3;
	}

for {set i 0} {$i<$nfC} {incr i 1} {#Bottom right corner
	#Fiber No, x,y, Area, warping(tobe included later)	
	set fibNo [expr $i+3*$nfC+$nfL+2*$nfbf+$nfdw]
	math::linearalgebra::setrow Fib $fibNo $fibNo 0 0;
	math::linearalgebra::setrow Fib $fibNo [expr $z4+($r+$t/2)*cos(3*$pi/2+$theta/2*(2*$i+1))] 1 1;
	math::linearalgebra::setrow Fib $fibNo [expr -$y3+($r+$t/2)*sin(3*$pi/2+$theta/2*(2*$i+1))] 2 2;
	math::linearalgebra::setrow Fib $fibNo $cArea 3 3;
	}	
for {set i 0} {$i<$nfL} {incr i 1} {#bottom lip
	set fibNo [expr $i+4*$nfC+$nfL+2*$nfbf+$nfdw]
	math::linearalgebra::setrow Fib $fibNo $fibNo 0 0;
	math::linearalgebra::setrow Fib $fibNo [expr ($z5+$z6)/2] 1 1;
	math::linearalgebra::setrow Fib $fibNo [expr -$y3+($dfL/2*(2*$i+1))] 2 2;
	math::linearalgebra::setrow Fib $fibNo [expr $dfL*$t] 3 3;
	}
#-----------------------------------------------------------------------------------------------------------------
#fiber x,y
for {set i 0} {$i<$NoOfFiber} {incr i 1} {
	set fId($i) [math::linearalgebra::getelem $Fib $i 0]
	set f_x($i) [math::linearalgebra::getelem $Fib $i 1];
	set f_y($i) [math::linearalgebra::getelem $Fib $i 2]
	set f_A($i) [math::linearalgebra::getelem $Fib $i 3]
}
#Interpolate and assign sectorial coordinates to fiber
set secCoord [Interpolate $Fib $corwarpInfo];

for {set i 0} {$i<$NoOfFiber} {incr i 1} {
	set wn($i) [lindex $secCoord $i 1];#Revised on 25 May 2019 conforming to Vlasov's sign convention
}
#Create fiber section
#---------------------------------------------------------------------------------
set poissonX 0.3; #Xinlong
set GX [expr 200000.0/(2*(1+$poissonX))]; #Xinlong
set GJX [expr $GX*$J]; #Xinlong
section Fiber $secID $yo $xo -GJ $GJX {          
	for {set i 0} {$i<$NoOfFiber} {incr i 1} {
	fiber $f_y($i) $f_x($i) $f_A($i) $matID; #Xinlong yLoc, zLoc, Area, materialID, sectorial coordinate, y_coord, and z_coord of shear centre
	}
	}
return $shearCentre; #returns shear centre coordinate to the main file
}

