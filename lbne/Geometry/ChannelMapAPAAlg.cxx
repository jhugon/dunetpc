////////////////////////////////////////////////////////////////////////
/// \file  ChannelMapAPAAlg.cxx
/// \brief Interface to algorithm class for a specific detector channel mapping
///
/// \version $Id:  $
/// \author  tylerdalion@gmail.com
////////////////////////////////////////////////////////////////////////

#include "Geometry/ChannelMapAPAAlg.h"
#include "Geometry/CryostatGeo.h"
#include "Geometry/TPCGeo.h"
#include "Geometry/PlaneGeo.h"
#include "Geometry/WireGeo.h"

#include "art/Framework/Services/Registry/ServiceHandle.h"

namespace geo{


  //----------------------------------------------------------------------------
  // Define sort order for cryostats in APA configuration
  //   same as standard
  static bool sortCryoAPA(const CryostatGeo* c1, const CryostatGeo* c2)
  {
    double xyz1[3] = {0.}, xyz2[3] = {0.};
    double local[3] = {0.}; 
    c1->LocalToWorld(local, xyz1);
    c2->LocalToWorld(local, xyz2);

    return xyz1[0] < xyz2[0];   
  }


  //----------------------------------------------------------------------------
  // Define sort order for tpcs in APA configuration.
  static bool sortTPCAPA(const TPCGeo* t1, const TPCGeo* t2) 
  {
    double xyz1[3] = {0.};
    double xyz2[3] = {0.};
    double local[3] = {0.};
    t1->LocalToWorld(local, xyz1);
    t2->LocalToWorld(local, xyz2);

    // The goal is to number TPCs first in the x direction so that,
    // in the case of APA configuration, TPCs 2c and 2c+1 make up APA c.
    // then numbering will go in y then in z direction.

    // First sort all TPCs into same-z groups
     if(xyz1[2] < xyz2[2]) return true;
 
    // Within a same-z group, sort TPCs into same-y groups
     if(xyz1[2] == xyz2[2] && xyz1[1] < xyz2[1]) return true;
 
    // Within a same-z, same-y group, sort TPCs according to x
     if(xyz1[2] == xyz2[2] && xyz1[1] == xyz2[1] && xyz1[0] < xyz2[0]) return true;
 
    // none of those are true, so return false
     return false;
  }


  //----------------------------------------------------------------------------
  // Define sort order for planes in APA configuration
  //   same as standard, but implemented differently
  static bool sortPlaneAPA(const PlaneGeo* p1, const PlaneGeo* p2) 
  {
    double xyz1[3] = {0.};
    double xyz2[3] = {0.};
    double local[3] = {0.};
    p1->LocalToWorld(local, xyz1);
    p2->LocalToWorld(local, xyz2);

    return xyz1[0] > xyz2[0];
  }


  //----------------------------------------------------------------------------
  bool sortWireAPA(WireGeo* w1, WireGeo* w2){
    double xyz1[3] = {0.};
    double xyz2[3] = {0.};

    w1->GetCenter(xyz1); w2->GetCenter(xyz2);

    // we want the wires to be sorted such that the smallest corner wire
    // on the readout end of a plane is wire zero, with wire number
    // increasing away from that wire. 

    // if a bottom TPC, count from bottom up
    if( xyz1[1]<0 && xyz1[1] < xyz2[1] ) return true; 

    // if a top TPC, count from top down
    if( xyz1[1]>0 && xyz1[1] > xyz2[1] ) return true;

    // sort the vertical wires to always increase in z direction
    if( xyz1[1] == xyz2[1] && xyz1[2] < xyz2[2] ) return true;

    return false;
  }


  //----------------------------------------------------------------------------
  ChannelMapAPAAlg::ChannelMapAPAAlg()
  {
  }

  //----------------------------------------------------------------------------
  ChannelMapAPAAlg::~ChannelMapAPAAlg()
  {
  }

