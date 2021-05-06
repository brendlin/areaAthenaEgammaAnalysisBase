#!/bin/bash

# asetup AthGeneration,21.6.57,here
INPUT=$1 # Example is: GridDirectFiles/example.txt
THEDIR=$2 # Old directory was: run_batchFromGridpack

GREEN='\033[0;32m'
NC='\033[0m' # No Color

if [ -z "$TestArea" ]
then
    # Make the directory, copy submit and run files there.
    mkdir -p $THEDIR

    cp batchRun $THEDIR/.
    cp submit $THEDIR/.
    cp $INPUT $THEDIR/.
    NJOBS=$(cat $INPUT | wc -l)

    # Make output directories
    cd $THEDIR
    for i in $(seq 0 $NJOBS); do
        mkdir -p job$(printf "%03d" $i);
    done;

    echo condor_submit submit THEDIR=$PWD NJOBS=$NJOBS
    condor_submit submit THEDIR=$PWD NJOBS=$NJOBS
    cd -
    echo -e ${GREEN} Submitted. ${NC};
    echo -e ${GREEN} Done. ${NC};

else
      echo -e ${GREEN} "Error: \$TestArea is NOT empty -- please submit with a fresh terminal session." ${NC};
fi

