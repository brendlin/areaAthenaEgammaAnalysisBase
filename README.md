What is this package for?
============================

This pacakge is for when you want to edit athena and test the impact on AnalysisBase. This is useful if,
for instance, you are developing the AsgPhotonIsEMSelector, and you would prefer to test things out on your
usual AnalysisBase code instead of having to have a full-blown athena setup.

How to use it
=============================

The general steps so far are:

 - Check out the package, then:
 
 ```
 source setupArea.sh
 cd source
 source the_asetup.sh
 mymake
 mybuild
 ```
 
 where mymake and mybuild are defined in the_asetup.sh (they are just wrapers of the normal cmake commands).
 
