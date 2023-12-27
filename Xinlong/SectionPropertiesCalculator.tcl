#This program computes the section properties of thin-walled open sections \
#  
# Written by: Rinchen  
# Date: 6 Oct 2015
# PhD student: University of Sydney, Sydney NSW, Australia
#
# Comments:
# NodeCoordinates contain nodeNumber, x- and y-coordinate of each node
# ElementInfo contains elementNumber, starNode, endNode, segment thickness
#
# Numerical integration schemes follow Simpson's Rule
#
#References:
# Papangelis, J. P. and G. J. Hancock (1995). "Computer analysis of thin-walled structural members." Computers & Structures 56(1): 157-176.
# Lue, D. M., J.-L. Liu and C.-H. Lin (2007). "Numerical evaluation on warping constants of general cold-formed steel open sections."
#
#-------------------------------------------------------------------------------------------------------------
proc SectionProperties {NodeCoordinates ElementInfo} {

	set NodeCoord $NodeCoordinates
	set Segment $ElementInfo
	set NoOfNodes [llength $NodeCoordinates]
	set NoOfElements [llength $ElementInfo]

#----Pick up the nodal coordinates corresponding to respective element ends
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	set k [expr $i+1]
	set segId [math::linearalgebra::getelem $Segment $i 0]; #search indicator
	set nodei [math::linearalgebra::getelem $Segment $i 1]; #search indicator
	set nodej [math::linearalgebra::getelem $Segment $i 2]; #search indicator
	
	set xi($k) [math::linearalgebra::getelem $NodeCoord [expr $nodei-1] 1];
	set yi($k) [math::linearalgebra::getelem $NodeCoord [expr $nodei-1] 2];
	set xj($k) [math::linearalgebra::getelem $NodeCoord [expr $nodej-1] 1];
	set yj($k) [math::linearalgebra::getelem $NodeCoord [expr $nodej-1] 2];
	set tij($k) [math::linearalgebra::getelem $Segment [expr $segId-1] 3];
	#puts "$nodei $nodej  $xi($k)  $yi($k) $xj($k)  $yj($k) $tij($k)"
}
#Calculate segment properties: centroid, area 	
		set AreaSec 0.0;
		set Axc 0.0;
		set Ayc 0.0;
		
for {set i 1} {$i<$NoOfNodes} {incr i 1} {
	set dxi($i) [expr $xi($i)-$xj($i)];#difference in x-coord
	set dyi($i) [expr $yi($i)-$yj($i)]; #difference in y-coord
	set Lij($i) [expr sqrt($dxi($i)*$dxi($i)+$dyi($i)*$dyi($i))];#length of segment
	set Aij($i) [expr $Lij($i)*$tij($i)]; #area of segment
	set xc($i) [expr ($xi($i)+$xj($i))/2];#x-coord of centroid of segment
	set yc($i) [expr ($yi($i)+$yj($i))/2];#y-coord of centroid of segment	
	set Axc [expr $Axc+$Aij($i)*$xc($i)]; #Sum(A*xc)
	set Ayc [expr $Ayc+$Aij($i)*$yc($i)];#Sum (A*yy)
	set AreaSec [expr $AreaSec+$Aij($i)]
}

#Calculate centroid of whole section from the extreme bottom left
set xc0 [expr $Axc/$AreaSec];
set yc0 [expr $Ayc/$AreaSec];

#Calculate second moment of area and polar moment of section w.r.t centroid
set Ixx 0.0;
set Iyy 0.0;
set Ixy 0.0;

for {set i 1} {$i<$NoOfNodes} {incr i 1} {
	set xii 0.0;
	set xjj 0.0;
	set yii 0.0;
	set yjj 0.0;
	
	set xii [expr ($xi($i)-$xc0)];
	set xjj [expr ($xj($i)-$xc0)];
	set yii [expr ($yi($i)-$yc0)];
	set yjj [expr ($yj($i)-$yc0)];
	
	set Ixx [expr $Ixx+($yii*$yii+$yii*$yjj+$yjj*$yjj)*$Lij($i)*$tij($i)/3];
	set Iyy [expr $Iyy+($xii*$xii+$xii*$xjj+$xjj*$xjj)*$Lij($i)*$tij($i)/3];
	set Ixy [expr $Ixy+(($xii*$yii+$xjj*$yjj)/3+($xii*$yjj+$xjj*$yii)/6)*$Lij($i)*$tij($i)];
}
#Calculate principal moment of area of a whole section
if {$Ixy==0.0} {set eps 0.000001} else {set eps 0.0} ;
set delta [expr sqrt(($Ixx-$Iyy)*($Ixx-$Iyy)/4+$Ixy*$Ixy)];
set Ipxx [expr ($Ixx+$Iyy)/2+$delta];#Imax
set Ipyy [expr ($Ixx+$Iyy)/2-$delta];#Imin
set alpha [expr atan(($Ixx-$Ipxx)/($Ixy+$eps))];#Inclination of principal axes in radians: +ve for anti-clockwise
set pi [expr 2*asin(1.0)];
set alphadeg [expr $alpha*180/$pi];
#Transform nodal coordinates to principal axis system
for {set i 1} {$i<$NoOfNodes} {incr i 1} {
		set xi0($i) [expr ($yi($i)-$yc0)*sin($alpha)+($xi($i)-$xc0)*cos($alpha)];
		set yi0($i) [expr ($yi($i)-$yc0)*cos($alpha)-($xi($i)-$xc0)*sin($alpha)];
		set xj0($i) [expr ($yj($i)-$yc0)*sin($alpha)+($xj($i)-$xc0)*cos($alpha)];
		set yj0($i) [expr ($yj($i)-$yc0)*cos($alpha)-($xj($i)-$xc0)*sin($alpha)];

#	puts "$xi0($i)  $yi0($i) $xj0($i)  $yj0($i) "
}

