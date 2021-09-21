What is this package for?
============================

This pacakge is for when you want to edit athena and test the impact on AnalysisBase. This is useful if,
for instance, you are developing the AsgPhotonIsEMSelector, and you would prefer to test things out on your
usual AnalysisBase code instead of having to have a full-blown athena setup.

As a prerequisite, you must add the following lines to your `~/.gitconfig` file (with your username instead of brendlin):
```
[atlas]
      user = brendlin
```

You also need to make a **fork of athena** (see https://atlassoftwaredocs.web.cern.ch/gittutorial/gitlab-fork/) before beginning.

How to use it
=============================

The general steps so far are, after checking out the package, do:
 
 ```
 source setupArea.sh
 ```
 
This will check out athena in the source directory (sparse checkout), add some egamma packages,
add egammaOrigin as a remote, and fetch the upstream.

Then, in the `source/the_asetup.sh` file, you must change the `MY_RELEASE` environment variable to the intended Athena release. Then you can use this script (and the shortcuts defined within it) to run asetup, run cmake make and build commands (see below):

 
 ```
 cd source
 source the_asetup.sh
 mymake
 mybuild
 ```
 
 where `mymake` and `mybuild` are defined in the_asetup.sh (they are just wrapers of the normal cmake commands, modified so that the package_filters are picked up).
 
