import React from 'react';
import {  withScriptjs, withGoogleMap} from 'react-google-maps';
import Map from './Map';
import Query from './Query'
class App extends React.Component{

  constructor(props){
    super(props)
    this.state = {
      vehicle_collission: 0,
      subway_entrances: 0,
      health_services: 0,
      police_misconduct_reports : 0,
      response : ""

    }
    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
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

        <div><Query data={this.state} handleChange={this.handleChange} handleSubmit={this.handleSubmit} /><div style={{ width: "100vw", height: "100vh"}}>
            <WrappedMap 
            googleMapURL={`https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=${
              process.env.REACT_APP_GOOGLE_KEY
          }`} 
            loadingElement = { <div style={{height: "100%"}}/>}
            containerElement = { <div style={{height: "100%"}}/>}
            mapElement =  { <div style={{height: "100%"}}/>} 
            response={this.state.response}
            />
          </div>
        </div> 
    )

  }

}


export default App