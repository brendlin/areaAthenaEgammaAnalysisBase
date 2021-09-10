#
# usage: source the_asetup.sh (from the source directory)
#

#asetup AnalysisBase,21.2.56,here
MY_RELEASE=2021-04-13T2101

if [ -z "$BATCH_SYSTEM" ]; then
    # BATCH_SYSTEM variable not set -- we are on an interactive machine
    asetup Athena,master,$MY_RELEASE,here
else
    # We are on the batch node, which means we need an additional "64" argument
    asetup Athena,master,$MY_RELEASE,64,here
fi


doExtras () {
    export MYCMAKE_TMP=(${CMAKE_PREFIX_PATH//:/ })
    export CMAKE_ATLAS=$MYCMAKE_TMP # not sure why this is necessary.
    if [ -a $TestArea/../build/$Athena_PLATFORM/setup.sh ]
    then
        echo source $TestArea/../build/$Athena_PLATFORM/setup.sh
        source $TestArea/../build/$Athena_PLATFORM/setup.sh
    fi
    export me=`pwd`
}

mymake () {
    echo doing Athena-aware make
    sleep 1
    cd $TestArea/../build
    cmake -DATLAS_PACKAGE_FILTER_FILE=../source/package_filters.txt cmake ../source/athena/Projects/WorkDir/
}

mybuild () {
    echo doing Athena-aware make
    sleep 1
    cd $TestArea/../build
    cmake --build .
    if [[ -z "$WorkDir_SET_UP" ]] ; then 
        echo source $TestArea/../build/$Athena_PLATFORM/setup.sh
        source $TestArea/../build/$Athena_PLATFORM/setup.sh
    fi
}

doExtras
