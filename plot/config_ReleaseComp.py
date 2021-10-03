
treename = 'CollectionTree'

test_label = 'test'
ref_label = 'ref'

variables = [
    # 'mu',
    # 'trueR',
    'abs(truthEta)',
    # 'truthPt',
    # 'recoPt',
    # 'eProbabilityHT_trans_0',
    # 'eProbabilityHT_trans_0*(trueR > 0)',
    # 'mu*(trueR > 0)',
    # 'nTRT_0*(trueR > 0)',
    # 'eProbabilityHT_trans_0*(trueR <= 0)',
    # 'mu*(trueR <= 0)',
    # 'nTRT_0*(trueR <= 0)',
    # 'abs(recoEta)',
    # 'abs(trkEta_0)',
    # 'nSi_0',
    # 'nSi_1',
    # 'eProbabilityHT_0',
    # 'eProbabilityHT_1',
    # 'max(eProbabilityHT_0,0)',
    # 'max(eProbabilityHT_1,0)',
    # 'nTRT_0',
    # 'nTRT_1',
    # 'precHitFrac_0',
    # 'precHitFrac_1',
    # 'nTRT_0 - 0.2*mu',
    # 'max(eProbabilityNN_0,0)',
    # 'max(eProbabilityNN_1,0)',
    # 'eProbabilityHT_0*(nSi_0 > 0) + eProbabilityHT_1*(nSi_1 > 0)', # Si track of Si-TRT
    # 'eProbabilityHT_0*(nSi_0 == 0) + eProbabilityHT_1*(nSi_1 == 0)', # TRT track of Si-TRT
    # 'trkPt_0/1000.',
]

# On top of what is specified in cutcomparisons, these cuts are also applied to all entries in
# the cutcomparisons dict
cuts = [
    'trueR > 0',    # all truth converted photons
    #'trueR <= 0',    # all truth unconverted photons
    'truthPt > 15.', # in GeV
    # 'recoPt > 0',                 # all reco photons
    # 'convType > 0',               # reco converted
    # 'convType == 2',              # Single TRT
    # '(nSi_0 <= 0 && nSi_1 <= 0)', # TRT-only
    # '((nSi_0 > 0 || nSi_1 > 0) && (!(nSi_0 > 0 && nSi_1 > 0)))', # Si-TRT
    # 'abs(recoEta)*1000 < 1.0',
    # 'convType == 3', # 2Si
    # 'convType == 4', # 2TRT
    # 'convType == 5', # SiTRT
    # 'abs(recoEta) < 1.2',
    # 'abs(recoEta) > 0.7',
    # 'precHitFrac_0 > 0.3',
    # '(eProbabilityHT_0 > 0.75 || nTRT_0 < 0)',
]

# Additional cuts, applied ONLY to the test sample.
additional_test_cuts = []

cuts_all_truth_conv_photons = []
cuts_reco_conv_photon = ['recoPt > 0','convType > 0']
cuts_single_si        = ['recoPt > 0','convType > 0','convType == 1']
cuts_single_trt       = ['recoPt > 0','convType > 0','convType == 2']
cuts_2si              = ['recoPt > 0','convType > 0','convType == 3']
cuts_2trt             = ['recoPt > 0','convType > 0','convType == 4']
cuts_1si_and_sitrt    = ['recoPt > 0','convType > 0','(convType == 1 || convType == 5)']
cuts_1trt_and_2trt    = ['recoPt > 0','convType > 0','(convType == 2 || convType == 4)']
cuts_sitrt            = ['recoPt > 0','convType > 0','convType == 5']

from collections import OrderedDict
cutcomparisons = OrderedDict()
cutcomparisons['all truth conv Photons' ] = []
cutcomparisons['Reco Conv Photon'] = cuts_reco_conv_photon
# cutcomparisons['Single Si'       ] = cuts_single_si
#cutcomparisons['Single TRT'      ] = cuts_single_trt
# cutcomparisons['2Si'             ] = cuts_2si
#cutcomparisons['2TRT'            ] = cuts_2trt
# cutcomparisons['1Si+SiTRT'       ] = cuts_1si_and_sitrt
cutcomparisons['1TRT+2TRT'       ] = cuts_1trt_and_2trt
# cutcomparisons['SiTRT'           ] = cuts_sitrt

# To get consistent plot colors (% is wildcard)
from ROOT import kGray,kBlack,kBlue,kRed,kGreen,kOrange,kCyan
colors = { 
    '%all truth conv Photons%':kGray,
    '%all truth Photons%':kGray,
    '%Reco Conv Photon%' :kBlack,
    '%Single Si%'        :kBlue+2,
    '%Single TRT%'       :kRed+2,
    '%2Si%'              :kGreen+2,
    '%2TRT%'             :kOrange+2,
    '%SiTRT%'            :kCyan+2,
    '%Unconv%'           :kOrange+3,
}

