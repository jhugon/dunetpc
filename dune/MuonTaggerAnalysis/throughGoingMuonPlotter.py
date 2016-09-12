#!/usr/bin/env python

import random
import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

if __name__ == "__main__":
  c = root.TCanvas()
  treeName = "muontaggertreemaker/tree"

  f = root.TFile("/pnfs/dune/scratch/users/jhugon/v06_05_00/muontaggertree/muontaggertree_v4/anahist.root")
  tree = f.Get("muontaggertreemaker/tree")
  nEntries = tree.GetEntries()
  print "tree nEntries: ", nEntries
  nEvents = 4200
  print "tree nEvents: ", nEvents

  ################################################################

  scaleFactorPerEvent = 1. / nEvents
  scaleFactorHz = 1. / nEvents / 6.45e-3

  fileConfigs = [
    {
      "fn": "/pnfs/dune/scratch/users/jhugon/v06_05_00/muontaggertree/muontaggertree_v4/anahist.root",
      #"fn":"/pnfs/dune/scratch/users/jhugon/v06_05_00/muontaggertree/muontaggertree_v4/10431460_1/MuonTaggerTree.root",
      "name": "throughGoingMuons",
    },
  ]
  histConfigs = [
    {
      "name":   "thetazenithb",
      "title": "All Muons",
      "var":    "thetazenithb*180/pi",
      "binning":[60,90,180],
      "xtitle": "Zenith angle [degrees]",
      "ytitle": "Normalized Muons / bin",
      "cuts":   "",
      "normalize": True,
    },
    {
      "name":   "thetazenithb_taggedfb",
      "title":  "Front/Back Tagged Muons",
      "var":    "thetazenithb*180/pi",
      "binning":[60,90,180],
      "xtitle": "Zenith angle [degrees]",
      "ytitle": "Normalized Muons / bin",
      "cuts":   "hitsFrontDet && hitsBackDet",
      "color": root.kRed,
      "normalize": True,
    },
  ]

  plotManyHistsOnePlot(fileConfigs,histConfigs,c,treeName,outPrefix="thetazenithb")

  histConfigs = [
    {
      "name":   "pEb",
      "title": "All Muons",
      "var":    "pEb",
      "binning": [50,0.,20],
      "xtitle": "Initial muon energy [GeV]",
      "ytitle": "Normalized muons per energy [GeV^{-1}]",
      "cuts":   "",
      "normalize": True,
    },
    {
      "name":   "pEb_taggedfb",
      "title":  "Front/Back Tagged Muons",
      "var":    "pEb",
      "binning": [50,0.,20],
      "xtitle": "Initial muon energy [GeV]",
      "ytitle": "Normalized muons per energy [GeV^{-1}]",
      "cuts":   "hitsFrontDet && hitsBackDet",
      "color": root.kRed,
      "normalize": True,
    },
  ]

  plotManyHistsOnePlot(fileConfigs,histConfigs,c,treeName,outPrefix="pEb")

  histConfigs = [
    {
      "name":   "pb",
      "title": "All Muons",
      "var":    "pb",
      "binning": [50,0.,20],
      "xtitle": "Initial muon momentum [GeV]",
      "ytitle": "Normalized muons per momentum [GeV^{-1}]",
      "cuts":   "",
      "normalize": True,
    },
    {
      "name":   "pb_taggedfb",
      "title":  "Front/Back Tagged Muons",
      "var":    "pb",
      "binning": [50,0.,20],
      "xtitle": "Initial muon momentum [GeV]",
      "ytitle": "Normalized muons per momentum [GeV^{-1}]",
      "cuts":   "hitsFrontDet && hitsBackDet",
      "color": root.kRed,
      "normalize": True,
    },
  ]

  plotManyHistsOnePlot(fileConfigs,histConfigs,c,treeName,outPrefix="pb")
