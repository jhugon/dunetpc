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

hists = plotVariable(tree,c,"thetazenithb/TMath::Pi()",50,-0.,1.,"#theta_{zenith}/#pi","Events/bin","thetazenithb.png",[
  #{
  #  "title":"p #leq 1 GeV/c",
  #  "cuts":"pb <= 1.",
  #  "color":root.kBlue,
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
    "title":"",
    "cuts":"",
    "color":root.kBlue,
  },
])

hists = plotVariable(tree,c,"thetab/TMath::Pi()",50,-0.,1.,"#theta_{z}/#pi","Events/bin","thetab.png",[
  {
    "title":"p #leq 1 GeV/c",
    "cuts":"pb <= 1.",
    "color":root.kBlue,
  },
  {
    "title":"1 GeV/c < p < 3 GeV/c",
    "cuts":"pb > 1. && pb < 3.",
    "color":root.kRed,
  },
  {
    "title":"p \geq 3 GeV/c",
    "cuts":"pb >= 3.",
    "color":root.kGreen,
  },
])

hists = plotVariable(tree,c,"phizenithb/TMath::Pi()",50,-1.,1,"#phi_{Zenith}/#pi ","Events/bin","phizenithb.png",[
  {
    "title":"p #leq 1 GeV/c",
    "cuts":"pb <= 1.",
    "color":root.kBlue,
  },
  {
    "title":"1 GeV/c < p < 3 GeV/c",
    "cuts":"pb > 1. && pb < 3.",
    "color":root.kRed,
  },
  {
    "title":"p \geq 3 GeV/c",
    "cuts":"pb >= 3.",
    "color":root.kGreen,
  },
])

hists = plotVariable(tree,c,"phib/TMath::Pi()",50,-1.,1,"#phi_{z}/#pi","Events/bin","phib.png",[
  {
    "title":"p #leq 1 GeV/c",
    "cuts":"pb <= 1.",
    "color":root.kBlue,
  },
  {
    "title":"1 GeV/c < p < 3 GeV/c",
    "cuts":"pb > 1. && pb < 3.",
    "color":root.kRed,
  },
  {
    "title":"p \geq 3 GeV/c",
    "cuts":"pb >= 3.",
    "color":root.kGreen,
  },
])

hists = plotVariable(tree,c,"pb",50,0.,100,"p [GeV/c]","Events/bin","momentum.png",[
  {
    "title":"",
    "cuts":"",
    "color":root.kBlue,
  },
],logy=True)
