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
      vehicle_collission1: 0,
      subway_entrances1: 0,
      health_services1: 0,
      vehicle_collission2: 0,
      subway_entrances2: 0,
      health_services2: 0,
      police_misconduct_reports : 0,
      response : "",
      selectedHouse: null

    }
    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.setSelectedHouse = this.setSelectedHouse.bind(this)
  }


  
setSelectedHouse(building){
    this.setState({selectedHouse:building})
}

  
  handleChange(evt){
    this.setState({
        [evt.target.name] : evt.target.value
        
    })
 }

  handleSubmit(event){
    let url = `http://ec2-52-91-13-65.compute-1.amazonaws.com:9000/buildings?vehicle_collission=${this.state.vehicle_collission}&subway_entrances=${this.state.subway_entrances}&health_services=${this.state.health_services}`
    fetch('http://ec2-52-91-13-65.compute-1.amazonaws.com:9000/buildings')
        .then( res=> res.json())
        .then(res=> this.setState({response: res}))
        .catch(err=>err);
    event.preventDefault();
}


  render(){
    const WrappedMap = withScriptjs(withGoogleMap(Map));
    return(

        <div>{!this.state.selectedHouse && <Query setSelectedHouse={this.setSelectedHouse} response={this.state.response} data={this.state} handleChange={this.handleChange} handleSubmit={this.handleSubmit} />}<div style={{ width: "100vw", height: "100vh"}}>
            <WrappedMap 
            googleMapURL={`https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=${
              process.env.REACT_APP_GOOGLE_KEY
          }`} 
            loadingElement = { <div style={{height: "100%"}}/>}
            containerElement = { <div style={{height: "100%"}}/>}
            mapElement =  { <div style={{height: "100%"}}/>} 
            response={this.state.response}
            selectHouse={this.setSelectedHouse}
            />
            {this.state.selectedHouse && <DetailedData house={this.state.selectedHouse}></DetailedData>}
          </div>
        </div> 
    )

  }

}


export default App