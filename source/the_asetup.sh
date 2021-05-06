#
# usage: source the_asetup.sh (from the source directory)
#

#asetup AnalysisBase,21.2.56,here
asetup Athena,master,2021-04-26T2101,here

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
