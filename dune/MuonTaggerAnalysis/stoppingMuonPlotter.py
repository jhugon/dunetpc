#!/usr/bin/env python

"""
root [2] _file0.cd("muontaggertreemaker")
(Bool_t)1
root [3] _file0.ls()
TFile**     MuonTaggerTree.root 
 TFile*     MuonTaggerTree.root 
  TDirectoryFile*       muontaggertreemaker muontaggertreemaker (MuonTaggerTreeMaker) folder
   KEY: TTree   tree;1  tree
   KEY: TH1F    trajectoryX;1   
   KEY: TH1F    trajectoryY;1   
   KEY: TH1F    trajectoryZ;1   
  KEY: TDirectoryFile   muontaggertreemaker;1   muontaggertreemaker (MuonTaggerTreeMaker) folder
root [4] tree.Print()
******************************************************************************
*Tree    :tree      : tree                                                   *
*        :          : Tree compression factor =   1.52                       *
******************************************************************************
*Br    0 :event     : event/i                                                *
*Br    1 :subrun    : subrun/i                                               *
*Br    2 :run       : run/i                                                  *
*Br    3 :pdg       : pdg/I                                                  *
*Br    4 :xb        : xb/F                                                   *
*Br    5 :yb        : yb/F                                                   *
*Br    6 :zb        : zb/F                                                   *
*Br    7 :tb        : tb/F                                                   *
*Br    8 :xe        : xe/F                                                   *
*Br    9 :ye        : ye/F                                                   *
*Br   10 :ze        : ze/F                                                   *
*Br   11 :te        : te/F                                                   *
*Br   12 :pxb       : pxb/F                                                  *
*Br   13 :pyb       : pyb/F                                                  *
*Br   14 :pzb       : pzb/F                                                  *
*Br   15 :pEb       : pEb/F                                                  *
*Br   16 :pxe       : pxe/F                                                  *
*Br   17 :pye       : pye/F                                                  *
*Br   18 :pze       : pze/F                                                  *
*Br   19 :pEe       : pEe/F                                                  *
*Br   20 :pb        : pb/F                                                   *
*Br   21 :pe        : pe/F                                                   *
*Br   22 :thetab    : thetab/F                                               *
*Br   23 :costhetab : costhetab/F                                            *
*Br   24 :phib      : phib/F                                                 *
*Br   25 :thetazenithb : thetazenithb/F                                      *
*Br   26 :costhetazenithb : costhetazenithb/F                                *
*Br   27 :phizenithb : phizenithb/F                                          *
*Br   28 :inTPCe    : inTPCe/O                                               *
*Br   29 :inWideTPCe : inWideTPCe/O                                          *
*Br   30 :rangeInWideTPC : rangeInWideTPC/F                                  *
*Br   31 :numberTrajectoryPoints : numberTrajectoryPoints/I                  *
*Br   32 :trajx     : vector<float>                                          *
*Br   33 :trajy     : vector<float>                                          *
*Br   34 :trajz     : vector<float>                                          *
*Br   35 :trajt     : vector<float>                                          *
*Br   36 :trajp     : vector<float>                                          *
*Br   37 :trajE     : vector<float>                                          *
*Br   38 :trajdEdx  : vector<float>                                          *
*Br   39 :trajInTPC : vector<bool>                                           *
*Br   40 :trajInWideTPC : vector<bool>                                       *
*Br   41 :trajDistToLine : vector<float>                                     *
*Br   42 :hitsFrontDet : hitsFrontDet/O                                      *
*Br   43 :hitsBackDet : hitsBackDet/O                                        *
*Br   44 :frontDetHitX : frontDetHitX/F                                      *
*Br   45 :frontDetHitY : frontDetHitY/F                                      *
*Br   46 :frontDetHitZ : frontDetHitZ/F                                      *
*Br   47 :frontDetHitT : frontDetHitT/F                                      *
*Br   48 :backDetHitX : backDetHitX/F                                        *
*Br   49 :backDetHitY : backDetHitY/F                                        *
*Br   50 :backDetHitZ : backDetHitZ/F                                        *
*Br   51 :backDetHitT : backDetHitT/F                                        *

"""

import random
import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

