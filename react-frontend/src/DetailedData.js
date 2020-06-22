import React from 'react';
import './DetailedData.css'

class DetailedData extends React.Component{
    constructor(props){
        super(props)

        this.state = {
            vehicle_collissions: null,
            mental_health : null,
            crime: null,
            police_misconduct: null,
            air_quality: null,
        }

        this.fetch_vehicle_data = this.fetch_vehicle_data.bind(this)
        this.fetch_mental_health = this.fetch_mental_health.bind(this)
        this.fetch_crime_data = this.fetch_crime_data.bind(this)
    }

    componentDidMount(){

    }

    fetch_vehicle_data(event){
        let url = `http://ec2-52-91-13-65.compute-1.amazonaws.com:9000`;
        fetch(url)
            .then( res=> res.json())
            .then(res=> this.setState({vehicle_collissions : res}))
            .catch(err=>err);
        event.preventDefault();
    }

    fetch_mental_health(event){
        let url = `http://ec2-52-91-13-65.compute-1.amazonaws.com:9000`;
        fetch(url)
            .then( res=> res.json())
            .then(res=> this.setState({vehicle_collissions : res}))
            .catch(err=>err);
        event.preventDefault();
    }

    fetch_crime_data(event){
        let url = `http://ec2-52-91-13-65.compute-1.amazonaws.com:9000`;
        fetch(url)
            .then( res=> res.json())
            .then(res=> this.setState({vehicle_collissions : res}))
            .catch(err=>err);
        event.preventDefault();

    }

    fetch_air_quality(event){
        let url = `http://ec2-52-91-13-65.compute-1.amazonaws.com:9000`;
        fetch(url)
            .then( res=> res.json())
            .then(res=> this.setState({vehicle_collissions : res}))
            .catch(err=>err);
        event.preventDefault();
    }
  
    
    render(){
        let data = this.props.house;
        let info =<div>{data.house_id}</div>
        return(
            <div class="bottombar">
                {info}
            </div>  
        )

}
}
  export default DetailedData;