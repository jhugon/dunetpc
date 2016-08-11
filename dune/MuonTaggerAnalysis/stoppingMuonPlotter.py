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

def plotVariable1D(tree,canvas,variable,nBinsX,xMin,xMax,xlabel,ylabel,saveName,cuts="",drawopt="",logx=False,logy=False,caption="",captionleft1="",captionleft2="",captionleft3="",captionright1="",captionright2="",captionright3="",preliminaryString=""):
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
  hist.SetTitle("")
  setHistTitles(hist,xlabel,ylabel)
  drawStandardCaptions(canvas,caption,captionleft1,captionleft2,captionleft3,captionright1,captionright2,captionright3,preliminaryString)
  canvas.SaveAs(saveName)
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
  hist.SetTitle("")
  setHistTitles(hist,xlabel,ylabel)
  drawStandardCaptions(canvas,caption,captionleft1,captionleft2,captionleft3,captionright1,captionright2,captionright3,preliminaryString)
  canvas.SaveAs(saveName)
  setupCOLZFrame(canvas,reset=True)
  return hist


if __name__ == "__main__":
  c = root.TCanvas()
  f = root.TFile("MuonTaggerTree.root")
  
  tree = f.Get("muontaggertreemaker/tree")
  tree.Print()
  
  #for iEvent in range(tree.GetEntries()):
  #for iEvent in range(100):
  #  tree.GetEntry(iEvent)
  #  if tree.inWideTPCe:
  #    print tree.xe, tree.ye, tree.ze, tree.pe
  #tree.Scan("numberTrajectoryPoints")

  plotVariable1D(tree,c,"xb",100,-1000,1000,"Muon Starting x [cm]","Events/bin","Start_x.png",cuts="")
  plotVariable1D(tree,c,"yb",500,0,1000,"Muon Starting y [cm]","Events/bin","Start_y.png",cuts="")
  plotVariable1D(tree,c,"zb",100,-2000,2000,"Muon Starting z [cm]","Events/bin","Start_z.png",cuts="")
  #plotVariable2D(tree,c,"yb:xb",40,-400,400,40,0,800,"Muon Starting x [cm]","Muon Starting y [cm]","Start_yVx.png",cuts="")
  #plotVariable2D(tree,c,"zb:yb",40,0,800,35,-10,690,"Muon Starting y [cm]","Muon Starting z [cm]","Start_zVy.png",cuts="")
  plotVariable2D(tree,c,"zb:xb",40,-400,400,35,-10,690,"Muon Starting x [cm]","Muon Starting z [cm]","Start_zVx.png",cuts="")

  plotVariable2D(tree,c,"ye:xe",40,-400,400,40,0,800,"Stopping Muon x [cm]","Stopping Muon y [cm]","Stop_yVx.png",cuts="inWideTPCe && pe<0.01")
  plotVariable2D(tree,c,"ze:ye",40,0,800,35,-10,690,"Stopping Muon y [cm]","Stopping Muon z [cm]","Stop_zVy.png",cuts="inWideTPCe && pe<0.01")
  plotVariable2D(tree,c,"ze:xe",40,-400,400,35,-10,690,"Stopping Muon x [cm]","Stopping Muon z [cm]","Stop_zVx.png",cuts="inWideTPCe && pe<0.01")

  plotVariable2D(tree,c,"ze:xe",40,-400,400,35,-10,690,"Stopping Muon x [cm]","Stopping Muon z [cm]","Stop_zVx_cuts.png",cuts="inWideTPCe && pe<0.01 && xb < 200 & xb > 0 && zb < 200 && zb > 0",caption="Muon Starting 0<x<200 cm and 0<z<200cm")

  plotVariable2D(tree,c,"180-thetazenithb*180/pi:zb",40,-400,400,45,0,90,"Stopping Muon x [cm]","Muon #theta_{zenith} [deg]","thetazVz.png",cuts="")

  tree.Scan("xb:yb:zb:180-thetazenithb*180/pi")
