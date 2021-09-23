
THEDIR=$1 # e.g. outDir

# Create a directory "ntuple" where the flat ntuple will be created
mkdir -p $THEDIR/ntuple;
cd $THEDIR/ntuple;

echo 'In directory' `pwd`
echo 'Running runmacro.py with conversionTuningTRT skimmer.'

# Run the macro in this directory
ln -s ../../conversionTuningTRT.h .
python ../../../genericUtils/macros/runmacro.py --xAODInit --macro conversionTuningTRT.h --bkgs ../job%/Nightly%pool.root

# Hadd everything together
hadd -f Nightly_Ntuple_gamma.pool.root *nano.root

cd -;

echo 'Complete.'
