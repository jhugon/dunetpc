#!/usr/bin/env python

import random
import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

def makeLineXY(xb,yb,pxb,pyb,minx=-1000,maxx=1000,miny=-1000,maxy=1000):
    x1 = minx
    x2 = maxx
    m = pyb/pxb
    b = yb - m * xb
    y1 = m*x1+b
    y2 = m*x2+b
    #if y1 > maxy or y1 < maxx or y2 > maxy or y2 < maxy:
    #  y1 = miny
    #  y2 = maxy
    #  x1 = (y1 - b) / m
    #  x2 = (y2 - b) / m
    if y1 < miny:
      y1 = miny
      x1 = (y1 - b) / m
    if y1 > miny:
      y1 = maxy
      x1 = (y1 - b) / m
    if y2 < miny:
      y2 = miny
      x2 = (y2 - b) / m
    if y2 > miny:
      y2 = maxy
      x2 = (y2 - b) / m
    line = root.TLine(x1,y1,x2,y2)
    line.SetLineWidth(1)
    return line

def projectToYPlane(tree,y=600.):
    mx = tree.pxb/tree.pyb
    mz = tree.pzb/tree.pyb
    bx = tree.xb - mx*tree.yb
    bz = tree.zb - mz*tree.yb
    x = mx*y + tree.xb
    z = mz*y + tree.zb
    return x, z

c = root.TCanvas()
f = root.TFile("/pnfs/dune/persistent/users/jhugon/v06_05_00/g4/muontaggertree_v1/anahist.root")

tree = f.Get("muontaggertreemaker/tree")

maxEvents = 1000000
nEvents = min(maxEvents,tree.GetEntries())

axisHistXY = Hist2D(1,-1000,1000,1,-1000,1000)
histXZ600 = Hist2D(100,-500,500,100,-200,800)
histXY = Hist2D(50,-500,500,10,-1000,1000)
histZY = Hist2D(60,-200,1000,10,-1000,1000)
linesXY = []
for iEvent in range(nEvents):
  tree.GetEntry(iEvent)
  line = makeLineXY(tree.xb,tree.yb,tree.pxb,tree.pyb)
  linesXY.append(line)

  x,z = projectToYPlane(tree,600.)
  if tree.thetazenithb > math.pi*160/180.:
    histXZ600.Fill(x,z)

  for i in range(1,histXY.GetYaxis().GetNbins()+1):
    y = histXY.GetYaxis().GetBinCenter(i)
    x, z = projectToYPlane(tree,y)
    histXY.Fill(x,y)
    histZY.Fill(z,y)

axisHistXY.Draw()
setHistTitles(axisHistXY,"Generator muon x [cm]", "Generator muon y [cm]")
for line in linesXY:
  line.Draw()
c.SaveAs("test1.png")
  
setupCOLZFrame(c)
setHistTitles(histXZ600,"Generator muon x [cm]", "Generator muon z [cm]")
histXZ600.Draw("colz")
c.SaveAs("test2.png")
  
setHistTitles(histXY,"Generator muon x [cm]", "Generator muon y [cm]")
histXY.Draw("colz")
c.SaveAs("test3.png")

setHistTitles(histZY,"Generator muon z [cm]", "Generator muon y [cm]")
histZY.Draw("colz")
c.SaveAs("test4.png")




