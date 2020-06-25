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
                    this.props.handleSubmit(this.state.vehicle_collission1, this.state.vehicle_collission2, this.state.subway_entrances1, this.state.subway_entrances2, this.state.health_services1, this.state.health_services2, this.state.crimes1, this.state.crimes2)
                    e.preventDefault();
                    
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
                    <label><div>NYPD Complaints (Felonies, Misdemeanors, Violations)</div>
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
                {this.state.viewquery && displayhouses}
                    
            </div>
  
        )
    }
  
  
  }

  export default Query;