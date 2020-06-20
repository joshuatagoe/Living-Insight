import React from 'react';
import { GoogleMap, withScriptjs, withGoogleMap, Marker} from 'react-google-maps';


class Map extends React.Component{ 
  constructor(props){
    super(props)
  }

  render(){
    let placemarks;
    let apiResponse = this.props.response;
    if(apiResponse.length>0){
      placemarks = apiResponse.map((building)=>(
        <Marker key={building.house_id} position={{lat:building.latitude, lng: building.longitude}}/>
        ))
    }
    return <GoogleMap 
    defaultZoom = {11} 
    defaultCenter = {{ lat : 40.7128, lng: -74.0060 }} 
    >
      {placemarks}
    </GoogleMap>

  }

}

export default Map;