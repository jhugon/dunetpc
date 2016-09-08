// StandardAdcWireBuildingService_service.cc

#include "StandardAdcWireBuildingService.h"
#include <iostream>
#include <sstream>
#include <iomanip>
#include "art/Framework/Services/Registry/ServiceHandle.h"
#include "lardata/RecoBaseArt/WireCreator.h"

using std::vector;
using std::string;
using std::ostream;
using std::cout;
using std::endl;
using std::setw;
using art::ServiceHandle;

//**********************************************************************

StandardAdcWireBuildingService::
StandardAdcWireBuildingService(fhicl::ParameterSet const& pset, art::ActivityRegistry&)
: m_LogLevel(1) {
  const string myname = "StandardAdcWireBuildingService::ctor: ";
  pset.get_if_present<int>("LogLevel", m_LogLevel);
  if ( m_LogLevel > 0 ) print(cout, myname);
}


//**********************************************************************

int StandardAdcWireBuildingService::build(AdcChannelData& data, WireVector* pwires) const {
  const string myname = "StandardAdcWireBuildingService:build: ";
  if ( m_LogLevel >= 2 ) cout << myname << "Building recob::Wire for channel "
                              << data.channel << "." << endl;
  if ( data.wire != nullptr ) {
    cout << myname << "WARNING: Wire already exists for channel " << data.channel
                   << ". No action taken." << endl;
    return 1;
  }
  if ( data.digit == nullptr ) {
    cout << myname << "WARNING: No digit is specified for channel " << data.channel
                   << ". No action taken." << endl;
    return 2;
  }
  if ( data.digit->Channel() != data.channel ) {
    cout << myname << "WARNING: Input data channel differs from digit: " << data.channel
         << " != " << data.digit->Channel() << ". No action taken." << endl;
    return 3;
  }
  if ( m_LogLevel >= 2 ) {
    cout << myname << "  Channel " << data.channel << " has " << data.rois.size() << " ROI"
         << (data.rois.size()==1 ? "" : "s") << "." << endl;
  }
  // Create recob ROIs.
  recob::Wire::RegionsOfInterest_t recobRois;
  for ( const AdcRoi& roi : data.rois ) {
    AdcSignalVector sigs;
    for ( unsigned int isig=roi.first; isig<=roi.second; ++isig ) {
      sigs.push_back(data.samples[isig]);
    }
    recobRois.add_range(roi.first, std::move(sigs));
  }
  // Create recob::Wire.
  recob::WireCreator wc(std::move(recobRois), *data.digit);
  // Record the new wire if there is a wire container and if there is at least one ROI.
  bool dataOwnsWire = (pwires == nullptr) || (data.rois.size() == 0);
  if ( ! dataOwnsWire ) {
    if ( pwires->size() == pwires->capacity() ) {
      cout << myname << "ERROR: Wire vector capacity " << pwires->capacity()
           << " is too small. Wire is not recorded." << endl;
      dataOwnsWire = true;
    } else {
      data.wireIndex = pwires->size();
      pwires->push_back(wc.move());
      data.wire = &pwires->back();
      if ( m_LogLevel >= 3 )
        cout << myname << "  Channel " << data.channel << " ROIs stored in container." << endl;
    }
  }
  if ( dataOwnsWire ) {
    data.wire = new recob::Wire(wc.move());
  }
  return 0;
}

//**********************************************************************

ostream& StandardAdcWireBuildingService::
print(ostream& out, string prefix) const {
  out << prefix << "StandardAdcWireBuildingService:" << endl;
  out << prefix << "    LogLevel: " << m_LogLevel << endl;
  return out;
}

//**********************************************************************

DEFINE_ART_SERVICE_INTERFACE_IMPL(StandardAdcWireBuildingService, AdcWireBuildingService)

//**********************************************************************
