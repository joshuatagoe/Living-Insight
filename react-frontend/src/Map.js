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
    let detail_placemarks_mh;
    let detail_placemarks_subway;
    let detail_placemarks_vc;
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
    if(this.props.mh_placemarks!=null){
      detail_placemarks_mh = this.props.mh_placemarks.map((building, index)=>(
        <Marker key={index} 
        position={{lat:building.latitude, lng: building.longitude}}
        icon={`http://maps.google.com/mapfiles/kml/shapes/lodging.png`}
        />

      ))
    }

      if(this.props.vc_placemarks!=null){
        detail_placemarks_mh = this.props.vc_placemarks.map((building, index)=>(
          <Marker key={index} 
          position={{lat:building.lat, lng: building.long}}
          icon={`http://maps.google.com/mapfiles/kml/shapes/earthquake.png`}
          />
  
        ))
      }

        if(this.props.subway_placemarks!=null){
          detail_placemarks_mh = this.props.subway_placemarks.map((building, index)=>(
            <Marker key={index} 
            position={{lat:building.lat, lng: building.long}}
            icon={`http://maps.google.com/mapfiles/kml/shapes/rail.png`}
            />
    
            
        ))
          }
        let zoom = 11;
        let center = { lat : 40.7128, lng: -74.00060}
        if(this.props.render_detail_placemarks){
          zoom = 13;
          center = { lat : this.props.selectedHouse.laatitude, lng: this.props.selectHouse.longitude }

        }

    return <GoogleMap 
    defaultZoom = {zoom} 
    defaultCenter = {center} 
    >
      {!this.props.render_detail_placemarks && placemarks}
      {this.props.render_detail_placemarks && detail_placemarks_mh && detail_placemarks_vc && detail_placemarks_subway}
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