def plotVariable2D(tree,canvas,variable,nBinsX,xMin,xMax,nBinsY,yMin,yMax,xlabel,ylabel,saveName,cuts="",drawopt="COLZ",logx=False,logy=False,caption="",captionleft1="",captionleft2="",captionleft3="",captionright1="",captionright2="",captionright3="",preliminaryString=""):
  """
  in variable, first part is y axis, second is x axis
  """
  setupCOLZFrame(canvas)
  if logx:
    canvas.SetLogx()
  else:
    canvas.SetLogx(False)
  if logy:
    canvas.SetLogy()
  else:
    canvas.SetLogy(False)
  binningString = "{0:d},{1:f},{2:f},{3:f},{4:f},{5:f}".format(nBinsX,xMin,xMax,nBinsY,yMin,yMax)
  name = "hist"+str(random.getrandbits(36))
  tree.Draw(variable+" >> "+name+"("+binningString+")",cuts,drawopt)
  hist = root.gPad.GetPrimitive(name)
  hist.UseCurrentStyle()
  hist.SetTitle("")
  setHistTitles(hist,xlabel,ylabel)
  drawStandardCaptions(canvas,caption,captionleft1,captionleft2,captionleft3,captionright1,captionright2,captionright3,preliminaryString)
  canvas.RedrawAxis()
  canvas.SaveAs(saveName)
  setupCOLZFrame(canvas,reset=True)
  return hist

def estimatePerSrForVerticalAndEgt1GeV(tree,nmax=10000000000):
   canvas = root.TCanvas("c2")
 
   func = root.TF1("fitfunc","[0]*cos(x)*cos(x)",0,math.pi)
 
   cuts = "pEb>1."
   #cuts = "pEb>1. && xb > -200 && xb < 200 && zb > 100 && zb < 500"
   theta = Hist(100,0,math.pi)
   theta.Sumw2()
   theta.UseCurrentStyle()
   tree.Draw("pi-thetazenithb >> {}".format(theta.GetName()),cuts,"hist",nmax    )
   setHistTitles(theta,"#theta","Events/Sr")
   drawStandardCaptions(canvas,"E_{#mu} > 1 GeV")
   xAxis = theta.GetXaxis()
   for iBinX in range(1,xAxis.GetNbins()+1):
     xLow = xAxis.GetBinLowEdge(iBinX)
     xHigh = xAxis.GetBinUpEdge(iBinX)
     solidAngle = 2*math.pi*(-math.cos(xHigh)+math.cos(xLow))
     binContent = theta.GetBinContent(iBinX)
     theta.SetBinContent(iBinX,binContent/solidAngle)
   theta.Draw("E")
   fitResult = theta.Fit(func,"WLMSQ",'',0.05,0.8)
   canvas.SaveAs("normalizationFit.png")
 
   normalization = fitResult.Parameter(0)
   normalizationUnc = fitResult.ParError(0)
   return normalization, normalizationUnc

def getNUniqueEvents(tree,nmax=10000000000):
   events = set()
   nEntries = min(tree.GetEntries(),nmax)
   for iEntry in range(nEntries):
     tree.GetEntry(iEntry)
     uniqueid = "{}{}{}".format(tree.run,tree.subrun,tree.event)
     if not uniqueid in events:
        events.add(uniqueid)
   return len(events)

