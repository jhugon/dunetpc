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

def plotVariable1D(tree,canvas,variable,nBinsX,xMin,xMax,xlabel,ylabel,saveName,cuts="",drawopt="",logx=False,logy=False,caption="",captionleft1="",captionleft2="",captionleft3="",captionright1="",captionright2="",captionright3="",preliminaryString="",scaleFactor=1.):
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
  hist.Scale(scaleFactor)
  hist.UseCurrentStyle()
  hist.SetTitle("")
  setHistTitles(hist,xlabel,ylabel)
  drawStandardCaptions(canvas,caption,captionleft1,captionleft2,captionleft3,captionright1,captionright2,captionright3,preliminaryString)
  canvas.SaveAs(saveName)
  #canvas.SaveAs(saveName+".C")
  #canvas.SaveAs(saveName+".root")
  #outfile = root.TFile(saveName+".root","RECREATE")
  #outfile.cd()
  #hist.Write()
  #outfile.Close()
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
  hist.UseCurrentStyle()
  hist.SetTitle("")
  setHistTitles(hist,xlabel,ylabel)
  drawStandardCaptions(canvas,caption,captionleft1,captionleft2,captionleft3,captionright1,captionright2,captionright3,preliminaryString)
  canvas.RedrawAxis()
  canvas.SaveAs(saveName)
  setupCOLZFrame(canvas,reset=True)
  return hist


if __name__ == "__main__":
  c = root.TCanvas()
  f = root.TFile("MuonTaggerTree.root")
  
  tree = f.Get("muontaggertreemaker/tree")
  #tree.Print()
  
  #for iEvent in range(tree.GetEntries()):
  #for iEvent in range(100):
  #  tree.GetEntry(iEvent)
  #  if tree.inWideTPCe:
  #    print tree.xe, tree.ye, tree.ze, tree.pe
  #tree.Scan("numberTrajectoryPoints")

  ## I think the sample assumes the detector is x: 0-200 and z: 0-150

  plotVariable1D(tree,c,"xb",100,-100,300,"Muon Starting x [cm]","Events/bin","Start_x.png",cuts="")
  plotVariable1D(tree,c,"yb",500,0,1000,"Muon Starting y [cm]","Events/bin","Start_y.png",cuts="")
  plotVariable1D(tree,c,"zb",100,-100,250,"Muon Starting z [cm]","Events/bin","Start_z.png",cuts="")
  #plotVariable2D(tree,c,"yb:xb",40,-400,400,40,0,800,"Muon Starting x [cm]","Muon Starting y [cm]","Start_yVx.png",cuts="")
  #plotVariable2D(tree,c,"zb:yb",40,0,800,35,-10,690,"Muon Starting y [cm]","Muon Starting z [cm]","Start_zVy.png",cuts="")
  plotVariable2D(tree,c,"zb:xb",40,-100,300,35,-100,250,"Muon Starting x [cm]","Muon Starting z [cm]","Start_zVx.png",cuts="")
  plotVariable2D(tree,c,"zb:xb",40,-100,300,35,-100,250,"Muon Starting x [cm]","Muon Starting z [cm]","Start_zVx_cuts.png",cuts="thetazenithb > pi*170/180",caption="#theta_{zenith} > 170 deg")
  plotVariable2D(tree,c,"zb:xb",100,-150,350,100,-150,250,"Muon Starting x [cm]","Muon Starting z [cm]","Start_zVx_cuts2.png",cuts="thetazenithb > pi*178/180",caption="#theta_{zenith} > 178 deg")

  plotVariable2D(tree,c,"ye:xe",8,0,200,12,0,600,"Stopping Muon x [cm]","Stopping Muon y [cm]","Stop_yVx.png",cuts="inWideTPCe && pe<0.01 && ze > 0 && ze < 150")
  plotVariable2D(tree,c,"ye:ze",6,0,150,12,0,600,"Stopping Muon z [cm]","Stopping Muon y [cm]","Stop_yVz.png",cuts="inWideTPCe && pe<0.01 && xe > 0 && xe < 200")
  plotVariable2D(tree,c,"ze:xe",8,0,200,6,0,150,"Stopping Muon x [cm]","Stopping Muon z [cm]","Stop_zVx.png",cuts="inWideTPCe && pe<0.01 && ye > 0 && ye < 600")

  plotVariable2D(tree,c,"ze:xe",40,-400,400,35,-10,690,"Stopping Muon x [cm]","Stopping Muon z [cm]","Stop_zVx_cuts.png",cuts="inWideTPCe && pe<0.01 && xb < 200 & xb > 0 && zb < 200 && zb > 0",caption="Muon Starting 0<x<200 cm and 0<z<200cm")

  plotVariable2D(tree,c,"180-thetazenithb*180/pi:zb",40,-400,400,45,0,90,"Stopping Muon x [cm]","Muon #theta_{zenith} [deg]","thetazVz.png",cuts="")

  stop_y_hist = plotVariable1D(tree,c,"ye",6,0,600,"Muon Stopping y [cm]","Stopping Muon Rate [Hz m^{-3}]","Stop_y.pdf",cuts="inWideTPCe && pe<0.01 && xe > 50 && xe < 150 && ze > 25 && ze < 125",scaleFactor=1./2e5*8.*166.)
  print "stop_y_hist integral: {0}".format(stop_y_hist.Integral())
  stop_ally_hist = plotVariable1D(tree,c,"ye",22,-1200,1000,"Muon Stopping y [cm]","Stopping Muon Rate [Hz m^{-3}]","Stop_ally.png",cuts="pe<0.01 && xe > 50 && xe < 150 && ze > 25 && ze < 125",scaleFactor=1./2e5*8.*166.)
  print "stop_ally_hist integral: {0}".format(stop_ally_hist.Integral())
  plotVariable1D(tree,c,"ye",10,0,1000,"Muon Stopping y [cm]","Stopping Muon Rate [Hz m^{-3}]","Stop_mosty.png",cuts="pe<0.01 && xe > 50 && xe < 150 && ze > 25 && ze < 125",scaleFactor=1./2e5*8.*166.)
  plotVariable1D(tree,c,"ye",100,0,1000,"Muon Stopping y [cm]","Stopping Muon Rate [Hz m^{-3}]","Stop_mostyfine.png",cuts="pe<0.01 && xe > 50 && xe < 150 && ze > 25 && ze < 125",scaleFactor=1./2e5*8.*166.*10)

  plotVariable2D(tree,c,"ye:pb",40,0.,10,10,0,1000,"Initial Muon Momentum [GeV/c]","Stopping Muon y [cm]","stop_mostyVpb.png",cuts="pe<0.01 && xe > 50 && xe < 150 && ze > 25 && ze < 125")

  #tree.Scan("xb:yb:zb:180-thetazenithb*180/pi")

  f2 = root.TFile("MuonTaggerTree_10k.root")
  tree2 = f2.Get("muontaggertreemaker/tree")
  trajXY = f2.Get("muontaggertreemaker/trajectoryXY")
  trajZY = f2.Get("muontaggertreemaker/trajectoryZY")
  trajXZ = f2.Get("muontaggertreemaker/trajectoryXZ")
  setupCOLZFrame(c)
  trajXY.UseCurrentStyle()
  trajZY.UseCurrentStyle()
  trajXZ.UseCurrentStyle()
  trajXY.GetXaxis().SetRangeUser(-200,400)
  trajXY.GetYaxis().SetRangeUser(-500,1000)
  trajXZ.GetXaxis().SetRangeUser(-200,400)
  trajXZ.GetYaxis().SetRangeUser(-200,400)
  trajZY.GetXaxis().SetRangeUser(-200,400)
  trajZY.GetYaxis().SetRangeUser(-500,1000)
  setHistTitles(trajXY,"Trajectory point x [cm]","Trajectory point y [cm]")
  setHistTitles(trajZY,"Trajectory point z [cm]","Trajectory point y [cm]")
  setHistTitles(trajXZ,"Trajectory point x [cm]","Trajectory point z [cm]")
  trajXY.Draw("colz")
  c.SaveAs("trajXY.png")
  trajZY.Draw("colz")
  c.SaveAs("trajZY.png")
  trajXZ.Draw("colz")
  c.SaveAs("trajXZ.png")

