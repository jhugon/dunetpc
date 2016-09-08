////////////////////////////////////////////////////////////////////////
// Class:       MuonTaggerTreeMaker
// Module Type: analyzer
// File:        MuonTaggerTreeMaker_module.cc
//
// Generated at Tue Jun 28 16:02:09 2016 by JustinHugon using artmod
// from cetpkgsupport v1_10_01.
////////////////////////////////////////////////////////////////////////

#include "art/Framework/Core/EDAnalyzer.h"
#include "art/Framework/Core/ModuleMacros.h"
#include "art/Framework/Principal/Event.h"
#include "art/Framework/Principal/Handle.h"
#include "art/Framework/Principal/Run.h"
#include "art/Framework/Principal/SubRun.h"
#include "canvas/Utilities/InputTag.h"
#include "fhiclcpp/ParameterSet.h"
#include "messagefacility/MessageLogger/MessageLogger.h"
#include "art/Framework/Services/Optional/TFileService.h"

#include <iostream>
#include <iomanip>
#include <string>
#include <cmath>

#include "larcore/Geometry/Geometry.h"
#include "larcore/Geometry/TPCGeo.h"
#include "larcore/Geometry/AuxDetGeo.h"

#include "nusimdata/SimulationBase/MCTruth.h"
#include "nusimdata/SimulationBase/MCParticle.h"
#include "lardataobj/Simulation/SimChannel.h"
#include "lardataobj/Simulation/AuxDetSimChannel.h"

#include "TH1D.h"
#include "TH2D.h"
#include "TFile.h"
#include "TTree.h"
#include "TDatabasePDG.h"
#include "TMath.h"

class MinMaxFinder 
{
  private:
    float _min;
    float _max;
  public:
    MinMaxFinder();
    void addPoint(float x);
    float getMax() const {return _max;};
    float getMin() const {return _min;};
};

bool inATPC(const TLorentzVector& v, const geo::Geometry& geom, float minTPCWidth=20.)
{
  for(auto& tpc: geom.IterateTPCs())
  {
    if (tpc.HalfWidth()*2 > minTPCWidth)
    {
      if (tpc.ContainsPosition(v.Vect()))
      {
        return true;
      }
    }
  }
  return false;
}

MinMaxFinder::MinMaxFinder():
    _min(1e20), _max(-1e20)
{}

void MinMaxFinder::addPoint(float x)
{
  if (x > _max)
  {
    _max = x;
  }
  if (x < _min)
  {
    _min = x;
  }
}

namespace dune {
  class MuonTaggerTreeMaker;
}

class dune::MuonTaggerTreeMaker : public art::EDAnalyzer {
public:
  explicit MuonTaggerTreeMaker(fhicl::ParameterSet const & p);
  // The destructor generated by the compiler is fine for classes
  // without bare pointers or other resource use.

  // Plugins should not be copied or assigned.
  MuonTaggerTreeMaker(MuonTaggerTreeMaker const &) = delete;
  MuonTaggerTreeMaker(MuonTaggerTreeMaker &&) = delete;
  MuonTaggerTreeMaker & operator = (MuonTaggerTreeMaker const &) = delete;
  MuonTaggerTreeMaker & operator = (MuonTaggerTreeMaker &&) = delete;

  // Required functions.
  void analyze(art::Event const & e) override;
  virtual void beginJob() override;
  virtual void endJob() override;

private:

  // Declare member data here.
  art::InputTag _mcParticleTag;
  art::InputTag _simChannelTag;
  art::InputTag _auxDetSimChannelTag;

  float _frontDetectorXmin;
  float _frontDetectorXmax;
  float _frontDetectorYmin;
  float _frontDetectorYmax;
  float _frontDetectorZ;

  float _backDetectorXmin;
  float _backDetectorXmax;
  float _backDetectorYmin;
  float _backDetectorYmax;
  float _backDetectorZ;