  //----------------------------------------------------------------------------
  void ChannelMapAPAAlg::Initialize(std::vector<geo::CryostatGeo*> & cgeo)
  {

    if(!fFirstChannelInThisPlane.empty() || !fFirstChannelInNextPlane.empty())
      {
	this->Uninitialize();
	std::cout << "FirstChannel vectors are not empty." << std::endl;
	std::cout << "FirstChannel vectors have been emptied." <<     std::endl;
      }


    fNcryostat = cgeo.size();
    
    mf::LogInfo("ChannelMapAPAAlg") << "Initializing...";

    std::sort(cgeo.begin(), cgeo.end(), sortCryoAPA);
    for(size_t c = 0; c < cgeo.size(); ++c) 
      cgeo[c]->SortSubVolumes(sortTPCAPA, sortPlaneAPA, sortWireAPA);
      
    fNTPC.resize(fNcryostat);
    fAPAs.resize(fNcryostat);
    fFirstChannelInNextPlane.resize(1);  // Change 1 to Ncryostat if you want
    fFirstChannelInThisPlane.resize(1);  // to treat each APA uniquely,and do
					 // the same with the other resizes.
    fPlanesPerAPA = cgeo[0]->TPC(0).Nplanes();
    nAnchoredWires.resize(fPlanesPerAPA);
    fWiresInPlane.resize(fPlanesPerAPA);
    fFirstChannelInThisPlane[0].resize(1);  // remember FirstChannel vectors
    fFirstChannelInNextPlane[0].resize(1);  // for first APA only.
    fFirstChannelInThisPlane[0][0].resize(fPlanesPerAPA);  // Make room for info
    fFirstChannelInNextPlane[0][0].resize(fPlanesPerAPA);  // on each plane.

    fTopChannel = 0;

    // Size some vectors and initialize the FirstChannel vectors.
    // If making FirstChannel's for every APA uniquely, they also
    // need to be sized here. Not necessary for now
    for(unsigned int cs = 0; cs != fNcryostat; ++cs){
      
      fNTPC[cs] = cgeo[cs]->NTPC();

      fAPAs[cs].resize(fNTPC[cs]/2);


      for(unsigned int APACount = 0; APACount != fNTPC[cs]/2; ++APACount){
	
	fAPAs[cs][APACount].resize(2); 		  // Two TPCs per APA always.
	fAPAs[cs][APACount][0] = 2*APACount;	  // This is related to how
	fAPAs[cs][APACount][1] = 2*APACount + 1;  // tpc_sort is defined.

	// Note: see tpc_sort and you will see that
	// TPCs 2x and 2x+1 form APA x.

      }// end sizing loop over APAs
    }// end sizing loop over cryostats

    // Find the number of wires anchored to the frame
    for(unsigned int p=0; p!=fPlanesPerAPA; ++p){

      fWiresInPlane[p] = cgeo[0]->TPC(0).Plane(p).Nwires();
      double xyz[3] = {0.};
      double xyz_next[3] = {0.};

      for(unsigned int w=0; w!=fWiresInPlane[p]; ++w){

	// for vertical planes
	if(cgeo[0]->TPC(0).Plane(p).View()==kW)   { 
	  nAnchoredWires[p] = fWiresInPlane[p];      
	  break;
	}

	cgeo[0]->TPC(0).Plane(p).Wire(w).GetCenter(xyz);
	cgeo[0]->TPC(0).Plane(p).Wire(w+1).GetCenter(xyz_next);

	if(xyz[2]==xyz_next[2]){
	  nAnchoredWires[p] = w-1;      
	  break;
	}
      }// end wire loop

    }// end plane loop

    static unsigned int CurrentChannel = 0;
   
    for(unsigned int PCount = 0; PCount != fPlanesPerAPA; ++PCount){

      fFirstChannelInThisPlane[0][0][PCount] = CurrentChannel;
      CurrentChannel = CurrentChannel + 2*nAnchoredWires[PCount];
      fFirstChannelInNextPlane[0][0][PCount] = CurrentChannel;

    }// end build loop over planes

    // Save the number of channels
    fChannelsPerAPA = fFirstChannelInNextPlane[0][0][fPlanesPerAPA-1];

    fNchannels = 0;
    for(size_t cs = 0; cs < fNcryostat; ++cs){
      fNchannels = fNchannels + fChannelsPerAPA*fNTPC[cs]/2;
    }

    //resize vectors
    fFirstWireCenterY.resize(fNcryostat);
    fFirstWireCenterZ.resize(fNcryostat);
    for (unsigned int cs=0; cs<fNcryostat; cs++){
      fFirstWireCenterY[cs].resize(cgeo[cs]->NTPC());
      fFirstWireCenterZ[cs].resize(cgeo[cs]->NTPC());
      for (unsigned int tpc=0; tpc<cgeo[cs]->NTPC(); tpc++){
        fFirstWireCenterY[cs][tpc].resize(cgeo[cs]->TPC(tpc).Nplanes());
        fFirstWireCenterZ[cs][tpc].resize(cgeo[cs]->TPC(tpc).Nplanes());
      }                                                                   
    }

    fWirePitch.resize(cgeo[0]->TPC(0).Nplanes());
    fOrientation.resize(cgeo[0]->TPC(0).Nplanes());
    fTanOrientation.resize(cgeo[0]->TPC(0).Nplanes());

    //save data into fFirstWireCenterY and fFirstWireCenterZ
    for (unsigned int cs=0; cs<fNcryostat; cs++){
      for (unsigned int tpc=0; tpc<cgeo[cs]->NTPC(); tpc++){
        for (unsigned int plane=0; plane<cgeo[cs]->TPC(tpc).Nplanes(); plane++){
          double xyz[3]={0.0, 0.0, 0.0};
          cgeo[cs]->TPC(tpc).Plane(plane).Wire(0).GetCenter(xyz);
          fFirstWireCenterY[cs][tpc][plane]=xyz[1];
          fFirstWireCenterZ[cs][tpc][plane]=xyz[2];
        }
      }
    }

    //initialize fWirePitch and fOrientation
    for (unsigned int plane=0; plane<cgeo[0]->TPC(0).Nplanes(); plane++){
        fWirePitch[plane]=cgeo[0]->TPC(0).WirePitch(0,1,plane);
        fOrientation[plane]=cgeo[0]->TPC(0).Plane(plane).Wire(0).ThetaZ();
        fTanOrientation[plane] = tan(fOrientation[plane]);
    }


    mf::LogVerbatim("GeometryTest") << "fNchannels = " << fNchannels ; 

    mf::LogVerbatim("GeometryTest") << "For all identical APA:" ; 
    mf::LogVerbatim("GeometryTest") << "fChannelsPerAPA = " << fChannelsPerAPA ; 

    mf::LogVerbatim("GeometryTest") << "Wires in Plane 0 = " << fWiresInPlane[0] ;
    mf::LogVerbatim("GeometryTest") << "Wires in Plane 1 = " << fWiresInPlane[1] ;
    mf::LogVerbatim("GeometryTest") << "Wires in Plane 2 = " << fWiresInPlane[2] ;

    mf::LogVerbatim("GeometryTest") << "Anchored Wires in Plane 0 = " << nAnchoredWires[0] ;
    mf::LogVerbatim("GeometryTest") << "Anchored Wires in Plane 1 = " << nAnchoredWires[1] ;
    mf::LogVerbatim("GeometryTest") << "Anchored Wires in Plane 2 = " << nAnchoredWires[2] ;

    mf::LogVerbatim("GeometryTest") << "FirstChannelInThisPlane[0][0][0] = " 
				    << fFirstChannelInThisPlane[0][0][0] ;
    mf::LogVerbatim("GeometryTest") << "FirstChannelInThisPlane[0][0][1] = " 
				    << fFirstChannelInThisPlane[0][0][1] ;
    mf::LogVerbatim("GeometryTest") << "FirstChannelInThisPlane[0][0][2] = " 
				    << fFirstChannelInThisPlane[0][0][2] ;

    mf::LogVerbatim("GeometryTest") << "FirstChannelInNextPlane[0][0][0] = " 
                                    << fFirstChannelInNextPlane[0][0][0] ;
    mf::LogVerbatim("GeometryTest") << "FirstChannelInNextPlane[0][0][1] = "   
  	                            << fFirstChannelInNextPlane[0][0][1] ;
    mf::LogVerbatim("GeometryTest") << "FirstChannelInNextPlane[0][0][2] = "   
                                    << fFirstChannelInNextPlane[0][0][2] ;

    mf::LogVerbatim("GeometryTest") << "Pitch in Plane 0 = " << fWirePitch[0] ;
    mf::LogVerbatim("GeometryTest") << "Pitch in Plane 1 = " << fWirePitch[1] ;
    mf::LogVerbatim("GeometryTest") << "Pitch in Plane 2 = " << fWirePitch[2] ;

    return;

  }
   
