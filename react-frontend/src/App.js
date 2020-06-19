import React from 'react';
import { GoogleMap, withScriptjs, withGoogleMap } from 'react-google-maps';
import Query from './Query'


function Map() { 
  return <GoogleMap 
  defaultZoom = {11} 
  defaultCenter = {{ lat : 40.7128, lng: -74.0060 }} 
  />
}

const WrappedMap = withScriptjs(withGoogleMap(Map));
export default function App(){
  
  return <div><Query/><div style={{ width: "100vw", height: "100vh"}}>
    <WrappedMap 
    googleMapURL={`https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=${
      process.env.REACT_APP_GOOGLE_KEY
  }`} 
    loadingElement = { <div style={{height: "100%"}}/>}
    containerElement = { <div style={{height: "100%"}}/>}
    mapElement =  { <div style={{height: "100%"}}/>}
    
    />
  </div>
  </div>
}