  bool _writeTrajectoryInfo;
  bool _writeIDEInfo;

  TTree* _outtree;
  TH1F* _trajectoryX;
  TH1F* _trajectoryY;
  TH1F* _trajectoryZ;
  TH2F* _trajectoryXY;
  TH2F* _trajectoryZY;
  TH2F* _trajectoryXZ;

  // tree data members
  //

  float _xb;
  float _yb;
  float _zb;
  float _tb;
  float _xe;
  float _ye;
  float _ze;
  float _te;

  float _pxb;
  float _pyb;
  float _pzb;
  float _pEb;
  float _pxe;
  float _pye;
  float _pze;
  float _pEe;

  float _pb;
  float _pe;
  float _thetab;
  float _costhetab;
  float _phib;

  float _thetazenithb;
  float _costhetazenithb;
  float _phizenithb;

  bool _inTPCe;
  bool _inWideTPCe;

  int _numberTrajectoryPoints;

  std::vector<float> _trajx;
  std::vector<float> _trajy;
  std::vector<float> _trajz;
  std::vector<float> _trajt;
  std::vector<float> _trajp;
  std::vector<float> _trajE;
  std::vector<float> _trajdEdx;
  std::vector<bool> _trajInTPC;
  std::vector<bool> _trajInWideTPC;

  int _numberIDEs;
  std::vector<float> _idex;
  std::vector<float> _idey;
  std::vector<float> _idez;

  bool _hitsFrontDet;
  bool _hitsBackDet;

  MinMaxFinder _minMaxFinderTrajX;
  MinMaxFinder _minMaxFinderTrajY;
  MinMaxFinder _minMaxFinderTrajZ;
  MinMaxFinder _minMaxFinderTrajT;

  MinMaxFinder _minMaxFinderXb; // b means begin
  MinMaxFinder _minMaxFinderYb;
  MinMaxFinder _minMaxFinderZb;

  // private functions
  bool hitsDetectorPlane(const simb::MCParticle& part, bool backDetector = false); // if false, front detector
};


dune::MuonTaggerTreeMaker::MuonTaggerTreeMaker(fhicl::ParameterSet const & p)
  :
  EDAnalyzer(p)  // ,
 // More initializers here.
{
  _mcParticleTag = p.get<art::InputTag>("mcParticleTag");
  std::cout << "_mcParticleTag: " << _mcParticleTag << std::endl;
  _simChannelTag = p.get<art::InputTag>("simChannelTag");
  std::cout << "_simChannelTag: " << _simChannelTag << std::endl;
  _auxDetSimChannelTag = p.get<art::InputTag>("auxDetSimChannelTag");
  std::cout << "_auxDetSimChannelTag: " << _auxDetSimChannelTag << std::endl;

  _frontDetectorXmin = p.get<float>("frontDetectorXmin");
  _frontDetectorXmax = p.get<float>("frontDetectorXmax");
  _frontDetectorYmin = p.get<float>("frontDetectorYmin");
  _frontDetectorYmax = p.get<float>("frontDetectorYmax");
  _frontDetectorZ = p.get<float>("frontDetectorZ");
  std::cout << "front detector X: " << _frontDetectorXmin << " - " << _frontDetectorXmax << std::endl;
  std::cout << "front detector Y: " << _frontDetectorYmin << " - " << _frontDetectorYmax << std::endl;
  std::cout << "front detector Z: " << _frontDetectorZ << std::endl;

  _backDetectorXmin = p.get<float>("backDetectorXmin");
  _backDetectorXmax = p.get<float>("backDetectorXmax");
  _backDetectorYmin = p.get<float>("backDetectorYmin");
  _backDetectorYmax = p.get<float>("backDetectorYmax");
  _backDetectorZ = p.get<float>("backDetectorZ");
  std::cout << "back detector X: " << _backDetectorXmin << " - " << _backDetectorXmax << std::endl;
  std::cout << "back detector Y: " << _backDetectorYmin << " - " << _backDetectorYmax << std::endl;
  std::cout << "back detector Z: " << _backDetectorZ << std::endl;

  _writeTrajectoryInfo = p.get<bool>("writeTrajectoryInfo");
  std::cout << "writeTrajectoryInfo: " << _writeTrajectoryInfo << std::endl;
  _writeIDEInfo = p.get<bool>("writeIDEInfo");
  std::cout << "writeIDEInfo: " << _writeIDEInfo << std::endl;
}

