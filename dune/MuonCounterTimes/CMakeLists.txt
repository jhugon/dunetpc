
simple_plugin(MuonCounterTimes "module"
			lardataobj_RawData
                        lardataobj_RecoBase
	                larcore_Geometry
	                larcore_Geometry_Geometry_service
                        lardata_Utilities    
			
			  
   lbne-raw-data_Overlays
   lbne_daqinput35t_utilities
   lbne_daqinput35t
                        ${ART_FRAMEWORK_CORE}
			${ART_FRAMEWORK_PRINCIPAL}
			${ART_FRAMEWORK_SERVICES_REGISTRY}
			${ART_FRAMEWORK_SERVICES_OPTIONAL}
			${ART_FRAMEWORK_SERVICES_OPTIONAL_TFILESERVICE_SERVICE}
			art_Persistency_Common canvas_Persistency_Common
			art_Persistency_Provenance canvas_Persistency_Provenance
			art_Utilities canvas_Utilities
			${MF_MESSAGELOGGER}
			${MF_UTILITIES}
	                ${FHICLCPP}
			${CETLIB}
                        ${ROOT_GEOM}
                        ${ROOT_XMLIO}
                        ${ROOT_GDML}
			${ROOT_BASIC_LIB_LIST}
              BASENAME_ONLY
)

install_headers()
install_fhicl()
install_source()
