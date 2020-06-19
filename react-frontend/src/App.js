import React from 'react';
import { GoogleMap, withScriptjs, withGoogleMap } from 'react-google-maps';
import Query from './Query'


class Map extends React.Component{ 
  constructor(props){
    this.placemarks = {};
  }

  handleSubmit(event){
    url = "http://ec2-52-91-13-65.compute-1.amazonaws.com:9000/buildings?vehicle_collission=${this.state.vehicle_collission}&subway_entrances=${this.state.subway_entrances}&health_services=${this.state.health_services}"
    fetch(url)
        .then( res=> res.json())
        .then(res=> this.setState({response: res}))
        .catch(err=>err);
    event.preventDefault();
}
  render(){
    return <GoogleMap 
    defaultZoom = {11} 
    defaultCenter = {{ lat : 40.7128, lng: -74.0060 }} 
    >
      {this.placemarks.map((building)=>(
      <Marker key={building.house_id} position={{lat:building.latitude, lng: building.longitude}}/>
      ))}
    </GoogleMap>

  }

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