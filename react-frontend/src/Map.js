import React from 'react';
import { GoogleMap, Marker, InfoWindow} from 'react-google-maps';


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
        icon={{url:`http://maps.google.com/mapfiles/kml/shapes/lodging.png`, scaledSize: new window.google.maps.Size(15,15)}}
        />

      ))
    }

      if(this.props.vc_placemarks!=null){
        detail_placemarks_vc = this.props.vc_placemarks.map((building, index)=>(
          <Marker key={index} 
          position={{lat:building.lat, lng: building.long}}
          icon={{ url: `http://maps.google.com/mapfiles/kml/shapes/earthquake.png`, scaledSize: new window.google.maps.Size(15,15)}}
          />
  
        ))
      }

        if(this.props.subway_placemarks!=null){
          detail_placemarks_subway = this.props.subway_placemarks.map((building, index)=>(
            <Marker key={index} 
            position={{lat:building.lat, lng: building.long}}
            icon={{ url:`http://maps.google.com/mapfiles/kml/shapes/rail.png`, scaledSize: new window.google.maps.Size(15,15)}}
            />
    
            
        ))
          }
        let zoom = 11;
        let center = { lat : 40.7128, lng: -74.00060}
        let curr;
        if(this.props.render_detail_placemarks){
          zoom = 13;
          center = { lat : this.props.selectedHouse.latitude, lng: this.props.selectedHouse.longitude }
          curr = <Marker position={{lat:this.props.selectedHouse.latitude, lng:this.props.selectedHouse.longitude}}/>

        }

    return <GoogleMap 
    defaultZoom = {zoom}
    defaultCenter = {center} 
    >
      {this.props.render_detail_placemarks && curr}
      {this.props.render_detail_placemarks && detail_placemarks_mh}
      {this.props.render_detail_placemarks && detail_placemarks_vc}
      {this.props.render_detail_placemarks && detail_placemarks_subway}
      {!this.props.render_detail_placemarks && placemarks}
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