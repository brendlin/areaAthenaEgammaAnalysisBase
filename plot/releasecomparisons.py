#!/usr/bin/env python

##
## This macro offers a way to compare different releases.
## To use it, make a config file and define inside a list called "cutcomparisons", e.g. to compare
## "CutSet1" (comprised of cut1a, cut1b, cut1c) and "CutSet2" (comprised of cut2a, cut2b, cut2c) do:
## cutcomparisons = [ ['CutSet1',['cut1a','cut1b','cut1c']], ['CutSet2',['cut2a','cut2b','cut2c']] ]
##

import ROOT,sys,os

# This only works with python2
sys.path.insert(0, "%s/../genericUtils/python"%(os.path.dirname(os.path.abspath(__file__))))
import TAxisFunctions as taxisfunc
import PyAnalysisPlotting as anaplot
import PlotFunctions as plotfunc

# import TAxisFunctions as taxisfunc
# import PyAnalysisPlotting as anaplot
# import PlotFunctions as plotfunc
import copy

def DrawHistosReleaseComparison(variable,options,ref_hists=[],test_hists=[],name='') :
    #
    # Clean up name
    #
    canname = anaplot.CleanUpName(variable)

    #
    # stack, before adding SUSY histograms
    #
    if not options.ratio :
        can = ROOT.TCanvas(canname,canname,800,600)
    else :
        can = plotfunc.RatioCanvas(canname,canname,500,500)

    if ref_hists :
        for i,h in enumerate(ref_hists) :

            if options.efficiency and i == 0 :
                continue

            if options.efficiency :
                h.Divide(ref_hists[0])

            plotfunc.AddHistogram(can,h,'pE1') # pE1

    if test_hists :
        for i,h in enumerate(test_hists) :

            if options.efficiency and i == 0 :
                continue

            if options.efficiency :
                h.Divide(test_hists[0])

            if options.ratio :
                plotfunc.AddRatio(can,h,ref_hists[i])
            else :
                plotfunc.AddHistogram(can,h)

    if not options.ratio :
        plotfunc.FormatCanvasAxes800600(can)
    else :
        plotfunc.FormatCanvasAxes(can)

    if options.log :
        if options.ratio :
            if taxisfunc.MinimumForLog(can.GetPrimitive('pad_top')) > 0 :
                can.GetPrimitive('pad_top').SetLogy()
        else :
            if taxisfunc.MinimumForLog(can) > 0 :
                can.SetLogy()

    if options.ratio :
        plotfunc.MakeLegend(can,0.53,0.65,0.92,0.90,totalentries=5,ncolumns=1,skip=['remove me'])
    else :
        plotfunc.MakeLegend(can,0.53,0.75,0.94,0.92,totalentries=4,ncolumns=1,skip=['remove me'],
                            textsize=27)

    ylabel = 'entries (normalized)' if options.normalize else 'entries'
    if options.efficiency :
        ylabel = 'efficiency'
    plotfunc.SetAxisLabels(can,options.xlabel.get(variable),ylabel)
    plotfunc.AutoFixAxes(can)

    if not options.log :
        if can.GetPrimitive('pad_top') :
            plotfunc.AutoFixYaxis(can.GetPrimitive('pad_top'),minzero=True)
        else :
            plotfunc.AutoFixYaxis(can,minzero=True)

    return can

