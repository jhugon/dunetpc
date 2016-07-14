#!/usr/bin/env python

"""
TFile**     MuonTaggerTree.root 
 TFile*     MuonTaggerTree.root 
  TDirectoryFile*       muontaggertreemaker muontaggertreemaker (MuonTaggerTreeMaker) folder
   KEY: TTree   tree;1  tree
   KEY: TTree   treeTrajPoints;1    treeTrajPoints
   KEY: TH1F    trajectoryX;1   
   KEY: TH1F    trajectoryY;1   
   KEY: TH1F    trajectoryZ;1   
  KEY: TDirectoryFile   muontaggertreemaker;1   muontaggertreemaker (MuonTaggerTreeMaker) folder
root [6] treeTrajPoints->Point
Error: Failed to evaluate class member 'Point' (treeTrajPoints->Point)
*** Interpreter error recovered ***
root [7] treeTrajPoints->Print()
******************************************************************************
*Tree    :treeTrajPoints: treeTrajPoints                                         *
*Entries :    77439 : Total =         1555666 bytes  File  Size =     843299 *
*        :          : Tree compression factor =   1.84                       *
******************************************************************************
*Br    0 :pb        : pb/F                                                   *
*Entries :    77439 : Total  Size=     311028 bytes  File Size  =       5476 *
*Baskets :       10 : Basket Size=      32000 bytes  Compression=  56.71     *
*............................................................................*
*Br    1 :thetazenithb : thetazenithb/F                                      *
*Entries :    77439 : Total  Size=     311168 bytes  File Size  =       5407 *
*Baskets :       10 : Basket Size=      32000 bytes  Compression=  57.45     *
*............................................................................*
*Br    2 :p         : p/F                                                    *
*Entries :    77439 : Total  Size=     311014 bytes  File Size  =     275902 *
*Baskets :       10 : Basket Size=      32000 bytes  Compression=   1.13     *
*............................................................................*
*Br    3 :E         : E/F                                                    *
*Entries :    77439 : Total  Size=     311014 bytes  File Size  =     281602 *
*Baskets :       10 : Basket Size=      32000 bytes  Compression=   1.10     *
*............................................................................*
*Br    4 :dEdx      : dEdx/F                                                 *
*Entries :    77439 : Total  Size=     311056 bytes  File Size  =     273803 *
*Baskets :       10 : Basket Size=      32000 bytes  Compression=   1.13     *
*............................................................................*

and  inTPC bool
and  inWideTPC bool
"""

import random
import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

f = root.TFile("MuonTaggerTree.root")

tree = f.Get("muontaggertreemaker/treeTrajPoints")
#tree.Print()

c = root.TCanvas()

def plotVariable2D(tree,canvas,variable,nBinsX,xMin,xMax,nBinsY,yMin,yMax,xlabel,ylabel,saveName,cuts="",drawopt="COL",logx=False,logy=False):
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
  hist.SetTitle("")
  setHistTitles(hist,xlabel,ylabel)
  canvas.SaveAs(saveName)
  return hist

if __name__ == "__main__":

  plotVariable2D(tree,c,"dEdx*1000.:E",50,0.,10.,100,0.,5.,"Muon Energy [GeV]","dE/dx [MeV/cm]","dEdxVE_notTPC.png",cuts="inTPC == 0")
  plotVariable2D(tree,c,"dEdx*1000.:p",50,0.,10.,100,0.,5.,"Muon Momentum [GeV/c]","dE/dx [MeV/cm]","dEdxVp_notTPC.png",cuts="inTPC == 0")
  plotVariable2D(tree,c,"dEdx*1000.:E",50,0.,10.,100,0.,5.,"Muon Energy [GeV]","dE/dx [MeV/cm]","dEdxVE_narrowTPC.png",cuts="inTPC && inWideTPC == 0")
  plotVariable2D(tree,c,"dEdx*1000.:p",50,0.,10.,100,0.,5.,"Muon Momentum [GeV/c]","dE/dx [MeV/cm]","dEdxVp_narrowTPC.png",cuts="inTPC && inWideTPC == 0")
  plotVariable2D(tree,c,"dEdx*1000.:E",50,0.,10.,100,1.,3.,"Muon Energy [GeV]","dE/dx [MeV/cm]","dEdxVE_wideTPC.png",cuts="inWideTPC")
  plotVariable2D(tree,c,"dEdx*1000.:p",50,0.,10.,100,1.,3.,"Muon Momentum [GeV/c]","dE/dx [MeV/cm]","dEdxVp_wideTPC.png",cuts="inWideTPC")
  plotVariable2D(tree,c,"E:p",100,0.,1.,100,0.,1.,"Muon Momentum [GeV/c]","Muon Energy [GeV]","EVp.png",cuts="")