void dune::MuonTaggerTreeMaker::beginJob()
{
  art::ServiceHandle<art::TFileService> tfs;
  _outtree = tfs->make<TTree>("tree","tree");

  _outtree->Branch("xb",&_xb,"xb/F");
  _outtree->Branch("yb",&_yb,"yb/F");
  _outtree->Branch("zb",&_zb,"zb/F");
  _outtree->Branch("tb",&_tb,"tb/F");
  _outtree->Branch("xe",&_xe,"xe/F");
  _outtree->Branch("ye",&_ye,"ye/F");
  _outtree->Branch("ze",&_ze,"ze/F");
  _outtree->Branch("te",&_te,"te/F");

  _outtree->Branch("pxb",&_pxb,"pxb/F");
  _outtree->Branch("pyb",&_pyb,"pyb/F");
  _outtree->Branch("pzb",&_pzb,"pzb/F");
  _outtree->Branch("pEb",&_pEb,"pEb/F");
  _outtree->Branch("pxe",&_pxe,"pxe/F");
  _outtree->Branch("pye",&_pye,"pye/F");
  _outtree->Branch("pze",&_pze,"pze/F");
  _outtree->Branch("pEe",&_pEe,"pEe/F");

  _outtree->Branch("pb",&_pb,"pb/F");
  _outtree->Branch("pe",&_pe,"pe/F");
  _outtree->Branch("thetab",&_thetab,"thetab/F");
  _outtree->Branch("costhetab",&_costhetab,"costhetab/F");
  _outtree->Branch("phib",&_phib,"phib/F");

  _outtree->Branch("thetazenithb",&_thetazenithb,"thetazenithb/F");
  _outtree->Branch("costhetazenithb",&_costhetazenithb,"costhetazenithb/F");
  _outtree->Branch("phizenithb",&_phizenithb,"phizenithb/F");

  _outtree->Branch("inTPCe",&_inTPCe,"inTPCe/O");
  _outtree->Branch("inWideTPCe",&_inWideTPCe,"inWideTPCe/O");

  _outtree->Branch("numberTrajectoryPoints",&_numberTrajectoryPoints,"numberTrajectoryPoints/I");

  if (_writeTrajectoryInfo)
  {
    _outtree->Branch("trajx",&_trajx);
    _outtree->Branch("trajy",&_trajy);
    _outtree->Branch("trajz",&_trajz);
    _outtree->Branch("trajt",&_trajt);
    _outtree->Branch("trajp",&_trajp);
    _outtree->Branch("trajE",&_trajE);
    _outtree->Branch("trajdEdx",&_trajdEdx);
    _outtree->Branch("trajInTPC",&_trajInTPC);
    _outtree->Branch("trajInWideTPC",&_trajInWideTPC);
  }
  if (_writeIDEInfo)
  {
    _outtree->Branch("numberIDEs",&_numberIDEs,"numberIDEs/I");
    _outtree->Branch("idex",&_idex);
    _outtree->Branch("idey",&_idey);
    _outtree->Branch("idez",&_idez);
  }

  _outtree->Branch("hitsFrontDet",&_hitsFrontDet,"hitsFrontDet/O");
  _outtree->Branch("hitsBackDet",&_hitsBackDet,"hitsBackDet/O");

  /////////////// Histos

  _trajectoryX = tfs->make<TH1F>("trajectoryX","",2000,-5000,5000);
  _trajectoryY = tfs->make<TH1F>("trajectoryY","",2000,-5000,1000);
  _trajectoryZ = tfs->make<TH1F>("trajectoryZ","",2000,-5000,5000);
  _trajectoryXY = tfs->make<TH2F>("trajectoryXY","",200,-500,750,200,-1000,1000);
  _trajectoryZY = tfs->make<TH2F>("trajectoryZY","",200,-1000,1000,200,-1000,1000);
  _trajectoryXZ = tfs->make<TH2F>("trajectoryXZ","",200,-500,750,200,-1000,1000);

  ////// Experiment w/ Geometry

  art::ServiceHandle<geo::Geometry> geom;
  std::cout << "Geometry: Detector Name:      '" << geom->DetectorName() << "'" << std::endl;
  std::cout << "Geometry: Number of Cryostats: " << geom->Ncryostats() << std::endl;
  std::cout << "Geometry: Number of TPCs:      " << geom->TotalNTPC() << std::endl;
  std::cout << "Geometry: Number of OpDets:    " << geom->NOpDets() << std::endl;
  std::cout << "Geometry: Number of AuxDets:   " << geom->NAuxDets() << std::endl;

  for(auto& cryostat: geom->IterateCryostats())
  {
    std::cout << "Cryostat mass: " << cryostat.Mass() << std::endl;
    std::cout << "Cryostat width:  " << 2*cryostat.HalfWidth() << std::endl;
    std::cout << "Cryostat height: " << 2*cryostat.HalfHeight() << std::endl;
    std::cout << "Cryostat length: " << cryostat.Length() << std::endl;
  }

  for(auto& tpc: geom->IterateTPCs())
  {
    std::cout << "TPC X in: " << tpc.MinX() << ", " << tpc.MaxX() << std::endl;
    std::cout << "TPC Y in: " << tpc.MinY() << ", " << tpc.MaxY() << std::endl;
    std::cout << "TPC Z in: " << tpc.MinZ() << ", " << tpc.MaxZ() << std::endl;
    std::cout << "  TPC width: " << tpc.HalfWidth()*2 << std::endl;
    std::cout << "  TPC height: " << tpc.HalfHeight()*2 << std::endl;
    std::cout << "  TPC length: " << tpc.Length() << std::endl;
    std::cout << "  TPC active width:  " << tpc.ActiveHalfWidth()*2 << std::endl;
    std::cout << "  TPC active height: " << tpc.ActiveHalfHeight()*2 << std::endl;
    std::cout << "  TPC active length: " << tpc.ActiveLength() << std::endl;
    std::cout << "  TPC active mass: " << tpc.ActiveMass() << std::endl;
  }

  std::vector<geo::AuxDetGeo *> const & auxDetGeos = geom->AuxDetGeoVec();
  for(auto& auxDetGeoPtr: auxDetGeos)
  {
    //std::cout << "AuxDet Named: '" << auxDetGeoPtr->Name() << "'" << std::endl;
    std::cout << "AuxDet Length: '" << auxDetGeoPtr->Length() << "'" << std::endl;
  }

}