  //----------------------------------------------------------------------------
  void ChannelMapAPAAlg::Uninitialize()
  {

      std::vector< std::vector<std::vector<unsigned int> > >().swap(fFirstChannelInThisPlane);
      std::vector< std::vector<std::vector<unsigned int> > >().swap(fFirstChannelInNextPlane);

  }

  //----------------------------------------------------------------------------
  std::vector<geo::WireID> ChannelMapAPAAlg::ChannelToWire(unsigned int channel)  const
  {

    // first check if this channel ID is legal
    if(channel >= fNchannels )
       throw cet::exception("Geometry") << "ILLEGAL CHANNEL ID for channel " << channel;

    std::vector< WireID > AllSegments;
    
    static unsigned int cstat;
    static unsigned int tpc;
    static unsigned int plane;
    static unsigned int wireThisPlane;
    static unsigned int NextPlane;
    static unsigned int ThisPlane;
    
    for(unsigned int csloop = 0; csloop != fNcryostat; ++csloop){
      
      bool breakVariable = false;
      
      for(unsigned int apaloop = 0; apaloop != fAPAs[csloop].size(); ++apaloop){
	for(unsigned int planeloop = 0; planeloop != fPlanesPerAPA; ++planeloop){
	  
	  NextPlane = (fFirstChannelInNextPlane[0][0][planeloop] 
		       + apaloop*fChannelsPerAPA
		       + csloop*(fAPAs[csloop].size())*fChannelsPerAPA);
	  
	  ThisPlane = (fFirstChannelInThisPlane[0][0][planeloop]
		       + apaloop*fChannelsPerAPA
		       + csloop*(fAPAs[csloop].size())*fChannelsPerAPA);
	  
	  if(channel < NextPlane){
	    
	    cstat = csloop;
	    tpc   = 2*apaloop;
	    plane = planeloop;
	    wireThisPlane  = channel - ThisPlane;
	    
	    breakVariable = true;
	    break;
	  }// end if break
	  
	  if(breakVariable) break;
	  
	}// end plane loop
	
	if(breakVariable) break;
	
      }// end apa loop
      
      if(breakVariable) break;
      
    }// end cryostat loop
    

    int WrapDirection = 1; // go from tpc to (tpc+1) or tpc to (tpc-1)

    // find the lowest wire
    unsigned int ChannelGroup = std::floor( wireThisPlane/nAnchoredWires[plane] );
    unsigned int bottomwire = wireThisPlane-ChannelGroup*nAnchoredWires[plane];
    
    if(ChannelGroup%2==1){
      tpc += 1;
      WrapDirection  = -1;	 
    }
    
    for(unsigned int WireSegmentCount = 0; WireSegmentCount != 50; ++WireSegmentCount){
      
      tpc += WrapDirection*(WireSegmentCount%2);
      
      geo::WireID CodeWire(cstat, tpc, plane, bottomwire + WireSegmentCount*nAnchoredWires[plane]);
      
      AllSegments.push_back(CodeWire);
      
      // reset the tcp variable so it doesnt "accumulate value"
      tpc -= WrapDirection*(WireSegmentCount%2);
      
      if( bottomwire + (WireSegmentCount+1)*nAnchoredWires[plane] > fWiresInPlane[plane]-1) break;
      
    } //end WireSegmentCount loop
    
    
    return AllSegments;
  }