if __name__ == "__main__":
  c = root.TCanvas()
  treeName = "muontaggertreemaker/tree"

  f = root.TFile("/pnfs/dune/scratch/users/jhugon/v06_05_00/muontaggertree/muontaggertree_v4/anahist.root")
  #f = root.TFile("/pnfs/dune/scratch/users/jhugon/v06_05_00/muontaggertree/muontaggertree_v4/10431460_1/MuonTaggerTree.root")
  tree = f.Get("muontaggertreemaker/tree")
  nEntries = tree.GetEntries()
  print "tree nEntries: ", nEntries
  print estimatePerSrForVerticalAndEgt1GeV(tree)
  #nEvents = getNUniqueEvents(tree)
  nEvents = 4200
  print "tree nEvents: ", nEvents

  ################################################################

  scaleFactorPerEvent = 1. / nEvents
  scaleFactorHz = 1. / nEvents / 6.45e-3

  fileConfigs = [
    {
      "fn": "/pnfs/dune/scratch/users/jhugon/v06_05_00/muontaggertree/muontaggertree_v4/anahist.root",
      #"fn":"/pnfs/dune/scratch/users/jhugon/v06_05_00/muontaggertree/muontaggertree_v4/10431460_1/MuonTaggerTree.root",
      "name": "stoppingMuons",
    },
  ]
  histConfigs = [
    {
      "name":   "Start_x",
      "var":    "xb",
      "binning":[100,-1000,1000],
      "xtitle": "Muon Starting x [cm]",
      "ytitle": "Events/bin",
      "cuts":   "",
    },
    {
      "name":   "Start_y",
      "var":    "yb",
      "binning":[50,0,1000],
      "xtitle": "Muon Starting y [cm]",
      "ytitle": "Events/bin",
      "cuts":   "",
    },
    {
      "name":   "Start_z",
      "var":    "zb",
      "binning":[100,-200,1000],
      "xtitle": "Muon Starting z [cm]",
      "ytitle": "Events/bin",
      "cuts":   "",
    },
    {
      "name":   "Start_zVx",
      "var":    "zb:xb",
      "binning":[20,-500,500,30,-200,1000],
      "xtitle": "Muon Starting x [cm]",
      "ytitle": "Muon Starting z [cm]",
      "cuts":   "",
    },
    {
      "name":   "Start_zVx_thetagt170",
      "var":    "zb:xb",
      "binning":[20,-500,500,30,-200,1000],
      "xtitle": "Muon Starting x [cm]",
      "ytitle": "Muon Starting z [cm]",
      "cuts":   "thetazenithb > pi*170/180",
      "caption":"#theta_{zenith} > 170 deg",
    },
    {
      "name":   "Stop_y",
      "var":    "ye",
      "binning":[32,0,608],
      "xtitle": "Muon stopping y [cm]",
      "ytitle": "Stopping #mu^{+} per y per event [m^{-1}]",
      "cuts":   "pdg== -13 && inWideTPCe && pe<0.01",
      "scaleFactor": scaleFactorPerEvent*100.,
      "normToBinWidth" : True,
      "printIntegral": True,
    },
    {
      "name":   "Stop_y_rate",
      "var":    "ye",
      "binning":[32,0,608],
      "xtitle": "Muon stopping y [cm]",
      "ytitle": "Stopping #mu^{+} rate per y [Hz m^{-1}]",
      "cuts":   "pdg== -13 && inWideTPCe && pe<0.01",
      "scaleFactor": scaleFactorHz*100.,
      "normToBinWidth" : True,
      "printIntegral": True,
    },
    {
      "name":   "Stop_y_vol",
      "var":    "ye",
      "binning":[32,0,608],
      "xtitle": "Muon stopping y [cm]",
      "ytitle": "Stopping #mu^{+} density per event [m^{-3}]",
      "cuts":   "pdg== -13 && inWideTPCe && pe<0.01",
      "scaleFactor": scaleFactorPerEvent*100./50.,
      "normToBinWidth" : True,
      "printIntegral": True,
    },
    {
      "name":   "Stop_y_rate_vol",
      "var":    "ye",
      "binning":[32,0,608],
      "xtitle": "Muon stopping y [cm]",
      "ytitle": "Stopping #mu^{+} rate density [Hz m^{-3}]",
      "cuts":   "pdg== -13 && inWideTPCe && pe<0.01",
      "scaleFactor": scaleFactorHz*100./50.,
      "normToBinWidth" : True,
      "printIntegral": True,
    },
    {
      "name":   "Stop_y_ally",
      "var":    "ye",
      "binning":[75,-500,1000],
      "xtitle": "Muon stopping y [cm]",
      "ytitle": "Stopping #mu^{+} per y per event [m^{-1}]",
      "cuts":   "pdg== -13 && pe<0.01 && xe > -359.9 && xe < 359.9 && ze > -0.5 && ze < 695.3",
      "scaleFactor": scaleFactorPerEvent*100.,
      "normToBinWidth" : True,
    },
    {
      "name":   "Stop_y_ally_rate",
      "var":    "ye",
      "binning":[75,-500,1000],
      "xtitle": "Muon stopping y [cm]",
      "ytitle": "Stopping #mu^{+} rate per y [Hz m^{-1}]",
      "cuts":   "pdg== -13 && pe<0.01 && xe > -359.9 && xe < 359.9 && ze > -0.5 && ze < 695.3",
      "scaleFactor": scaleFactorHz*100.,
      "normToBinWidth" : True,
    },
    {
      "name":   "Stop_y_ally_rate_vol",
      "var":    "ye",
      "binning":[75,-500,1000],
      "xtitle": "Muon stopping y [cm]",
      "ytitle": "Stopping #mu^{+} rate density [Hz m^{-3}]",
      "cuts":   "pdg== -13 && pe<0.01 && xe > -359.9 && xe < 359.9 && ze > -0.5 && ze < 695.3",
      "scaleFactor": scaleFactorHz*100./50.,
      "normToBinWidth" : True,
    },
    {
      "name":   "Stop_yVpb_ally",
      "var":    "ye:pb",
      "binning":[20,0.,4,30,-500,1000],
      "xtitle": "Initial Muon Momentum [GeV/c]",
      "ytitle": " #mu^{+} stopping y [cm]",
      "cuts":   "pdg== -13 && pe<0.01 && xe > -359.9 && xe < 359.9 && ze > -0.5 && ze < 695.3",
      "ztitle": "#mu^{+} / bin / event",
      "scaleFactor": scaleFactorPerEvent,
    },
    {
      "name":   "Stop_rangeVy",
      "var":    "rangeInWideTPC:ye",
      "binning":[16,0,608,70,0,700.],
      "xtitle": "#mu^{+} stopping y [cm]",
      "ytitle": "#mu^{+} range in TPC [cm]",
      "ztitle": "Stopping #mu^{+} density / range / event [m^{-4}]",
      "cuts":   "pdg== -13 && inWideTPCe && pe<0.01",
      "normToBinWidth": True,
      "scaleFactor": scaleFactorPerEvent*100./50.*100,
    },
    {
      "name":   "Stop_yVrange",
      "var":    "ye:rangeInWideTPC",
      "binning":[70,0,700.,16,0,608],
      "xtitle": "#mu^{+} range in TPC [cm]",
      "ytitle": "#mu^{+} stopping y [cm]",
      "ztitle": "Stopping #mu^{+} density / range / event [m^{-4}]",
      "cuts":   "pdg== -13 && inWideTPCe && pe<0.01",
      "normToBinWidth": True,
      "scaleFactor": scaleFactorPerEvent*100./50.*100,
    },
    {
      "name":   "pEbVrangeMup",
      "var":    "rangeInWideTPC:pEb",
      "binning":[40,0,5,40,0,700.],
      "ytitle": "#mu^{+} range in TPC [cm]",
      "xtitle": "Initial #mu^{+} Energy [cm]",
      "ztitle": "#mu^{+} / bin / event",
      "cuts":   "pdg== -13 && inWideTPCe && pe<0.01",
      "scaleFactor": scaleFactorPerEvent,
    },
    {
      "name":   "pEbVrangeMum",
      "var":    "rangeInWideTPC:pEb",
      "binning":[40,0,5,40,0,700.],
      "ytitle": "#mu^{-} range in TPC [cm]",
      "xtitle": "Initial #mu^{-} Energy [cm]",
      "ztitle": "#mu^{-} / bin / event",
      "cuts":   "pdg== 13 && inWideTPCe && pe<0.01",
      "scaleFactor": scaleFactorPerEvent,
    },
    {
      "name":   "tb",
      "var":    "tb*1.0e-6",
      "binning":[1000,-4,4],
      "xtitle": "Muon creation time [ms]",
      "ytitle": "Muons/bin/event",
      "cuts":   "",
      "scaleFactor": scaleFactorPerEvent,
    },
    {
      "name":   "tb_early",
      "var":    "tb*1.0e-6",
      "binning":[1000,-4,-2],
      "xtitle": "Muon creation time [ms]",
      "ytitle": "Muons/bin/event",
      "cuts":   "",
      "scaleFactor": scaleFactorPerEvent,
    },
    {
      "name":   "tb_late",
      "var":    "tb*1.0e-6",
      "binning":[1000,2,4],
      "xtitle": "Muon creation time [ms]",
      "ytitle": "Muons/bin/event",
      "cuts":   "",
      "scaleFactor": scaleFactorPerEvent,
    },
    {
      "name":   "te",
      "var":    "te*1.0e-6",
      "binning":[1000,-4,4],
      "xtitle": "Muon end time [ms]",
      "ytitle": "Muons/bin/event",
      "cuts":   "",
      "scaleFactor": scaleFactorPerEvent,
    },
  ]

  plotOneHistOnePlot(fileConfigs,histConfigs,c,treeName)

  histConfigs =  [
    {
      "name":   "Stop_y_rate_vol",
      "var":    "ye",
      "title": "Range > 0",
      "binning":[32,0,608],
      "xtitle": "Muon stopping y [cm]",
      "ytitle": "Stopping #mu^{+} rate density [Hz m^{-3}]",
      "cuts":   "pdg== -13 && inWideTPCe && pe<0.01",
      "scaleFactor": scaleFactorHz*100./50.,
      "normToBinWidth" : True,
      "printIntegral": True,
    },
    {
      "name":   "Stop_y_rate_vol",
      "var":    "ye",
      "title": "Range > 100 cm",
      "binning":[32,0,608],
      "xtitle": "Muon stopping y [cm]",
      "ytitle": "Stopping #mu^{+} rate density [Hz m^{-3}]",
      "cuts":   "pdg== -13 && inWideTPCe && pe<0.01 && rangeInWideTPC > 100.",
      "scaleFactor": scaleFactorHz*100./50.,
      "normToBinWidth" : True,
      "printIntegral": True,
      "color": root.kRed,
    },
    {
      "name":   "Stop_y_rate_vol",
      "var":    "ye",
      "title": "Range > 200 cm",
      "binning":[32,0,608],
      "xtitle": "Muon stopping y [cm]",
      "ytitle": "Stopping #mu^{+} rate density [Hz m^{-3}]",
      "cuts":   "pdg== -13 && inWideTPCe && pe<0.01 && rangeInWideTPC > 200.",
      "scaleFactor": scaleFactorHz*100./50.,
      "normToBinWidth" : True,
      "printIntegral": True,
      "color": root.kBlue,
    },
  ]
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,treeName,outPrefix="forRange_")

