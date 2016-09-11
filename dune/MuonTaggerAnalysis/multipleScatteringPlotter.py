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

if __name__ == "__main__":
  c = root.TCanvas()
  treeName = "muontaggertreemaker/tree"
  scaleFactor = 1.#/nEvents*8.*166.

  ################################################################

  fileConfigs = [
    {
      "fn": "/pnfs/dune/scratch/users/jhugon/v06_05_00/muontaggertree/muontaggertree_v4/anahist.root",
      "name": "multipleScatteringMuons",
    },
  ]
  histConfigs = [
    {
      "name":   "scatDist",
      "var":    "trajDistToLine",
      "binning":[100,0.,10.],
      "xtitle": "True trajectory distance to muon tagger line [cm]",
      "ytitle": "Trajectory points/distance [cm^{-1}]",
      "cuts":   "hitsFrontDet && hitsBackDet",
      "normToBinWidth": True,
    },
    {
      "name":   "scatDistLogLog",
      "var":    "trajDistToLine",
      #"binning":[1000,0.,10.],
      "binning":getLogBins(100,1e-4,1e2),
      "xtitle": "True trajectory distance to muon tagger line [cm]",
      "ytitle": "Trajectory points/distance [cm^{-1}]",
      "cuts":   "hitsFrontDet && hitsBackDet",
      "normToBinWidth": True,
      "logx": True,
      "logy": True,
    },
    {
      "name":   "tof",
      "var":    "fabs(backDetHitT - frontDetHitT)",
      "binning":[80,20.,40],
      "xtitle": "Front/back muon tagger hit #Delta t [ns]",
      "ytitle": "Muons/bin",
      "cuts":   "hitsFrontDet && hitsBackDet",
    },
    {
      "name":   "tofVE",
      "var":    "fabs(backDetHitT - frontDetHitT):pEb",
      "binning":[30,0.,20.,80,20,40],
      "xtitle": "Initial muon energy [GeV]",
      "ytitle": "Front/back muon tagger hit #Delta t [ns]",
      "cuts":   "hitsFrontDet && hitsBackDet",
    },
  ]

  plotOneHistOnePlot(fileConfigs,histConfigs,c,treeName)

