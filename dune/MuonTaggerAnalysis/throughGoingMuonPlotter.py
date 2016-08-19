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

  f2 = root.TFile("MuonTaggerTree_10k.root")
  tree2 = f2.Get("muontaggertreemaker/tree")
  for iEntry in range(tree2.GetEntries()):
    if iEntry > 100:
      continue
    tree2.GetEntry(iEntry)
    print "Event: ",iEntry
    for iPoint in range(tree2.numberTrajectoryPoints):
      if iPoint > 0:
        dx = tree2.trajx[iPoint] - tree2.trajx[iPoint-1]
        dy = tree2.trajy[iPoint] - tree2.trajy[iPoint-1]
        dz = tree2.trajz[iPoint] - tree2.trajz[iPoint-1]
        dr = sqrt(dx**2+dy**2+dz**2)
        print dr
    