#----Calculate sectorial area of Segment with respect to centroid
for {set i 1} {$i<$NoOfNodes} {incr i 1} {
	set Aoc($i) [expr ($xi0($i)*$yj0($i)-$xj0($i)*$yi0($i))]
#	puts $Aoc($i)
}
#------------Determine sectorial coordinate w.r.t centroid------------

# Create matrix to store warping displacement dof at each node at element ends
set WarpingCoord [math::linearalgebra::mkMatrix $NoOfElements 3 0]

for {set i 0} {$i<$NoOfElements} {incr i 1} {
	math::linearalgebra::setelem WarpingCoord $i 0 [expr $i+1];#Element ID
	math::linearalgebra::setelem WarpingCoord $i 1 [expr 2*($i+1)-1];#Warping displacement dof at node i
	math::linearalgebra::setelem WarpingCoord $i 2 [expr 2*($i+1)];#Warping displacement dof at node j
}

#Construct matrix Cw ([Cw]{w}=df/dz(Fi))
set Cw [math::linearalgebra::mkMatrix [expr 2*$NoOfElements] [expr 2*$NoOfElements] 0]
set lastRow [expr 2*$NoOfElements-1];

#Construct NoOfElement rows for element equations in Cw
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	math::linearalgebra::setelem Cw $i [expr 2*$i] -1.0;
	math::linearalgebra::setelem Cw $i [expr 2*$i+1] 1.0;
}

#Construct rows corresponding to compatibility equations in Cw
set rowNum [expr $NoOfElements-1];#starting row number for compatibility equations

for {set i 1} {$i<[expr $NoOfElements+1]} {incr i 1} {
	set found 0
	for {set j 1} {$j<[expr $NoOfElements+1]} {incr j 1} {#compare the occurrence of each node in ith and jth column
		set node1 [lindex $Segment [expr $j-1] 1]
		set node2 [lindex $Segment [expr $j-1] 2]		
		if {$i==$node1 | $i==$node2} {
			set found [expr $found+1]			
				if {$i==$node1} {
					set ele($found) $j
					set acol($found) 1
						if {$found ==1} {set windex [lindex $WarpingCoord [expr $ele($found)-1] 1]}
					}
				if {$i==$node2} {
					set ele($found) $j
					set acol($found) 2
					if {$found ==1} {set windex [lindex $WarpingCoord [expr $ele($found)-1] 2]}
					}
		}
		
	}
		if {$found>1} {
			set colpos1 $windex ;# sets the ith column position in Cw matrix for wi
			for {set k 2} {$k<[expr $found+1]} {incr k 1} {
				set rowNum [expr $rowNum+1]
				set colpos2 [lindex $WarpingCoord [expr $ele($k)-1] $acol($k)];#sets the jth column position for wj
				math::linearalgebra::setelem Cw $rowNum [expr $colpos1-1] 1.0;
				math::linearalgebra::setelem Cw $rowNum [expr $colpos2-1] -1.0;
			}
		}	
}
	
#Construct last row for normalized warping equation in Cw
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	set j [expr $i+1]
	math::linearalgebra::setelem Cw $lastRow [expr 2*$i] [expr $Aij($j)/2];
	math::linearalgebra::setelem Cw $lastRow [expr 2*$i+1] [expr $Aij($j)/2];
}
#Construct column vector Fi
set Fi [math::linearalgebra::mkVector [expr 2*$NoOfElements] 0];

for {set i 0} {$i<$NoOfElements} {incr i 1} {
	math::linearalgebra::setelem Fi $i [expr $Aoc([expr $i+1])];	
}