# Formatting the histogram ranges / x-axis labels
histformat = {
    'trueR':[1085,0,1085,'Truth Radius [mm]'],
    'mu':[45,0,90,'#mu'],
    'mu*(trueR > 0)':[17,5,90,'#mu'],
    'mu*(trueR <= 0)':[17,5,90,'#mu'],
    'eProbabilityHT_0':[20,0,1,'eProbabilityHT_0'],
    'eProbabilityHT_trans_0':[40,-0.1,1.5,'eProbabilityHT_trans_0'],
    'eProbabilityHT_trans_0*(trueR > 0)':[50,-0.1,1,'eProbabilityHT_trans_0'],
    'eProbabilityHT_trans_0*(trueR <= 0)':[50,-0.1,1,'eProbabilityHT_trans_0'],
    'eProbabilityHT_1':[20,0,1,'eProbabilityHT_1'],
    'max(eProbabilityHT_0,0)':[20,0,1,'eProbabilityHT_0'],
    'max(eProbabilityHT_1,0)':[20,0,1,'eProbabilityHT_1'],
    'max(eProbabilityNN_0,0)':[20,0,1,'eProbabilityNN_0'],
    'max(eProbabilityNN_1,0)':[20,0,1,'eProbabilityNN_1'],
    'nSi_0':[20,0,20,'nSi_0'],
    'nSi_1':[20,0,20,'nSi_1'],
    'nTRT_0':[50,-0.5,49.5,'nTRT_0'],
    'nTRT_0*(trueR > 0)':[25,0,50,'nTRT_0'],
    'nTRT_0*(trueR <= 0)':[25,0,50,'nTRT_0'],
    'nTRT_1':[50,0,50,'nTRT_1'],
    'truthPt':[2985,15,3000,'truth p_{T} [GeV]'],
    'abs(recoEta)':[100,0,2.5,'reco |#eta|'],
    'abs(truthEta)':[25,0,2.5,'truth |#eta|'],
    'abs(trkEta_0)':[50,0,2.5,'track 0 |#eta|'],
    'abs(trkEta_1)':[50,0,2.5,'track 1 |#eta|'],
    'eProbabilityHT_0*(nSi_0 > 0) + eProbabilityHT_1*(nSi_1 > 0)':[20,0,1,'eProbabilityHT Si'],
    'eProbabilityHT_0*(nSi_0 == 0) + eProbabilityHT_1*(nSi_1 == 0)':[20,0,1,'eProbabilityHT TRT'],
    'nTRT_0 - 0.2*mu':[25,0,45,'mu-corrected nTRT'],
    'precHitFrac_0':[20,0,1,'precHitFrac'],
    'precHitFrac_1':[20,0,1,'precHitFrac (trk1)'],
    'trkPt_0/1000.':[30,0,100,'track p_{T} [GeV]'],
}

# This dict gives you the opportunity to make variable bin widths, as long as they are consistent
# with the bin edges specified in "histformat"
rebin = {
    'trueR':[0, 50, 89, 123, 170, 210, 250, 299, 335, 371, 443, 514, 554, 800, 1085],
    'truthPt':[15,20,25,30,40,50,60,70,80,90,100,150,200,
               250,300,400,500,600,700,800,900,1000,2000,3000],
    #'abs(truthEta)':[0.0, 0.75, 1.2, 2.5],
    #'abs(truthEta)':[0.0, 2.5],
}

# Here you can do any last-minute manipulations of the plot
def afterburner(can) :
    import ROOT
    import PlotFunctions as plotfunc

    # Make the "reference, test" legend
    if plotfunc.GetTopPad(can) :
        file_leg = ROOT.TLegend(0.19,0.65,0.49,0.90)
    else :
        file_leg = ROOT.TLegend(0.19,0.75,0.49,0.92)
    file_leg.SetName('file_titles_%s'%(can.GetName()))
    file_leg.SetFillStyle(0)
    file_leg.SetTextSize(18 if plotfunc.GetTopPad(can) else 24)

    leghist_ref = ROOT.TH1F()
    leghist_ref.SetMarkerColor(ROOT.kGray)
    leghist_ref.SetLineColor(ROOT.kGray)
    leghist_ref.SetMarkerStyle(24)
    file_leg.AddEntry(leghist_ref,ref_label,'pe')
    leghist_test = ROOT.TH1F()
    leghist_test.SetMarkerColor(ROOT.kGray)
    leghist_test.SetLineColor(ROOT.kGray)
    leghist_test.SetMarkerStyle(20)
    file_leg.AddEntry(leghist_test,test_label,'pe')
    # For spacing
    file_leg.AddEntry(0,'','')
    file_leg.AddEntry(0,'','')
    can.cd()
    if plotfunc.GetTopPad(can) :
        plotfunc.GetTopPad(can).cd()
    file_leg.Draw()
    plotfunc.tobject_collector.append(leghist_ref)
    plotfunc.tobject_collector.append(leghist_test)
    plotfunc.tobject_collector.append(file_leg)

    return
