proc Interpolate {fiberCoordinate SegmentInfo} {
#This procedure determines the sectorial coordinate at the centroid of each fiber by linearly interpolating between the sectorial coordinates at
#the element ends
#
# Written by: Rinchen  
# Date: 12 Oct 2015
# PhD student: University of Sydney, Sydney NSW, Australia
#
# Input parameters:
# fiberCoordinate contains fiberID, x-,y-coordinates of fiber centroid, Area of fiber
# SegmentInfo contains x-,y-,w- coordinates at ith and jth end of element
#
set NoOfFiber [llength $fiberCoordinate];
set NoOfElements [llength $SegmentInfo];

#Extract coordinates and warping info at the ends of the element
for {set i 0} {$i<$NoOfElements} {incr i 1} {
	set j [expr $i+1]
	set xi0($j) [lindex $SegmentInfo $i 0]; 
	set yi0($j) [lindex $SegmentInfo $i 1];
	set w0i($j) [lindex $SegmentInfo $i 2];
	set xj0($j) [lindex $SegmentInfo $i 3];
	set yj0($j) [lindex $SegmentInfo $i 4];
	set w0j($j) [lindex $SegmentInfo $i 5];
	#puts "$xi0($j)      $yi0($j)      $w0i($j)      $xj0($j)      $yj0($j)      $w0j($j)"
}

#Extract x,y coordinates of fiber centroid
for {set i 0} {$i<$NoOfFiber} {incr i 1} {
	set fId($i) [math::linearalgebra::getelem $fiberCoordinate $i 0]
	set f_x($i) [math::linearalgebra::getelem $fiberCoordinate $i 1];
	set f_y($i) [math::linearalgebra::getelem $fiberCoordinate $i 2]
	#set f_A($i) [math::linearalgebra::getelem $Fib $i 3]
        #puts "$i   $f_x($i)     $f_y($i)"
}

#Determines the sectorial coordinate at centroid of each fiber
set esp 0.15; #set tolerance for numerical roundoff
for {set i 1} {$i<[expr $NoOfElements+1]} {incr i 1} {
	for {set j 0} {$j<$NoOfFiber} {incr j 1} {
		
	if {($f_x($j)>=[expr $xi0($i)-$esp] && $f_x($j)<=[expr $xj0($i)+$esp]) && ($f_y($j)>=[expr $yi0($i)-$esp] && $f_y($j)<=[expr $yj0($i)+$esp])} {
		set d sqrt(($f_x($j)-$xi0($i))*($f_x($j)-$xi0($i))+($f_y($j)-$yi0($i))*($f_y($j)-$yi0($i)))
		set dij sqrt(($xj0($i)-$xi0($i))*($xj0($i)-$xi0($i))+($yj0($i)-$yi0($i))*($yj0($i)-$yi0($i)))
		set w($j) [expr $w0i($i)+$d/$dij*($w0j($i)-$w0i($i))]
               # puts "$j  $w($j)"
		}
		
	if {($f_x($j)>=[expr $xi0($i)-$esp] && $f_x($j)<=[expr $xj0($i)+$esp]) && ($f_y($j)<=[expr $yi0($i)+$esp] && $f_y($j)>=[expr $yj0($i)-$esp])} {
		set d sqrt(($f_x($j)-$xi0($i))*($f_x($j)-$xi0($i))+($f_y($j)-$yi0($i))*($f_y($j)-$yi0($i)))
		set dij sqrt(($xj0($i)-$xi0($i))*($xj0($i)-$xi0($i))+($yj0($i)-$yi0($i))*($yj0($i)-$yi0($i)))
		set w($j) [expr $w0i($i)+$d/$dij*($w0j($i)-$w0i($i))]
              #  puts "$j  $w($j)"
                }	
		
	if {($f_x($j)<=[expr $xi0($i)+$esp] && $f_x($j)>=[expr $xj0($i)-$esp]) && ($f_y($j)>=[expr $yi0($i)-$esp] && $f_y($j)<=[expr $yj0($i)+$esp])} {
		set d sqrt(($f_x($j)-$xi0($i))*($f_x($j)-$xi0($i))+($f_y($j)-$yi0($i))*($f_y($j)-$yi0($i)))
		set dij sqrt(($xj0($i)-$xi0($i))*($xj0($i)-$xi0($i))+($yj0($i)-$yi0($i))*($yj0($i)-$yi0($i)))
		set w($j) [expr $w0i($i)+$d/$dij*($w0j($i)-$w0i($i))]
                #  puts "$j  $w($j)"
		}
		
	if {($f_x($j)<=[expr $xi0($i)+$esp] && $f_x($j)>=[expr $xj0($i)-$esp]) && ($f_y($j)<=[expr $yi0($i)+$esp] && $f_y($j)>=[expr $yj0($i)-$esp])} {
		set d sqrt(($f_x($j)-$xi0($i))*($f_x($j)-$xi0($i))+($f_y($j)-$yi0($i))*($f_y($j)-$yi0($i)))
		set dij sqrt(($xj0($i)-$xi0($i))*($xj0($i)-$xi0($i))+($yj0($i)-$yi0($i))*($yj0($i)-$yi0($i)))
		set w($j) [expr $w0i($i)+$d/$dij*($w0j($i)-$w0i($i))]
		}	
	}
}

#set nodeInfo [math::linearalgebra::mkMatrix $NoOfNodes 3 0.0];
#
#for {set i 0} {$i<$NoOfNodes} {incr i 1} {
#	     set k [expr $i+1]
#	set j 0
#	while {$j<$NoOfElements} {
#		set elNo [lindex $Segment $j 0]
#		set node1 [lindex $Segment $j 1]
#		set node2 [lindex $Segment $j 2]
#		if {$k == $node1} {
#			#math::linearalgebra::setrow nodeInfo $i $k 0 0;
#			math::linearalgebra::setrow nodeInfo $i $xi0($elNo) 0 0;
#			math::linearalgebra::setrow nodeInfo $i $yi0($elNo) 1 1;
#			math::linearalgebra::setrow nodeInfo $i \{\{$w0i($elNo)\}\} 2 2;		
#		}
#		if {$k == $node2} {
#			#math::linearalgebra::setrow nodeInfo $i $k 0 0;
#			math::linearalgebra::setrow nodeInfo $i $xj0($elNo) 0 0;
#			math::linearalgebra::setrow nodeInfo $i $yj0($elNo) 1 1;
#			math::linearalgebra::setrow nodeInfo $i "{\{$w0j($elNo)\}}" 2 2;
#		}
#		set j [expr $j+1]		
#	}	
#}
#
#set fiberInfo [math::linearalgebra::mkMatrix $NoOfFiber 2 0.0]
#for {set i 0} {$i<$NoOfFiber} {incr i 1} {
#	#math::linearalgebra::setrow fiberInfo $i $fId($i) 0 0;
#	math::linearalgebra::setrow fiberInfo $i $f_x($i) 0 0;
#	math::linearalgebra::setrow fiberInfo $i $f_y($i) 1 1;
#}
#
#foreach coord {$fiberInfo} {
#	 puts "$coord: [::math::interpolate::interp-spatial $nodeInfo $fiberInfo]"
#}
# Assemble sectorial coordinates to return
set fiberSectCoord [math::linearalgebra::mkMatrix $NoOfFiber 2 0];

for {set i 0} {$i<$NoOfFiber} {incr i 1} {
    math::linearalgebra::setrow fiberSectCoord $i $i 0 0;
    math::linearalgebra::setrow fiberSectCoord $i $w($i) 1 1;    
}
return $fiberSectCoord
}
