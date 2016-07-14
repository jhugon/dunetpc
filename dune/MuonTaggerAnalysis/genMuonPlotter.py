#!/usr/bin/env python

import random
import ROOT as root
from helpers import *
from trajectoryPlotter import plotVariable2D
root.gROOT.SetBatch(True)

f = root.TFile("MuonTaggerTree.root")

tree = f.Get("muontaggertreemaker/tree")
#tree.Print()

c = root.TCanvas()

def plotVariable(tree,canvas,variable,nBins,xMin,xMax,xlabel,ylabel,saveName,histConfigs,drawopt="SAME",logx=False,logy=False):
  if logx:
    canvas.SetLogx()
  else:
    canvas.SetLogx(False)
  if logy:
    canvas.SetLogy()
  else:
    canvas.SetLogy(False)
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

#hists = plotVariable(tree,c,"thetazenithb/TMath::Pi()*180.",50,0.,180.,"#theta_{zenith} [#circ]","Events/bin","thetazenithb.png",[
#  #{
#  #  "title":"p #leq 1 GeV/c",
#  #  "cuts":"pb <= 1.",
#  #  "color":root.kBlack,
#  #},
#  #{
#  #  "title":"1 GeV/c < p < 3 GeV/c",
#  #  "cuts":"pb > 1. && pb < 3.",
#  #  "color":root.kRed,
#  #},
#  #{
#  #  "title":"p \geq 3 GeV/c",
#  #  "cuts":"pb >= 3.",
#  #  "color":root.kGreen,
#  #},
#  {
#    "title":"All",
#    "cuts":"",
#    "color":root.kBlack,
#  },
#  {
#    "title":"Hit Front Det",
#    "cuts":"hitsFrontDet",
#    "color":root.kGreen,
#  },
#  {
#    "title":"Hit Back Det",
#    "cuts":"hitsBackDet",
#    "color":root.kRed,
#  },
#  {
#    "title":"Hit Both Det",
#    "cuts":"hitsFrontDet && hitsBackDet",
#    "color":root.kBlue,
#  },
#])
#
#hists = plotVariable(tree,c,"thetab/TMath::Pi()*180.",50,0.,180.,"#theta_{z} [#circ]","Events/bin","thetab.png",[
#  #{
#  #  "title":"p #leq 1 GeV/c",
#  #  "cuts":"pb <= 1.",
#  #  "color":root.kBlack,
#  #},
#  #{
#  #  "title":"1 GeV/c < p < 3 GeV/c",
#  #  "cuts":"pb > 1. && pb < 3.",
#  #  "color":root.kRed,
#  #},
#  #{
#  #  "title":"p \geq 3 GeV/c",
#  #  "cuts":"pb >= 3.",
#  #  "color":root.kGreen,
#  #},
#  {
#    "title":"All",
#    "cuts":"",
#    "color":root.kBlack,
#  },
#  {
#    "title":"Hit Front Det",
#    "cuts":"hitsFrontDet",
#    "color":root.kGreen,
#  },
#  {
#    "title":"Hit Back Det",
#    "cuts":"hitsBackDet",
#    "color":root.kRed,
#  },
#  {
#    "title":"Hit Both Det",
#    "cuts":"hitsFrontDet && hitsBackDet",
#    "color":root.kBlue,
#  },
#])
#
#hists = plotVariable(tree,c,"phizenithb/TMath::Pi()*180.",50,-180.,180,"#phi_{Zenith} [#circ] ","Events/bin","phizenithb.png",[
#  {
#    "title":"All",
#    "cuts":"",
#    "color":root.kBlack,
#  },
#  {
#    "title":"Hit Front Det",
#    "cuts":"hitsFrontDet",
#    "color":root.kGreen,
#  },
#  {
#    "title":"Hit Back Det",
#    "cuts":"hitsBackDet",
#    "color":root.kRed,
#  },
#  {
#    "title":"Hit Both Det",
#    "cuts":"hitsFrontDet && hitsBackDet",
#    "color":root.kBlue,
#  },
#])
#
#hists = plotVariable(tree,c,"phib/TMath::Pi()*180.",50,-180,180,"#phi_{z} [#circ]","Events/bin","phib.png",[
#  {
#    "title":"All",
#    "cuts":"",
#    "color":root.kBlack,
#  },
#  {
#    "title":"Hit Front Det",
#    "cuts":"hitsFrontDet",
#    "color":root.kGreen,
#  },
#  {
#    "title":"Hit Back Det",
#    "cuts":"hitsBackDet",
#    "color":root.kRed,
#  },
#  {
#    "title":"Hit Both Det",
#    "cuts":"hitsFrontDet && hitsBackDet",
#    "color":root.kBlue,
#  },
#])
#
#hists = plotVariable(tree,c,"pb",50,0.,100,"p [GeV/c]","Events/bin","momentum.png",[
#  {
#    "title":"All",
#    "cuts":"",
#    "color":root.kBlack,
#  },
#  {
#    "title":"Hit Front Det",
#    "cuts":"hitsFrontDet",
#    "color":root.kGreen,
#  },
#  {
#    "title":"Hit Back Det",
#    "cuts":"hitsBackDet",
#    "color":root.kRed,
#  },
#  {
#    "title":"Hit Both Det",
#    "cuts":"hitsFrontDet && hitsBackDet",
#    "color":root.kBlue,
#  },
#],logy=True)

plotVariable2D(tree,c,"xb:yb",1000,-4000.,4000.,1000,-5000,5000,"MuonProduction y [cm]","Muon Production x [cm]","xbVyb.png",cuts="")
plotVariable2D(tree,c,"xb:zb",1000,-4000.,4000.,1000,-5000,5000,"MuonProduction y [cm]","Muon Production x [cm]","zbVxb.png",cuts="")
plotVariable2D(tree,c,"yb:zb",1000,-4000.,4000.,1000,-5000,5000,"MuonProduction y [cm]","Muon Production x [cm]","zbVyb.png",cuts="")
c.Clear()
hists = plotVariable(tree,c,"xb",500,-1000.,-1000,"Muon Production x [cm]","Events/bin","xb.png",[
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
],logy=False)
hists = plotVariable(tree,c,"yb",500,-3000,3000,"Muon Production y [cm]","Events/bin","yb.png",[
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
],logy=False)
hists = plotVariable(tree,c,"zb",500,-1000,1000,"Muon Production z [cm]","Events/bin","zb.png",[
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
],logy=False)

hists = plotVariable(tree,c,"tb",5000,-1,1,"Muon Production t [s]","Events/bin","tb.png",[
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
],logy=False)

