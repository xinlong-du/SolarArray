section Fiber $ColSecTag $y0 $z0 -GJ $GJ {
	for {set i 1} {$i<51} {incr i 1} {
    	fiber [expr -40.8+1.6*$i] -20.998 2.56 $matID;
    }

    for {set i 1} {$i<41} {incr i 1} {
    	fiber -39.2 [expr -21.798+1.6-0.71+1.42*$i] 2.272 $matID;
    	fiber 39.2 [expr -21.798+1.6-0.71+1.42*$i] 2.272 $matID;
    }

    for {set i 1} {$i<11} {incr i 1} {
    	fiber [expr 29.5+1.0*$i] 37.402 1.6 $matID;
    	fiber [expr -40.5+1.0*$i] 37.402 1.6 $matID;
    }

}