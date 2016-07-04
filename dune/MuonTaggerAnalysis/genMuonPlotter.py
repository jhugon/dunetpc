#!/usr/bin/env python

import random
import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

f = root.TFile("MuonTaggerTree.root")

tree = f.Get("muontaggertreemaker/tree")
#tree.Print()

c = root.TCanvas()

def plotVariable(tree,canvas,variable,nBins,xMin,xMax,xlabel,ylabel,saveName,histConfigs,drawopt="SAME",logx=False,logy=False):
  if logx:
    c.SetLogx()
  else:
    c.SetLogx(False)
  if logy:
    c.SetLogy()
  else:
    c.SetLogy(False)
  hists = []
  binningString = "{0:d},{1:f},{2:f}".format(nBins,xMin,xMax)
  for histConfig in histConfigs:
    name = "hist"+str(random.getrandbits(36))
    tree.Draw(variable+" >> "+name+"("+binningString+")",histConfig['cuts'])
    tmpHist = root.gPad.GetPrimitive(name)
    tmpHist.SetLineColor(histConfig['color'])
    tmpHist.SetTitle("")
    tmpHist.SetLineWidth(1)
    tmpHist.SetMarkerSize(1.2)
    hists.append(tmpHist)
  ymax = 1.5*max([getHistMax(x) for x in hists])
  ymin = 0.
  if logy:
    ymin = 0.1
  axisHist = root.TH2F("axisHist1"+str(random.getrandbits(36)),"",1,xMin,xMax,1,ymin,ymax)
  hists.append(axisHist)
  setHistTitles(axisHist,xlabel,ylabel)
  axisHist.Draw()
  for hist in hists:
    hist.Draw(drawopt)
  canvas.SaveAs(saveName)
  return hists

hists = plotVariable(tree,c,"thetazenithb/TMath::Pi()*180.",50,0.,180.,"#theta_{zenith} [#circ]","Events/bin","thetazenithb.png",[
  #{
  #  "title":"p #leq 1 GeV/c",
  #  "cuts":"pb <= 1.",
  #  "color":root.kBlack,
  #},
  #{
  #  "title":"1 GeV/c < p < 3 GeV/c",
  #  "cuts":"pb > 1. && pb < 3.",
  #  "color":root.kRed,
  #},
  #{
  #  "title":"p \geq 3 GeV/c",
  #  "cuts":"pb >= 3.",
  #  "color":root.kGreen,
  #},
  {
    "title":"All",
    "cuts":"",
    "color":root.kBlack,
  },
  {
    "title":"Hit Front Det",
    "cuts":"hitsFrontDet",
    "color":root.kGreen,
  },
  {
    "title":"Hit Back Det",
    "cuts":"hitsBackDet",
    "color":root.kRed,
  },
  {
    "title":"Hit Both Det",
    "cuts":"hitsFrontDet && hitsBackDet",
    "color":root.kBlue,
  },
])

hists = plotVariable(tree,c,"thetab/TMath::Pi()*180.",50,0.,180.,"#theta_{z} [#circ]","Events/bin","thetab.png",[
  #{
  #  "title":"p #leq 1 GeV/c",
  #  "cuts":"pb <= 1.",
  #  "color":root.kBlack,
  #},
  #{
  #  "title":"1 GeV/c < p < 3 GeV/c",
  #  "cuts":"pb > 1. && pb < 3.",
  #  "color":root.kRed,
  #},
  #{
  #  "title":"p \geq 3 GeV/c",
  #  "cuts":"pb >= 3.",
  #  "color":root.kGreen,
  #},
  {
    "title":"All",
    "cuts":"",
    "color":root.kBlack,
  },
  {
    "title":"Hit Front Det",
    "cuts":"hitsFrontDet",
    "color":root.kGreen,
  },
  {
    "title":"Hit Back Det",
    "cuts":"hitsBackDet",
    "color":root.kRed,
  },
  {
    "title":"Hit Both Det",
    "cuts":"hitsFrontDet && hitsBackDet",
    "color":root.kBlue,
  },
])

hists = plotVariable(tree,c,"phizenithb/TMath::Pi()*180.",50,-180.,180,"#phi_{Zenith} [#circ] ","Events/bin","phizenithb.png",[
  {
    "title":"All",
    "cuts":"",
    "color":root.kBlack,
  },
  {
    "title":"Hit Front Det",
    "cuts":"hitsFrontDet",
    "color":root.kGreen,
  },
  {
    "title":"Hit Back Det",
    "cuts":"hitsBackDet",
    "color":root.kRed,
  },
  {
    "title":"Hit Both Det",
    "cuts":"hitsFrontDet && hitsBackDet",
    "color":root.kBlue,
  },
])

hists = plotVariable(tree,c,"phib/TMath::Pi()*180.",50,-180,180,"#phi_{z} [#circ]","Events/bin","phib.png",[
  {
    "title":"All",
    "cuts":"",
    "color":root.kBlack,
  },
  {
    "title":"Hit Front Det",
    "cuts":"hitsFrontDet",
    "color":root.kGreen,
  },
  {
    "title":"Hit Back Det",
    "cuts":"hitsBackDet",
    "color":root.kRed,
  },
  {
    "title":"Hit Both Det",
    "cuts":"hitsFrontDet && hitsBackDet",
    "color":root.kBlue,
  },
])

hists = plotVariable(tree,c,"pb",50,0.,100,"p [GeV/c]","Events/bin","momentum.png",[
  {
    "title":"All",
    "cuts":"",
    "color":root.kBlack,
  },
  {
    "title":"Hit Front Det",
    "cuts":"hitsFrontDet",
    "color":root.kGreen,
  },
  {
    "title":"Hit Back Det",
    "cuts":"hitsBackDet",
    "color":root.kRed,
  },
  {
    "title":"Hit Both Det",
    "cuts":"hitsFrontDet && hitsBackDet",
    "color":root.kBlue,
  },
],logy=True)
