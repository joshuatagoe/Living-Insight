import React from 'react';
import './Query.css';

class Query extends React.Component{
    constructor(props){
        super(props)
        this.state = { 
            vehicle_collission1: 0,
            subway_entrances1: 0,
            health_services1: 0,
            vehicle_collission2: 0,
            subway_entrances2: 0,
            health_services2: 0,
            viewquery: false
     }
     this.toggleQueries = this.toggleQueries.bind(this)
     this.handleChange = this.handleChange.bind(this)
    }

    toggleQueries(){
        this.setState({viewquery: !this.state.viewquery})

    }
  
    handleChange(evt){
        this.setState({
            [evt.target.name] : evt.target.value
            
        })
     }
    
    render(){
        let queriedhouses = this.props.response;
        let displayhouses;
        if(queriedhouses){
            displayhouses = queriedhouses.map((building,index)=>(
                <div class="house">
                    <span  style={{fontSize: "1rem"}} class="fa-stack fa-3x">
                        <i class="fa fa-circle-o fa-stack-2x"></i>
                        <strong class="fa-stack-1x">{index+1}</strong>
                    </span>
                    <h2 style={{cursor: "pointer"}} onClick={()=>{ this.props.setSelectedHouse(building)}}>{building.house_id}</h2>
                    <div>Address: {building.address}</div>
                    <div>Rental Price: {building.rental_price}</div>

                </div>
            ))
        }
        return(
            <div class="sidebar">
                <input class="searchbar" type="text" placeholder="Search..."></input>
                <hr></hr>
                {!this.props.viewquery && <form onSubmit={(e)=>{
                    this.props.handleSubmit(this.state.vehicle_collission1, this.state.subway_entrances1, this.state.health_services1)
                    e.preventDefault();
                    
                    }}>
                    <label><div>Vehicle Collissions</div>
                        <input name="vehicle_collission1" type="number" value={this.state.vehicle_collission1} onChange={this.handleChange}/>
                        to
                        <input name="vehicle_collission2" type="number" value={this.state.vehicle_collission2} onChange={this.handleChange}/>
                    </label>
                    <label><div>Subway Entrances</div>
                        <input type="number" name="subway_entrances1" value={this.state.subway_entrances1} onChange={this.handleChange}/>
                        to
                        <input type="number" name="subway_entrances2" value={this.state.subway_entrances2} onChange={this.handleChange}/>
                    </label>
                    <label><div>Mental Health Services</div>
                        <input type="number" name="health_services1" value={this.state.health_services1} onChange={this.handleChange}/>
                        to
                        <input type="number" name="health_services2" value={this.state.health_services2} onChange={this.handleChange}/>
                    </label>
  {/*                     <label>Number of Police Misconduct Reports
                        <input type="number" name="police_misconduct_reports" value={this.state.police_misconduct_reports} onChange={this.props.handleChange}/>
                    </label> */}
                <hr></hr>
                <input onClick={this.toggleQueries} type="submit" value="Query"/>
                </form>  }
                {this.state.viewquery && displayhouses}
                    
            </div>
  
        )
    }
  
  
  }

  export default Query;