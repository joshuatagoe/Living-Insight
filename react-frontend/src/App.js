import React from 'react';
import {  withScriptjs, withGoogleMap} from 'react-google-maps';
import Map from './Map';
import Query from './Query'
import DetailedData from './DetailedData'
import './App.css'
class App extends React.Component{

  constructor(props){
    super(props)
    this.state = {
      police_misconduct_reports : 0,
      response : "",
      selectedHouse: null,
      renderMHVCSubway : false,
      mh_placemarks : null,
      vc_placemarks: null,
      subway_placemarks: null,

    }
    this.handleSubmit = this.handleSubmit.bind(this)
    this.setSelectedHouse = this.setSelectedHouse.bind(this)
    this.fetch_vehicle_data = this.fetch_vehicle_data.bind(this)
    this.fetch_mental_health = this.fetch_mental_health.bind(this)
    this.fetch_subway_entrances = this.fetch_subway_entrances.bind(this)
    this.fetch_detail_placemarks = this.fetch_detail_placemarks.bind(this)
  }

  fetch_detail_placemarks(){
    this.fetch_vehicle_data();
    this.fetch_mental_health();
    this.fetch_subway_entrances();

  }

  fetch_vehicle_data(){
    let url = `http://ec2-52-91-13-65.compute-1.amazonaws.com:9000/get_incidents?house_id='${this.state.selectedHouse.house_id}'`;
    fetch(url)
        .then( res=> res.json())
        .then(res=> this.setState({vc_placemarks: res}))
        .catch(err=>err);

}

fetch_mental_health(){
    let url = `http://ec2-52-91-13-65.compute-1.amazonaws.com:9000/get_health_services?house_id='${this.state.selectedHouse.house_id}'`;
    fetch(url)
        .then( res=> res.json())
        .then(res=> this.setState({mh_placemarks : res}))
        .catch(err=>err);

}

fetch_subway_entrances(){
  let url = `http://ec2-52-91-13-65.compute-1.amazonaws.com:9000/get_subway_entrances?house_id='${this.state.selectedHouse.house_id}'`;
  fetch(url)
      .then( res=> res.json())
      .then(res=> this.setState({subway_placemarks : res}))
      .catch(err=>err);

}

  
setSelectedHouse(building){
    this.setState({selectedHouse:building,
    renderMHVCSubway: true})
}

  


  handleSubmit(vehicle_collission1, vehicle_collission2, subway_entrances1, subway_entrances2, health_services1, health_services2, crimes1, crimes2){
    let url = `http://ec2-52-91-13-65.compute-1.amazonaws.com:9000/getbuildings?vehicle_collission1=${vehicle_collission1}&subway_entrances1=${subway_entrances1}&health_services1=${health_services1}&vehicle_collission2=${vehicle_collission2}&subway_entrances2=${subway_entrances2}&health_services2=${health_services2}&crimes1=${crimes1}&crimes2=${crimes2}`
    fetch(url)
        .then( res=> res.json())
        .then(res=> this.setState({response: res}))
        .catch(err=>err);
}


  render(){
    const WrappedMap = withScriptjs(withGoogleMap(Map));
    return(

        <div>{!this.state.selectedHouse && <Query setSelectedHouse={this.setSelectedHouse} response={this.state.response} handleChange={this.handleChange} handleSubmit={this.handleSubmit} />}<div style={{ width: "100vw", height: "100vh"}}>
            <WrappedMap 
            googleMapURL={`https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=${
              process.env.REACT_APP_GOOGLE_KEY
          }`} 
            loadingElement = { <div style={{height: "100%"}}/>}
            containerElement = { <div style={{height: "100%"}}/>}
            mapElement =  { <div style={{height: "100%"}}/>} 
            response={this.state.response}
            selectHouse={this.setSelectedHouse}
            render_detail_placemarks={this.state.renderMHVCSubway}
            mh_placemarks={this.state.mh_placemarks}
            vc_placemarks={this.state.vc_placemarks}
            subway_placemarks={this.state.subway_placemarks}
            selectedHouse = {this.state.selectedHouse}
            
            />
            {this.state.selectedHouse && <DetailedData getData={this.fetch_detail_placemarks} house={this.state.selectedHouse}></DetailedData>}
          </div>
        </div> 
    )

  }

}


export default App