#  #tree.Scan("xb:yb:zb:180-thetazenithb*180/pi")
#
#  f2 = root.TFile("/scratch/dune/jhugon/mergentuple_51975_13681/anahist.root")
#  tree2 = f2.Get("muontaggertreemaker/tree")
#  trajXY = f2.Get("muontaggertreemaker/trajectoryXY")
#  trajZY = f2.Get("muontaggertreemaker/trajectoryZY")
#  trajXZ = f2.Get("muontaggertreemaker/trajectoryXZ")
#  setupCOLZFrame(c)
#  trajXY.UseCurrentStyle()
#  trajZY.UseCurrentStyle()
#  trajXZ.UseCurrentStyle()
#  trajXY.GetXaxis().SetRangeUser(-500,500)
#  trajXY.GetYaxis().SetRangeUser(-500,1000)
#  trajXZ.GetXaxis().SetRangeUser(-500,500)
#  trajXZ.GetYaxis().SetRangeUser(-200,1000)
#  trajZY.GetXaxis().SetRangeUser(-200,1000)
#  trajZY.GetYaxis().SetRangeUser(-500,1000)
#  setHistTitles(trajXY,"Trajectory point x [cm]","Trajectory point y [cm]")
#  setHistTitles(trajZY,"Trajectory point z [cm]","Trajectory point y [cm]")
#  setHistTitles(trajXZ,"Trajectory point x [cm]","Trajectory point z [cm]")
#  trajXY.Draw("colz")
#  c.SaveAs("trajXY.png")
#  trajZY.Draw("colz")
#  c.SaveAs("trajZY.png")
#  trajXZ.Draw("colz")
#  c.SaveAs("trajXZ.png")
#
#  plotVariable2D(tree2,c,"trajy:trajx",100,-500,500,150,-500,1000,"Trajectory point x [cm]","Trajectory point y [cm]","trajXY_tree.png",cuts="")
#  plotVariable2D(tree2,c,"trajy:trajz",120,-200,1000,150,-500,1000,"Trajectory point x [cm]","Trajectory point y [cm]","trajZY_tree.png",cuts="")
#  plotVariable2D(tree2,c,"trajy:trajx",100,-500,500,100,-500,1000,"Trajectory point x [cm]","Trajectory point y [cm]","trajXY_cuts1.png",cuts="thetazenithb < pi*150/180",caption="#theta_{zenith} < 150 deg")
#  #plotVariable2D(tree2,c,"trajy:trajx",100,-500,500,100,-500,1000,"Trajectory point x [cm]","Trajectory point y [cm]","trajXY_cuts2.png",cuts="xb < 200 & xb > 0 && zb < 200 && zb > 0",caption="Muon Starting 0<x<200 cm and 0<z<200cm")
#  #plotVariable2D(tree2,c,"trajy:trajx",100,-500,500,100,-500,1000,"Trajectory point x [cm]","Trajectory point y [cm]","trajXY_cuts3.png",cuts="!(xb < 200 & xb > 0 && zb < 200 && zb > 0)",caption="Muon Not Starting in 0<x<200 cm and 0<z<200cm")
#  #plotVariable2D(tree2,c,"trajy:trajx",100,-500,500,100,-500,1000,"Trajectory point x [cm]","Trajectory point y [cm]","trajXY_cuts4.png",cuts="inWideTPCe && pe<0.01 ",caption="Stopping Muons in TPC")
#