#-------------------------------------------------------------------------
def main(options,args) :

    mystyle = plotfunc.SetupStyle()

    files_test,trees_test,keys_test = anaplot.GetTreesFromFiles(options.test     ,treename=options.treename,xAODInit=options.xAODInit)
    files_ref ,trees_ref ,keys_ref  = anaplot.GetTreesFromFiles(options.reference,treename=options.treename,xAODInit=options.xAODInit)

    # A bit of a hack to get the test and ref labels properly in the code:
    options.labels = dict()
    for k in keys_test :
        options.labels[k] = options.test_label
    for k in keys_ref :
        options.labels[k] = options.ref_label

    cans = []

    # get the histograms from the files
    for v in options.variables :
        ref_hists = []
        test_hists = []

        for cname in options.cutcomparisons.keys() :
            cutcomp = options.cutcomparisons[cname]
            inputname = '%s_%s'%(v,cname)

            weight = options.weight

            if type(weight) == type(dict()) :
                weight = weight[cname]

            # Weights/Cuts for the reference
            if ''.join(options.cuts+cutcomp) :
                weight_ref = (weight+'*(%s)'%(' && '.join(options.cuts+cutcomp).lstrip('& ').rstrip('& '))).lstrip('*')
            else :
                weight_ref = weight

            # Weights/Cuts for the test (including additional test cuts)
            weight_test = weight # weight value (and cuts) applied to test
            if ''.join(options.cuts+cutcomp+options.additional_test_cuts) :
                weight_test = (weight+'*(%s)'%(' && '.join(options.cuts+cutcomp+options.additional_test_cuts).lstrip('& ').rstrip('& '))).lstrip('*')
            else :
                weight_test = weight

            # Make the plots
            if options.test :
                test_hists_tmp = anaplot.GetVariableHistsFromTrees(trees_test,keys_test,v,weight_test,options,files=files_test,inputname=inputname)

                for d in test_hists_tmp :
                    d.SetTitle(cname)
                    test_hists.append(d)

            if options.reference :
                ref_hists_tmp = anaplot.GetVariableHistsFromTrees(trees_ref,keys_ref,v,weight_ref,options,files=files_ref,inputname=inputname)
                anaplot.SetLegendLabels(ref_hists_tmp,options)

                for s in ref_hists_tmp :
                    s.SetTitle(('%s, %s'%(s.GetTitle(),cname)).lstrip(' ,'))
                    ref_hists.append(s)

        if options.normalize :
            for hist in test_hists + ref_hists :
                if not hist : continue
                hist.Scale(1/float(hist.Integral()))

        # Hack to turn off labels (since they are already set) before another round of
        # PrepareSignalHistos.
        tmp_options = copy.copy(options)
        tmp_options.labels = {}
        anaplot.PrepareSignalHistos(ref_hists+test_hists,tmp_options)
        for h in ref_hists :
            h.SetMarkerStyle(24)
            h.SetTitle('remove')

        ## Special canvas:
        cans.append(DrawHistosReleaseComparison(v,options,ref_hists=ref_hists,test_hists=test_hists))

    if options.afterburner :
        for can in cans :
            options.afterburner(can)

    anaplot.UpdateCanvases(cans,options)

    if not options.batch :
        import code
        code.interact(banner='Pausing... Press Contol-D to exit.',local=locals())

    anaplot.doSaving(options,cans)

    print('done.')
    return

if __name__ == '__main__':

    p = anaplot.TreePlottingOptParser()

    p.p.remove_option('--bkgs')
    p.p.add_option('--reference',type='string',default='',dest='reference',help='reference release')
    p.p.add_option('--test'     ,type='string',default='',dest='test'     ,help='test release')
    p.p.add_option('--efficiency',action='store_true',default=False,dest='efficiency',help='Plot efficiencies')

    options,args = p.parse_args()

    if options.ratio :
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('%% Taking the ratio of TEST divided by REF')
        print('%% and plotting in the bottom pad.')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    if options.efficiency :
        print ('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print ('%% Important! Plotting the efficiency with the FIRST entry in cutcomparisons')
        print ('%%  as the denominator!')
        print ('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    if hasattr(options.usermodule,'cutcomparisons') :
        options.cutcomparisons = options.usermodule.cutcomparisons

    if hasattr(options.usermodule,'test_label') :
        options.test_label = options.usermodule.test_label

    if hasattr(options.usermodule,'ref_label') :
        options.ref_label = options.usermodule.ref_label

    options.additional_test_cuts = []
    if hasattr(options.usermodule,'additional_test_cuts') :
        options.additional_test_cuts = options.usermodule.additional_test_cuts

    if not options.variables :
        print ('Error! Please specify a variable!')
        sys.exit()

    main(options,args)
