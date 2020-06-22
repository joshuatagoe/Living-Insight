import React from 'react';
import { GoogleMap, withScriptjs, withGoogleMap, Marker, InfoWindow} from 'react-google-maps';


class Map extends React.Component{ 
  constructor(props){
    super(props)

    this.state = {
        hoveredhouse : null
    }

    this.setHoveredHouse = this.setHoveredHouse.bind(this)
  }

  setHoveredHouse(building){
      this.setState({hoveredhouse:building})
  }

  render(){
    let placemarks;
    let apiResponse = this.props.response;
    if(apiResponse.length>0){
      placemarks = apiResponse.map((building,index)=>(
        <Marker key={index} 
        position={{lat:building.latitude, lng: building.longitude}}
        onClick = {()=>{
            this.props.selectHouse(building);
        }}
        onMouseOver = {()=>{
          this.setHoveredHouse(building);
        }}
        onMouseLeave = {()=>{
          this.setHoveredHouse(null);
        }}
        icon={`https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_red${1+index}.png`}
        />
        ))
    }
    return <GoogleMap 
    defaultZoom = {11} 
    defaultCenter = {{ lat : 40.7128, lng: -74.0060 }} 
    >
      {placemarks}
      {this.state.hoveredhouse && (
          <InfoWindow
            position={{lat:this.state.hoveredhouse.latitude, lng: this.state.hoveredhouse.longitude}}
            onCloseClick = {()=>{
              this.setHoveredHouse(null);
            }}
          >
              <div>
                  <h1
                    onClick = {()=>{
                      this.props.selectHouse(this.state.hoveredhouse);
                    }}
                    style={{cursor:'pointer'}}
                  >
                    {this.state.hoveredhouse.house_id}
                  </h1>
                  <h2>{this.state.hoveredhouse.address}</h2>
                  <p>{this.state.hoveredhouse.rental_price}</p>

                  </div>
          </InfoWindow>
      )}
    </GoogleMap>

  }

}

export default Map;