#----Solve for sectorial coordinate w.r.t centroid
set omc	[math::linearalgebra::solvePGauss $Cw $Fi];

#---Assign sectorial coordinate at each end of segment
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	set j [expr $i+1]
	set wci($j) [math::linearalgebra::getelem $omc [expr 2*$i] 0]
	set wcj($j) [math::linearalgebra::getelem $omc [expr 2*$i+1] 0]
#	puts "$wci($j)   $wcj($j)"
}

set Iwx 0.0
set Iwy 0.0
#puts "wi   yi    wj    yj    Lij    tij   "
#puts "------------------------------------"
for {set i 1} {$i<[expr $NoOfElements+1]} {incr i 1} {
	set Iwx [expr $Iwx+(($wci($i)*$xi0($i)+$wcj($i)*$xj0($i))/3+($wci($i)*$xj0($i)+$wcj($i)*$xi0($i))/6)*$Lij($i)*$tij($i)];
	set Iwy [expr $Iwy+(($wci($i)*$yi0($i)+$wcj($i)*$yj0($i))/3+($wci($i)*$yj0($i)+$wcj($i)*$yi0($i))/6)*$Lij($i)*$tij($i)];
	#puts "$wci($i) $yi0($i) $wcj($i) $yj0($i)  $Lij($i)  $tij($i)  "
}

#Calculate shear centre w.r.t centroid and in principal axes
set xo [expr (-$Ipyy*$Iwy)/(-$Ipxx*$Ipyy)];
set yo [expr ($Ipxx*$Iwx)/(-$Ipxx*$Ipyy)];

#Calculate shear centre coordinate w.r.t rectangular axes
set Y0 [expr $xo*sin($alpha)+$yo*cos($alpha)+$yc0];
set X0 [expr $xo*cos($alpha)-$yo*sin($alpha)+$xc0];

#Calculate sectorial area with respect to shear centre
for {set i 1} {$i<[expr $NoOfElements+1]} {incr i 1} {
	set j [expr $i+1]
	set Aos($i) [expr -(($yj0($i)-$yi0($i))*$xo+($xi0($i)-$xj0($i))*$yo-($xi0($i)*$yj0($i)-$xj0($i)*$yi0($i)))]
}

#-----Calculate warping constant------------
#Calculate normalized sectorial coordinate w.r.t shear centre
set Fi0 [math::linearalgebra::mkVector [expr 2*$NoOfElements] 0];

for {set i 0} {$i<$NoOfElements} {incr i 1} {
	math::linearalgebra::setelem Fi0 $i [expr $Aos([expr $i+1])];		
}
set om0	[math::linearalgebra::solvePGauss $Cw $Fi0];

#Assemble the sectorial coordinates at the element ends with reversed sign 
#puts "Woi  Woj"
#puts "----------------------------"
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	set j [expr $i+1]
	set wni($j) [expr -[math::linearalgebra::getelem $om0 [expr 2*$i] 0]];
	set wnj($j) [expr -[math::linearalgebra::getelem $om0 [expr 2*$i+1] 0]];
#	puts "$wni($j)   $wnj($j)"
}

#-----------------Compute warping constant Iw----------------------------------------------
set Iw 0.0

for {set i 1} {$i<[expr $NoOfElements+1]} {incr i 1} {
	set Iw [expr $Iw+($wni($i)*$wni($i)+$wni($i)*$wnj($i)+$wnj($i)*$wnj($i))/3*$Lij($i)*$tij($i)];
}

#Assemble sectorial coordinates corresponding to each node
for {set i 1} {$i<[expr $NoOfNodes+1]} {incr i 1} {
	for {set j 0} {$j<$NoOfElements} {incr j 1} {
		set elNo [lindex $Segment $j 0]
		set node1 [lindex $Segment $j 1]
		set node2 [lindex $Segment $j 2]
		
		if {$i == $node1} {
		set wnn($node1) $wni($elNo)
		}
		if {$i == $node2} {
		set wnn($node2) $wnj($elNo) 
		}
	}
}
# Calculate torsional constant J and monosymmetry parameter betax, betay

set J 0.0;
set betax 0.0;
set betay 0.0;

for {set i 1} {$i<[expr $NoOfElements +1]} {incr i 1} {
  set J [expr $J+$Lij($i)*$tij($i)*$tij($i)*$tij($i)/3]

  set yiyj [expr $yi0($i)+$yj0($i)]
  set xixj [expr $xi0($i)+$xj0($i)]	
	
  set betax  [expr $betax+($yi0($i)*($xi0($i)*$xi0($i)+$yi0($i)*$yi0($i))+0.5*$yiyj*($xixj*$xixj+$yiyj*$yiyj)+$yj0($i)*($xj0($i)*$xj0($i)+$yj0($i)*$yj0($i)))*$Aij($i)/6]
  set betay  [expr $betay+($xi0($i)*($xi0($i)*$xi0($i)+$yi0($i)*$yi0($i))+0.5*$xixj*($xixj*$xixj+$yiyj*$yiyj)+$xj0($i)*($xj0($i)*$xj0($i)+$yj0($i)*$yj0($i)))*$Aij($i)/6]	    
}