  //----------------------------------------------------------------------------
  unsigned int ChannelMapAPAAlg::Nchannels() const
  {
    return fNchannels;
  }
  

  //----------------------------------------------------------------------------
  unsigned int    ChannelMapAPAAlg::NearestWire(const TVector3& xyz,
                                         unsigned int    plane,
                                         unsigned int    tpc,
                                         unsigned int    cryostat)     const
  {

    //get the position of first wire in a given cryostat, tpc and plane
    double firstxyz[3]={0.0, 0.0, 0.0};
    firstxyz[1]=fFirstWireCenterY[cryostat][tpc][plane];
    firstxyz[2]=fFirstWireCenterZ[cryostat][tpc][plane];

    //get the orientation angle of a given plane and calculate the distance between first wire
    //and a point projected in the plane
    int rotate = 1;
    if (tpc%2 == 1) rotate = -1;
    double distance = std::abs(xyz[1]-firstxyz[1]-rotate*tan(fOrientation[plane])*xyz[2]
			   +   rotate*fTanOrientation[plane]*firstxyz[2])/
                               sqrt(fTanOrientation[plane]*fTanOrientation[plane]+1);
    
    //by dividing distance by wirepitch and given that wires are sorted in increasing order,
    //then the wire that is closest to a given point can be calculated
    unsigned int iwire=int(distance/fWirePitch[plane]);

    //if the distance between the wire and a given point is greater than the half of wirepitch,
    //then the point is closer to a i+1 wire thus add one
    double res = distance/fWirePitch[plane] - int( distance/fWirePitch[plane] );
    if (res > fWirePitch[plane]/2)	iwire+=1;

    return iwire;

  }
  
