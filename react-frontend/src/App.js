import React from 'react';
import { GoogleMap, withScriptjs, withGoogleMap, Marker} from 'react-google-maps';


class Map extends React.Component{ 
  constructor(props){
    super(props)
    this.state = {
      vehicle_collission: 0,
      subway_entrances: 0,
      health_services: 0,
      police_misconduct_reports : 0,
      response : ""

    }
  }

  handleChange(evt){
    this.setState({
        [evt.target.name] : evt.target.value
        
    })
 }

  handleSubmit(event){
    fetch(`http://ec2-52-91-13-65.compute-1.amazonaws.com:9000/buildings?vehicle_collission=${this.state.vehicle_collission}&subway_entrances=${this.state.subway_entrances}&health_services=${this.state.health_services}`)
        .then( res=> res.json())
        .then(res=> this.setState({response: res}))
        .catch(err=>err);
    event.preventDefault();
}
  render(){
    let placemarks;
    let apiResponse = this.state.response;
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

class Query extends React.Component{
  constructor(props){
      super(props)
      this.state = { 
          collission_query_type : 'precise',
          entrances_query_type : 'precise',
          health_services_query_type : 'precise',
          police_misconduct_query_type : 'precise'
   }
  }

  
  render(){
      return(
          <div>
              <form onSubmit={Map.handleSubmit}>
                  <label>Vehicle Collissions
                      <input name="vehicle_collission" type="number" value={this.state.vehicle_collission} onChange={Map.handleChange}/>
                  </label>
                  <label>Subway Entrances
                      <input type="number" name="subway_entrances" value={this.state.subway_entrances} onChange={Map.handleChange}/>
                  </label>
                  <label>Mental Health Services
                      <input type="number" name="health_services" value={this.state.health_services} onChange={Map.handleChange}/>
                  </label>
{/*                     <label>Number of Police Misconduct Reports
                      <input type="number" name="police_misconduct_reports" value={this.state.police_misconduct_reports} onChange={this.props.handleChange}/>
                  </label> */}
              <input type="submit" value="Submit"/>
              </form>
              <div>{this.state.response}</div>

          </div>

      )
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