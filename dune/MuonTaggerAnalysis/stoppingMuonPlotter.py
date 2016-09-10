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
*        :          : Tree compression factor =   1.28                       *
******************************************************************************
*Br    0 :xb        : xb/F                                                   *
*Br    1 :yb        : yb/F                                                   *
*Br    2 :zb        : zb/F                                                   *
*Br    3 :tb        : tb/F                                                   *
*Br    4 :xe        : xe/F                                                   *
*Br    5 :ye        : ye/F                                                   *
*Br    6 :ze        : ze/F                                                   *
*Br    7 :te        : te/F                                                   *
*Br    8 :pxb       : pxb/F                                                  *
*Br    9 :pyb       : pyb/F                                                  *
*Br   10 :pzb       : pzb/F                                                  *
*Br   11 :pEb       : pEb/F                                                  *
*Br   12 :pxe       : pxe/F                                                  *
*Br   13 :pye       : pye/F                                                  *
*Br   14 :pze       : pze/F                                                  *
*Br   15 :pEe       : pEe/F                                                  *
*Br   16 :pb        : pb/F                                                   *
*Br   17 :pe        : pe/F                                                   *
*Br   18 :thetab    : thetab/F                                               *
*Br   19 :costhetab : costhetab/F                                            *
*Br   20 :phib      : phib/F                                                 *
*Br   21 :thetazenithb : thetazenithb/F                                      *
*Br   22 :costhetazenithb : costhetazenithb/F                                *
*Br   23 :phizenithb : phizenithb/F                                          *
*Br   24 :inTPCe    : inTPCe/O                                               *
*Br   25 :inWideTPCe : inWideTPCe/O                                          *
*Br   26 :numberTrajectoryPoints : numberTrajectoryPoints/I                  *
*Br   27 :hitsFrontDet : hitsFrontDet/O                                      *
*Br   28 :hitsBackDet : hitsBackDet/O                                        *

"""

import random
import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

def plotVariable1D(tree,canvas,variable,nBinsX,xMin,xMax,xlabel,ylabel,saveName,cuts="",drawopt="",logx=False,logy=False,caption="",captionleft1="",captionleft2="",captionleft3="",captionright1="",captionright2="",captionright3="",preliminaryString="",scaleFactor=1.):
  if logx:
    canvas.SetLogx()
  else:
    canvas.SetLogx(False)
  if logy:
    canvas.SetLogy()
  else:
    canvas.SetLogy(False)
  binningString = "{0:d},{1:f},{2:f}".format(nBinsX,xMin,xMax)
  name = "hist"+str(random.getrandbits(36))
  tree.Draw(variable+" >> "+name+"("+binningString+")",cuts,drawopt)
  hist = root.gPad.GetPrimitive(name)
  hist.Scale(scaleFactor)
  hist.UseCurrentStyle()
  hist.SetTitle("")
  setHistTitles(hist,xlabel,ylabel)
  drawStandardCaptions(canvas,caption,captionleft1,captionleft2,captionleft3,captionright1,captionright2,captionright3,preliminaryString)
  canvas.SaveAs(saveName)
  #canvas.SaveAs(saveName+".C")
  #canvas.SaveAs(saveName+".root")
  #outfile = root.TFile(saveName+".root","RECREATE")
  #outfile.cd()
  #hist.Write()
  #outfile.Close()
  return hist

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

if __name__ == "__main__":
  c = root.TCanvas()
  treeName = "muontaggertreemaker/tree"
  scaleFactor = 1.#/nEvents*8.*166.

  f = root.TFile("/pnfs/dune/persistent/users/jhugon/v06_05_00/g4/muontaggertree_v1/anahist.root")
  tree = f.Get("muontaggertreemaker/tree")
  nEvents = tree.GetEntries()
  print "tree nEntries: ", nEvents
  print estimatePerSrForVerticalAndEgt1GeV(tree)

  ################################################################

  fileConfigs = [
    {
      "fn": "/pnfs/dune/persistent/users/jhugon/v06_05_00/g4/muontaggertree_v1/anahist.root",
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
      "ytitle": "Stopping muon rate density [Hz m^{-3}]",
      "cuts":   "inWideTPCe && pe<0.01",
      "scaleFactor": scaleFactor,
      "printIntegral": True,
    },
    {
      "name":   "Stop_y_ally",
      "var":    "ye",
      "binning":[75,-500,1000],
      "xtitle": "Muon stopping y [cm]",
      "ytitle": "Stopping muon rate density [Hz m^{-3}]",
      "cuts":   "pe<0.01",
      "scaleFactor": scaleFactor,
    },
    {
      "name":   "Stop_yVpb_ally",
      "var":    "ye:pb",
      "binning":[20,0.,4,30,-500,1000],
      "xtitle": "Initial Muon Momentum [GeV/c]",
      "ytitle": "Muon stopping y [cm]",
      "cuts":   "pe<0.01",
    },
  ]

  plotOneHistOnePlot(fileConfigs,histConfigs,c,treeName)

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