void dune::MuonTaggerTreeMaker::analyze(art::Event const & e)
{
  // Implementation of required member function here.

  // Zero out vectors for tree
  _trajx.clear();
  _trajy.clear();
  _trajz.clear();
  _trajt.clear();
  _trajp.clear();
  _trajE.clear();
  _trajdEdx.clear();
  _trajInTPC.clear();
  _trajInWideTPC.clear();
  _idex.clear();
  _idey.clear();
  _idez.clear();

  //Get needed data products
  auto mcPartHand = e.getValidHandle<std::vector<simb::MCParticle>>(_mcParticleTag);
  std::vector<art::Ptr<simb::MCParticle>> mcPartVec;
  art::fill_ptr_vector(mcPartVec, mcPartHand);

  auto simChanHand = e.getValidHandle<std::vector<sim::SimChannel>>(_simChannelTag);
  std::vector<art::Ptr<sim::SimChannel>> simChanVec;
  art::fill_ptr_vector(simChanVec, simChanHand);

  auto auxDetSimChanHand = e.getValidHandle<std::vector<sim::AuxDetSimChannel>>(_auxDetSimChannelTag);
  std::vector<art::Ptr<sim::AuxDetSimChannel>> auxDetSimChanVec;
  art::fill_ptr_vector(auxDetSimChanVec, auxDetSimChanHand);

  art::ServiceHandle<geo::Geometry> geom;

  for (const auto& mcPart : mcPartVec)
  {
    //std::cout << "MC Particle: PDG ID: " << mcPart->PdgCode() << " Status: " << mcPart->StatusCode() << " momentum [GeV]: " << mcPart->Momentum().P();
    //std::cout << " Px,Py,Pz:    " <<mcPart->Momentum().X() <<", "<<mcPart->Momentum().Y()<<", "<<mcPart->Momentum().Z()<<", "<< std::endl;
    //std::cout << " Start X,Y,Z: " <<mcPart->Position().X() <<", "<<mcPart->Position().Y()<<", "<<mcPart->Position().Z()<<", "<< std::endl;
    //std::cout << " End X,Y,Z:   " <<mcPart->EndPosition().X() <<", "<<mcPart->EndPosition().Y()<<", "<<mcPart->EndPosition().Z()<<", "<< std::endl;
    //std::cout << " Process: "<< mcPart->Process() << " EndProcess: "<<mcPart->EndProcess()<<" NumberDaughters: "<<mcPart->NumberDaughters() << std::endl;
    if (abs(mcPart->PdgCode()) != 13)
        continue;

    //_hitsFrontDet = hitsDetectorPlane(*mcPart,false); // front
    //_hitsBackDet = hitsDetectorPlane(*mcPart,true); // back

    _xb = mcPart->Position().X();
    _yb = mcPart->Position().Y();
    _zb = mcPart->Position().Z();
    _tb = mcPart->Position().T();
    _minMaxFinderXb.addPoint(_xb);
    _minMaxFinderYb.addPoint(_yb);
    _minMaxFinderZb.addPoint(_zb);


    _xe = mcPart->EndPosition().X();
    _ye = mcPart->EndPosition().Y();
    _ze = mcPart->EndPosition().Z();
    _te = mcPart->EndPosition().T();

    _pxb = mcPart->Momentum().X();
    _pyb = mcPart->Momentum().Y();
    _pzb = mcPart->Momentum().Z();
    _pEb = mcPart->Momentum().T();
    _pxe = mcPart->EndMomentum().X();
    _pye = mcPart->EndMomentum().Y();
    _pze = mcPart->EndMomentum().Z();
    _pEe = mcPart->EndMomentum().T();

    _pb = mcPart->Momentum().P();
    _pe = mcPart->EndMomentum().P();
    _thetab = mcPart->Momentum().Theta();
    _costhetab = mcPart->Momentum().CosTheta();
    _phib = mcPart->Momentum().Phi();

    _costhetazenithb = _pyb/_pb;
    _thetazenithb = TMath::ACos(_costhetazenithb);
    _phizenithb = TMath::ATan2(_pzb,-_pxb);

    _inTPCe = inATPC(mcPart->EndPosition(),*geom,0.);
    _inWideTPCe = inATPC(mcPart->EndPosition(),*geom,20.);

    _numberTrajectoryPoints = mcPart->NumberTrajectoryPoints();

    for(unsigned iPoint=0; iPoint<mcPart->NumberTrajectoryPoints(); iPoint++)
    {
      _trajectoryX->Fill(mcPart->Position(iPoint).X());
      _trajectoryY->Fill(mcPart->Position(iPoint).Y());
      _trajectoryZ->Fill(mcPart->Position(iPoint).Z());

      _trajectoryXY->Fill(mcPart->Position(iPoint).X(),mcPart->Position(iPoint).Y());
      _trajectoryZY->Fill(mcPart->Position(iPoint).Z(),mcPart->Position(iPoint).Y());
      _trajectoryXZ->Fill(mcPart->Position(iPoint).X(),mcPart->Position(iPoint).Z());

      bool isInATPC = inATPC(mcPart->Position(iPoint),*geom,0.);
      bool isInAWideTPC = inATPC(mcPart->Position(iPoint),*geom,20.);
      if (isInAWideTPC)
      {
        //std::cout << "   X,Y,Z:    " << std::setw(12) <<mcPart->Position(iPoint).X() <<", " << std::setw(12)<<mcPart->Position(iPoint).Y()<<", " << std::setw(12)<<mcPart->Position(iPoint).Z()<<", "<< std::endl;
        auto vec3 = mcPart->Position(iPoint).Vect();
        _minMaxFinderTrajX.addPoint(mcPart->Position(iPoint).X());
        _minMaxFinderTrajY.addPoint(mcPart->Position(iPoint).Y());
        _minMaxFinderTrajZ.addPoint(mcPart->Position(iPoint).Z());
        _minMaxFinderTrajT.addPoint(mcPart->Position(iPoint).T());
      }
      if (_writeTrajectoryInfo)
      {
        _trajx.push_back(mcPart->Position(iPoint).X());
        _trajy.push_back(mcPart->Position(iPoint).Y());
        _trajz.push_back(mcPart->Position(iPoint).Z());
        _trajt.push_back(mcPart->Position(iPoint).T());
        _trajp.push_back(mcPart->Momentum(iPoint).P());
        _trajE.push_back(mcPart->Momentum(iPoint).E());
        _trajInTPC.push_back(isInATPC);
        _trajInWideTPC.push_back(isInAWideTPC);
        if (iPoint > 0)
        {
          //float pathLength = (vec3-mcPart->Position().Vect()).Mag();
          //float energyDiff = mcPart->Momentum(iPoint).E()-mcPart->Momentum().E();

          float dE = mcPart->Momentum(iPoint).E() - mcPart->Momentum(iPoint-1).E();
          float dx = (mcPart->Position(iPoint).Vect() - mcPart->Position(iPoint-1).Vect()).Mag();
          float mdEodx = - dE/dx;
          //std::cout << "     dE:    " << std::setw(12) <<dE <<" dx: " << std::setw(12)<<dx<<" -dE/dl " << std::setw(12)<<mdEodx<< std::endl;
          _trajdEdx.push_back(mdEodx);
        }
        else
        {
          _trajdEdx.push_back(nanf(""));
        }
      } // if _writeTrajectoryInfo
    } // for iPoint

    if (_writeIDEInfo)
    {
      // Look at IDE points
      int trackid = mcPart->TrackId();
      _numberIDEs = 0;
      for (const auto& simChan : simChanVec)
      {
        const auto & tdcidemap = simChan->TDCIDEMap();
        for(auto& tdcidepair : tdcidemap)
        {
          //auto tdc = tdcidepair.first;
          auto ides = tdcidepair.second;
          //std::cout << "tdc: " << tdc << ", ide: " << std::endl;
          for (const auto& ide : ides)
          {
            if (ide.trackID == trackid)
            {
              _numberIDEs++;
              _idex.push_back(ide.x);
              _idey.push_back(ide.y);
              _idez.push_back(ide.z);
              //std::cout << "  x,y,z" << ide.x <<", " << ide.y << ", "<< ide.z << std::endl;
            }
          }
        }
        //simChan->Dump(std::cout);
        //std::cout << std::endl;
      } // for simChanVec
    } // if _writeIDEInfo

  } // for mcPartVec

  //for (const auto& simChan : simChanVec)
  //{
  //  const std::map< unsigned short, std::vector< sim::IDE > > & tdcidemap = simChan->TDCIDEMap();
  //  for(auto& tdcidepair : tdcidemap)
  //  {
  //    //auto tdc = tdcidepair.first;
  //    auto ides = tdcidepair.second;
  //    //std::cout << "tdc: " << tdc << ", ide: " << std::endl;
  //    for (const auto& ide : ides)
  //    {
  //      //std::cout << "  x,y,z" << ide.x <<", " << ide.y << ", "<< ide.z << std::endl;
  //    }
  //  }
  //  //simChan->Dump(std::cout);
  //  //std::cout << std::endl;
  //} // for simChanVec

  //for (const auto& auxDetSimChan : auxDetSimChanVec)
  //{
  //  std::vector< sim::AuxDetIDE > const & auxDetIDEs = auxDetSimChan->AuxDetIDEs();
  //  for(const sim::AuxDetIDE& ide : auxDetIDEs)
  //  {
  //    std::cout << "auxDetIDE:\n";
  //    std::cout << "  entry x,y,z: " << ide.entryX << ", " << ide.entryZ << ", " << ide.entryZ << std::endl;
  //    std::cout << "  exit  x,y,z: " << ide.exitX << ", " << ide.exitZ << ", " << ide.exitZ << std::endl;
  //  }

  //} // for auxDetSimChanVec

  _outtree->Fill();
  
}