#  #plotVariable2D(tree2,c,"trajy:trajx",100,-200,400,100,-500,1000,"Trajectory point x [cm]","Trajectory point y [cm]","trajXY_tree.png",cuts="")
#  plotVariable2D(tree2,c,"trajy:trajx",100,-200,400,100,-500,1000,"Trajectory point x [cm]","Trajectory point y [cm]","trajXY_cuts1.png",cuts="thetazenithb < pi*150/180",caption="#theta_{zenith} < 150 deg")
#  plotVariable2D(tree2,c,"trajy:trajx",100,-200,400,100,-500,1000,"Trajectory point x [cm]","Trajectory point y [cm]","trajXY_cuts2.png",cuts="xb < 200 & xb > 0 && zb < 200 && zb > 0",caption="Muon Starting 0<x<200 cm and 0<z<200cm")
#  plotVariable2D(tree2,c,"trajy:trajx",100,-200,400,100,-500,1000,"Trajectory point x [cm]","Trajectory point y [cm]","trajXY_cuts3.png",cuts="!(xb < 200 & xb > 0 && zb < 200 && zb > 0)",caption="Muon Not Starting in 0<x<200 cm and 0<z<200cm")
#  plotVariable2D(tree2,c,"trajy:trajx",100,-200,400,100,-500,1000,"Trajectory point x [cm]","Trajectory point y [cm]","trajXY_cuts4.png",cuts="inWideTPCe && pe<0.01 ",caption="Stopping Muons in TPC")

