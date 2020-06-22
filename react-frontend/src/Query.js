import React from 'react';
import './Query.css';

class Query extends React.Component{
    constructor(props){
        super(props)
        this.state = { 
            collission_query_type : 'precise',
            entrances_query_type : 'precise',
            health_services_query_type : 'precise',
            police_misconduct_query_type : 'precise',
            viewquery: false
     }
     this.toggleQueries = this.toggleQueries.bind(this)
    }

    toggleQueries(){
        this.setState({viewquery: !this.state.viewquery})

    }
  
    
    render(){
        let queriedhouses = this.props.response;
        let displayhouses;
        if(queriedhouses){
            displayhouses = queriedhouses.map((building,index)=>(
                <div class="house">
                    <h2 onClick={()=>{ this.props.setSelectedHouse(building)}}>{building.house_id}</h2>
                    <div>Address: {building.address}</div>
                    <div></div>

                </div>
            ))
        }
        return(
            <div class="sidebar">
                <input class="searchbar" type="text" placeholder="Search..."></input>
                <hr></hr>
                {!this.props.viewquery && <form onSubmit={this.props.handleSubmit}>
                    <label><div>Vehicle Collissions</div>
                        <input name="vehicle_collission1" type="number" value={this.props.data.vehicle_collission1} onChange={this.props.handleChange}/>
                        to
                        <input name="vehicle_collission2" type="number" value={this.props.data.vehicle_collission2} onChange={this.props.handleChange}/>
                    </label>
                    <label><div>Subway Entrances</div>
                        <input type="number" name="subway_entrances1" value={this.props.data.subway_entrances1} onChange={this.props.handleChange}/>
                        to
                        <input type="number" name="subway_entrances2" value={this.props.data.subway_entrances2} onChange={this.props.handleChange}/>
                    </label>
                    <label><div>Mental Health Services</div>
                        <input type="number" name="health_services1" value={this.props.data.health_services1} onChange={this.props.handleChange}/>
                        to
                        <input type="number" name="health_services2" value={this.props.data.health_services2} onChange={this.props.handleChange}/>
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