void dune::MuonTaggerTreeMaker::endJob()
{
  std::cout << "trajectory x in: "<< _minMaxFinderTrajX.getMin() << ", " << _minMaxFinderTrajX.getMax() << std::endl;
  std::cout << "trajectory y in: "<< _minMaxFinderTrajY.getMin() << ", " << _minMaxFinderTrajY.getMax() << std::endl;
  std::cout << "trajectory z in: "<< _minMaxFinderTrajZ.getMin() << ", " << _minMaxFinderTrajZ.getMax() << std::endl;
  std::cout << "trajectory t in: "<< _minMaxFinderTrajT.getMin() << ", " << _minMaxFinderTrajT.getMax() << std::endl;

  std::cout << std::endl;
  std::cout << "x trajectory begin in: "<< _minMaxFinderXb.getMin() << ", " << _minMaxFinderXb.getMax() << std::endl;
  std::cout << "y trajectory begin in: "<< _minMaxFinderYb.getMin() << ", " << _minMaxFinderYb.getMax() << std::endl;
  std::cout << "z trajectory begin in: "<< _minMaxFinderZb.getMin() << ", " << _minMaxFinderZb.getMax() << std::endl;
}

bool dune::MuonTaggerTreeMaker::hitsDetectorPlane(const simb::MCParticle& part, bool backDetector) // if false, front detector
{
//  std::cout << "hitsDetectorPlane starting ";
  if (backDetector)
  {
//    std::cout << "on back detector..." << std::endl;
  }
  else
  {
//    std::cout << "on front detector..." << std::endl;
  }
  float zdet = _frontDetectorZ;
  if (backDetector)
    zdet = _backDetectorZ;

  const simb::MCTrajectory& traj = part.Trajectory();
  const unsigned nTrajPoints = traj.size();
  float beginZ = traj.Z(0);
  float endZ = traj.Z(nTrajPoints - 1);
  bool backwards = false;
  if (beginZ > endZ)
  {
//    std::cout << "trajectory is backwards " << std::endl;
    backwards = true;
  }
  // Check that pass through detector
  if (backwards)
  {
    if(endZ > zdet || beginZ < zdet)
    {
//        std::cout << "trajectory does not cross zdet: " << zdet << " beginZ: " << beginZ << " endZ: " << endZ << std::endl;
        return false;
    }
  }
  else // forwards
  {
    if(beginZ > zdet || endZ < zdet)
    {
//        std::cout << "trajectory does not cross zdet: " << zdet << " beginZ: " << beginZ << " endZ: " << endZ << std::endl;
        return false;
    }
  }
//  std::cout << "trajectory does cross zdet: " << zdet << " beginZ: " << beginZ << " endZ: " << endZ << std::endl;
  // find iPoint where cross detector in z
  unsigned iCrossZ = -1;
  unsigned iCrossZLast = -1;
  for(unsigned iPoint = 1; iPoint < nTrajPoints; iPoint++)
  {
    float z = traj.Z(iPoint);
    float zLast = traj.Z(iPoint-1);
    if(backwards)
    {
      if(zLast > zdet && z < zdet)
      {
        iCrossZ = iPoint;
        iCrossZLast = iPoint-1;
      }
    }
    else // forwards
    {
      if(z > zdet && zLast < zdet)
      {
        iCrossZ = iPoint;
        iCrossZLast = iPoint-1;
      }
    } // else
  } // for iPoint
//  std::cout << "iCrossZ : " << iCrossZ<< "   "<< traj.Z(iCrossZ) << " iCrossZLast: " << iCrossZLast<< "   "<< traj.Z(iCrossZLast) << std::endl;
  if (iCrossZ > 0 && iCrossZLast > 0)
  {
    float xMinDet = _frontDetectorXmin;
    float xMaxDet = _frontDetectorXmax;
    float yMinDet = _frontDetectorYmin;
    float yMaxDet = _frontDetectorYmax;
    if (backDetector)
    {
      xMinDet = _backDetectorXmin;
      xMaxDet = _backDetectorXmax;
      yMinDet = _backDetectorYmin;
      yMaxDet = _backDetectorYmax;
    }
    // Fuzzily say that we hit the detector if either point is in the detector's x,y limits
    float x = traj.X(iCrossZ);
    float y = traj.Y(iCrossZ);
    if (xMinDet < x && xMaxDet > x && yMinDet < y && yMaxDet > y)
    {
 //     std::cout << "iPointZ ";
 //     std::cout << "x,y: " <<x << ", " << y << " where in the detector limits x: ("<<xMinDet << ", "<< xMaxDet<<") y: ("<< yMinDet<< ", " << yMaxDet<<")";
 //     std::cout << " Point Z: " << traj.Z(iCrossZ) << std::endl;
      return true;
    }
    x = traj.X(iCrossZLast);
    y = traj.Y(iCrossZLast);
    if (xMinDet < x && xMaxDet > x && yMinDet < y && yMaxDet > y)
    {
 //     std::cout << "iPointZLast ";
 //     std::cout << "x,y: " <<x << ", " << y << " where in the detector limits x: ("<<xMinDet << ", "<< xMaxDet<<") y: ("<< yMinDet<< ", " << yMaxDet<<")";
 //     std::cout << " Point Z: " << traj.Z(iCrossZLast) << std::endl;
      return true;
    }
//    x = traj.X(iCrossZ);
//    y = traj.Y(iCrossZ);
//    float z = traj.Z(iCrossZ);
//    std::cout << "Not in detector: x,y,z: " <<x << ", " << y << ", "<<z <<std::endl;
//    x = traj.X(iCrossZLast);
//    y = traj.Y(iCrossZLast);
//    z = traj.Z(iCrossZLast);
//    std::cout << "Not in detector: x,y,z: " <<x << ", " << y << ", "<<z <<std::endl;
//    std::cout << " where in the detector limits x: ("<<xMinDet << ", "<< xMaxDet<<") y: ("<< yMinDet<< ", " << yMaxDet<<")" << std::endl;
    return false;
  }
  else
  {
    std::cout << "Error: Could not find where trajectory crosses detector in Z" << std::endl;
    return false;
  }
}

DEFINE_ART_MODULE(dune::MuonTaggerTreeMaker)
