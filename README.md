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

Running Reconstruction on the DESY batch
============
This package can also facilitate running on the DESY batch nodes in order to avoid running on the grid (and presumably it can be easily amended to run on other batch systems too).

Replicate RDO files locally
---------

First, one must replicate the target RDO onto the `DESY-HH_LOCALGROUPDISK` RSE (using e.g. `rucio add-rule mc16_13TeV:mc16_13TeV.00000000...r10470 1 DESY-HH_LOCALGROUPDISK`). Then one must prepare a file that contains a list of all of the replicated files on the NAF, using `rucio list-file-replicas`. Here is an example command that strips down most of the extra content:

```bash
rucio list-file-replicas mc16_13TeV.423001.ParticleGun_single_photon_egammaET.recon.RDO.e3566_s3113_r10470 | grep DESY-HH_LOCALGROUPDISK | sort | cut -d'|' -f6,8 | sed 's/[ \t]*$//'
```

Then edit this output mildly to get it into the following format, and put it into a text file which we will call `RDOfiles.txt` here:
```bash
/pnfs/desy.de/atlas/dq2/atlaslocalgroupdisk/rucio/mc16_13TeV/c7/66/RDO.14016886._000001.pool.root.1
/pnfs/desy.de/atlas/dq2/atlaslocalgroupdisk/rucio/mc16_13TeV/3e/40/RDO.14016886._000002.pool.root.1
/pnfs/desy.de/atlas/dq2/atlaslocalgroupdisk/rucio/mc16_13TeV/7a/c2/RDO.14016886._000003.pool.root.1
/pnfs/desy.de/atlas/dq2/atlaslocalgroupdisk/rucio/mc16_13TeV/3a/6e/RDO.14016886._000004.pool.root.1
/pnfs/desy.de/atlas/dq2/atlaslocalgroupdisk/rucio/mc16_13TeV/dc/50/RDO.14016886._000005.pool.root.1
```

Submit to the NAF batch
--------

Three files are responsible for submitting the jobs to the NAF:
 - `doSubmit.sh`: Creates the job directory structure and submits to condor
 - `submit`: the condor submit script
 - `batchRun`: the script that is executed on the batch node (runs `reco_tf.py`)
 - `setupRecoTf.sh`: called during the batch job, it defines the **conditions tag**, the **pre-exec** and the **post-exec** arguments for `reco_tf.py`

To run and send output to a directory named `outputDir`, do:
```
source doSubmit.sh RDOfiles.txt outputDir
```

A few notes:
 - `doSubmit.sh` and `batchRun` conspire to submit 2 jobs per file, with 1000 events per job (there are 2000 events in the RDOs used now). This is done in order to limit the length of the job to less than 3 hours (the default NAF time limit), which makes the jobs run much much faster on the NAF. If this scheme needs to be changed (for example if the jobs are taking too long or if there are more/less than 2000 events per job), then these two files would need to be modified.

The resulting AOD files can be found in the directories e.g. `outputDir/job000`.

BONUS: Creating a flat ntuple from an AOD (for photon conversion studies)
--------
It is widely understood that running over AODs is time-consuming and frustrating; it would be better to move to a flat ntuple as quickly as possible in order to work more efficiently. Therefore a script has been created to run a straightforward selection on photons and dump the results into an output ntuple.

The ntuple relies on a back-end from the `genericUtils` package. To run the ntupler, simply run:

```bash
source makeFlatNtuple.sh outputDir
```
where `outputDir` is the output directory from your batch `reco_tf` run. This will make a flat ntuple in a new "ntuple" directory, ready for you to explore. To see what goes into the selection for the flat ntuple, you can find the selection macro at `conversionTuningTRT.h`.
