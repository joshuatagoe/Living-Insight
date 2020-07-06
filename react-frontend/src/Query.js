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
            crimes1 : 0,
            crimes2 : 0,
            viewquery: false,
            search: "",
            search_type: 'house_id'
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
                <form onSubmit={(e)=>{
                    e.preventDefault();
                    console.log("test")
                    this.props.search_data(this.state.search_type, this.state.search)
                    

                }}>
                    <select onChange={this.handleChange} value={this.state.search_type} name="search_type">
                    <option value="house_id">house_id</option>
                    <option value="address">address</option>
                    </select>
                    <input name="search" class="searchbar" onChange={this.handleChange} value={this.state.search} type="text" placeholder="Search..."></input>
                    </form>
                <hr></hr>
                {!this.props.viewquery && <form onSubmit={(e)=>{
                    e.preventDefault();
                    this.props.handleSubmit(this.state.vehicle_collission1, this.state.vehicle_collission2, this.state.subway_entrances1, this.state.subway_entrances2, this.state.health_services1, this.state.health_services2, this.state.crimes1, this.state.crimes2)

                    }}>
                    <label><div>Vehicle Collissions<div>Avg: 61509.841093117409 SD: 38094.55832552</div></div>
                        <input name="vehicle_collission1" type="number" value={this.state.vehicle_collission1} onChange={this.handleChange}/>
                        to
                        <input name="vehicle_collission2" type="number" value={this.state.vehicle_collission2} onChange={this.handleChange}/>
                    </label>
                    <label><div>Subway Entrances <div>Avg: 139.7330462863293864 SD: 111.381353080728</div></div>
                        <input type="number" name="subway_entrances1" value={this.state.subway_entrances1} onChange={this.handleChange}/>
                        to
                        <input type="number" name="subway_entrances2" value={this.state.subway_entrances2} onChange={this.handleChange}/>
                    </label>
                    <label><div>Mental Health Services  <div>Avg: 6.7795100222717149 SD: 4.2418973826743063</div></div>
                        <input type="number" name="health_services1" value={this.state.health_services1} onChange={this.handleChange}/>
                        to
                        <input type="number" name="health_services2" value={this.state.health_services2} onChange={this.handleChange}/>
                    </label>
                    <label><div>NYPD Complaints (Felonies, Misdemeanors, Violations)<div>Avg: 1310.2647657841140530 SD: 601.820533292486</div></div>
                        <input type="number" name="crimes1" value={this.state.crimes1} onChange={this.handleChange}/>
                        to
                        <input type="number" name="crimes2" value={this.state.crimes2} onChange={this.handleChange}/>
                    </label>
  {/*                     <label>Number of Police Misconduct Reports
                        <input type="number" name="police_misconduct_reports" value={this.state.police_misconduct_reports} onChange={this.props.handleChange}/>
                    </label> */}
                <hr></hr>
                <input onClick={this.toggleQueries} type="submit" value="Query"/>
                </form>  }
                {displayhouses}
                    
            </div>
  
        )
    }
  
  
  }

  export default Query;