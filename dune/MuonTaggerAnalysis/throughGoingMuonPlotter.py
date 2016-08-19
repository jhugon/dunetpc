#!/usr/bin/env python

import random
import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

from stoppingMuonPlotter import *

#xb
#yb
#zb
#tb
#xe
#ye
#ze
#te
#
#pxb
#pyb
#pzb
#pEb
#pxe
#pye
#pze
#pEe
#
#pb
#pe
#thetab
#costhetab
#phib
#
#thetazenithb
#costhetazenithb
#phizenithb
#
#inTPCe
#inWideTPCe

if __name__ == "__main__":
  c = root.TCanvas()
  f = root.TFile("MuonTaggerTree.root")
  
  tree = f.Get("muontaggertreemaker/tree")
  nEvents = tree.GetEntries()
  scaleFactor = 1./nEvents*8.*166.

  plotVariable1D(tree,c,"thetab*180/pi",18,0,180,"Muon #theta w.r.t. beam direction [deg]","Events/bin","thetab.png",cuts="",scaleFactor=1.)
  plotVariable1D(tree,c,"acos(pxb/pb)*180/pi",18,0,180,"Muon #theta w.r.t. x-axis [deg]","Events/bin","thetax.png",cuts="",scaleFactor=1.)
  plotVariable1D(tree,c,"fabs(acos(pxb/pb)*180/pi-90)",18,0,180,"Muon #theta w.r.t. APA plane [deg]","Events/bin","thetaxplane.png",cuts="",scaleFactor=1.)
  plotVariable1D(tree,c,"fabs(acos(pxb/pb)*180/pi-90)",18,0,180,"Muon #theta w.r.t. APA plane [deg]","Events/bin","thetaxplane_cuts.png",cuts="fabs(thetab*180/pi-90)>50",scaleFactor=1.)


