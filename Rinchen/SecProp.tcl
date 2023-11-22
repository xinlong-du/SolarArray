#This function calls the functions "sectionData" and "SectionProperties" to compute the section properties
# and stores the results in textfile "SectionProperties.txt"
#
#Written by:
#Rinchen
#PhD student
#University of Sydney, Australia
#23 October 2015

#-------------------------------------------------------
source sectionData.tcl
source SectionPropertiesCalculator.tcl

#-----------------------------------------------
#Enter dimensions for the open cross-sections
#------------------------------------------------
#1)Plain C section without lips
#set D 20.0
#set Bt 5.0
#set Bb 50.0
#set tw 1.5
#set tf 1.5
##------------------------------------------------
#set data [plainCSectionWithoutLipInfo $D $Bt $Bb $tw $tf];#C-sections without lips
#==========================================================
#2)C-Sections
set D 100.0;#depth
set B 75.0; #flange width
set L 16.5; #Lip length
set t 1.5;  #thickness
set r 1.5;  #Inside corner radius
#-------------------------------------------------------
#set data [plainCSectionInfo $D $B $L $t];#channel sections with lips but without curved corners 
set data [roundCornerCSectionInfo $D $B $L $t $r];#channel sections with curved corners 
#set data [roundCornerCSectionInfoLipTurnUp $D $B $L $t $r];#Asymmetric sections - variant of C-sections
#==========================================================
#3)I-Sections
#set D 100.0
#set B 75.0
#set tw 3.0
#set tf 3.0
#set bfactor 0.5; #0<bfactor<1 Defines the location of web along the flange (0 = left end; 1 = right end)
#-------------------------------------------------------
#set data [plainISectionInfo $D $B $tf $tw $bfactor];#prepares data for calculation of section properties
#==========================================================
#
#Calculate section properties
#-------------------------------------------------------

proc secProperties {data} {
   set NodeCoord [lindex [lindex $data] 0]; #NodeInfo
   set Segment [lindex [lindex $data] 1]; #SegmentInfo 
   set r [SectionProperties $NodeCoord $Segment];#Calculates section properties   
}
secProperties $data;
puts ""
puts "Section properties written to a file 'SectionProperties.txt'"
puts ""
#--------------------------------------------------------------