set betax [expr $betax/$Ipxx-2.0*$yo]
set betay [expr $betay/$Ipyy-2.0*$xo]

#Create matrix to store coordinates and warping function at element endI and endJ
#Center and torsional constant J information are stored in 7th column

if {$NoOfElements<6} {set NoOfRows 6} else {set NoOfRows $NoOfElements} ; # ensures that row is never less than 6 to hold additional data in 7th column!

set CoordAndWarping [math::linearalgebra::mkMatrix $NoOfRows 7 0.0];

for {set i 0} {$i<$NoOfElements} {incr i 1} {
    set k [expr $i+1]
    math::linearalgebra::setrow CoordAndWarping $i $xi0($k) 0 0;
    math::linearalgebra::setrow CoordAndWarping $i $yi0($k) 1 1;
    math::linearalgebra::setrow CoordAndWarping $i $wni($k) 2 2;
    math::linearalgebra::setrow CoordAndWarping $i $xj0($k) 3 3;
    math::linearalgebra::setrow CoordAndWarping $i $yj0($k) 4 4;
    math::linearalgebra::setrow CoordAndWarping $i $wnj($k) 5 5;   
}
    math::linearalgebra::setcol CoordAndWarping 6 $xc0 0 0; #x-coord of centroid of the section
    math::linearalgebra::setcol CoordAndWarping 6 $yc0 1 1;# y -coordinate of centrod of the section
    math::linearalgebra::setcol CoordAndWarping 6 $xo 2 2;#x-coord of shear center
    math::linearalgebra::setcol CoordAndWarping 6 $yo 3 3;#y-coord of shear center
    math::linearalgebra::setcol CoordAndWarping 6 $J 4 4;#Torsional constant
    math::linearalgebra::setcol CoordAndWarping 6 $alpha 5 5;#orientation of principal axes

#=====================================================================================================================
#Write calculated section properties to the file SectionProperties.txt
#---------------------------------------------------------------------------------------------------
set fid [open SectionProperties.txt w]	

puts $fid "Open Section Properties"
puts $fid "----------------------------------------------"
#puts "Area:format "%.4f" $AreaSec"
puts $fid "Area:  [format "%.4f" $AreaSec]"
puts $fid " "
puts $fid "Second moment,product moment of area about rectangular axes"
puts $fid "Ix:    [format "%.4f" $Ixx]"
puts $fid "Iy:    [format "%.4f" $Iyy]"
puts $fid "Ixy:   [format "%.4f" $Ixy]"
puts $fid ""
puts $fid "Second moment of area about principal axes"
puts $fid "Ipxx:  [format "%.4f" $Ipxx]"
puts $fid "Ipyy:  [format "%.4f" $Ipyy]"
puts $fid ""
puts $fid "Torsion constant,  J: [format "%.4f" $J]"
puts $fid "Warping constant, Iw: [format "%.4f" $Iw]"
puts $fid ""
puts $fid "Coordinates of centroid from bottom left"
puts $fid "xc0:	[format "%.4f" $xc0] "
puts $fid "yc0:	[format "%.4f" $yc0] " 
puts $fid ""
puts $fid "Coordinates of shear centre w.r.t rectangular axes"
puts $fid "Xs:	[format "%.4f" $X0] "
puts $fid "Ys:	[format "%.4f" $Y0] "
puts $fid ""
puts $fid "Coordinates of shear centre in principal axes"
puts $fid "x0:	[format "%.4f" $xo] "
puts $fid "y0:	[format "%.4f" $yo] "
puts $fid ""
puts $fid "Orientation of principal axes"
puts $fid "alpha:	[format "%.6f" $alpha] radian([format "%.4f" $alphadeg] deg)"
puts $fid " "
puts $fid "Monosymmetry section constants"
puts $fid "betax: 	[format "%.4f" $betax]"
puts $fid "betay: 	[format "%.4f" $betay]"
puts $fid "    "
puts $fid "Normalized Sectorial coordinate"
puts $fid " Node       Sectorial Coordinate"
puts $fid "---------------------------"
for {set i 1} {$i<[expr $NoOfNodes+1]} {incr i 1} {
	puts $fid "$i     [format "%.4f" $wnn($i)]"
}
close $fid
return $CoordAndWarping; # returns this matrix to the other file
}