  //----------------------------------------------------------------------------
  unsigned int ChannelMapAPAAlg::PlaneWireToChannel(unsigned int plane,
							 unsigned int wire,
							 unsigned int tpc,
							 unsigned int cstat) const
  {
    unsigned int OtherSideWires = 0;

    unsigned int Channel = fFirstChannelInThisPlane[0][0][plane]; // start in very first APA.
    Channel += cstat*(fAPAs[cstat].size())*fChannelsPerAPA;       // move channel to proper cstat.
    Channel += std::floor( tpc/2 )*fChannelsPerAPA;		  // move channel to proper APA.
    OtherSideWires += (tpc%2)*nAnchoredWires[plane];	          // get number of wires on the first
								  // side of the APA if starting
								  // on the other side TPC.


    // Lastly, account for the fact that channel number while moving up wire number in one
    // plane resets after 2 times the number of wires anchored -- one for each APA side.
    // At the same time, OtherSideWires accounts for the fact that if a channel starts on 
    // the other side, it is offset by the number of wires on the first side.
    Channel += (OtherSideWires + wire)%(2*nAnchoredWires[plane]);
    
    return Channel;

  }

  //----------------------------------------------------------------------------
  const SigType_t ChannelMapAPAAlg::SignalType( unsigned int const channel )  const
  {
    unsigned int chan = channel % fChannelsPerAPA;
    SigType_t sigt;

    if(       chan <  fFirstChannelInThisPlane[0][0][2]     ){ sigt = kInduction;  }
    else if( (chan >= fFirstChannelInThisPlane[0][0][2]) &&
             (chan <  fFirstChannelInNextPlane[0][0][2])    ){ sigt = kCollection; }
    else{    mf::LogWarning("BadChannelSignalType") << "Channel " << channel 
	     << " (" << chan << ") not given signal type." << std::endl;         }
  
    return sigt;
  }

  //----------------------------------------------------------------------------
  const View_t ChannelMapAPAAlg::View( unsigned int const channel )  const
  {
    unsigned int chan = channel % fChannelsPerAPA;
    View_t view;

    if(       chan <  fFirstChannelInNextPlane[0][0][0]     ){ view = kU; }
    else if( (chan >= fFirstChannelInThisPlane[0][0][1]) &&
             (chan <  fFirstChannelInNextPlane[0][0][1])    ){ view = kV; }
    else if( (chan >= fFirstChannelInThisPlane[0][0][2]) &&
             (chan <  fFirstChannelInNextPlane[0][0][2])    ){ view = kW; }
    else{    mf::LogWarning("BadChannelViewType") << "Channel " << channel 
             << " (" << chan << ") not given view type." << std::endl;  }
    
    return view;
  }  


} // namespace
