
# If you have e.g. a different tier3 username than your gitlab username, put the following
# two lines in your ~/.gitconfig
# [atlas]
# 	user = brendlin

GIT_USER=`git config --global atlas.user`

#
# - Check out athena in the source directory (sparse checkout)
# - Add egamma packages
# - Add egammaOrigin
# - Fetch upstream
#
if [[ ! -d source/athena ]]; then
    echo checking out athena
    mkdir -p source/athena
    cd source/athena
    git atlas init-workdir -b 21.2 ssh://git@gitlab.cern.ch:7999/${GIT_USER}/athena.git . \
        -p ElectronPhotonShowerShapeFudgeTool ElectronPhotonSelectorTools
    # git atlas addpkg PhotonEfficiencyCorrection
    git remote add egammaOrigin ssh://git@gitlab.cern.ch:7999/ATLAS-EGamma/athena.git
    git fetch upstream
    cd -
fi
