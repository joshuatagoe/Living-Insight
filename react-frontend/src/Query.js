import React from 'react';

class Query extends React.Component{
    constructor(props){
        super(props)
        this.state = { 
            collission_query_type : 'precise',
            entrances_query_type : 'precise',
            health_services_query_type : 'precise',
            police_misconduct_query_type : 'precise',
            vehicle_collission: 0,
            subway_entrances: 0,
            health_services: 0,
            police_misconduct_reports : 0,
            response : ""

     }
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.callAPI = this.callAPI.bind(this);
    }

    handleChange(evt){
        this.setState({
            [evt.target.name] : evt.target.value
            
        })
    }

    handleSubmit(event){
        fetch("http://localhost:9000/buildings")
            .then( res=> res.text())
            .then(res=> this.setState({response: res}))
            .catch(err=>err);
        event.preventDefault();
    }
    
    render(){
        return(
            <div>
                <form onSubmit={this.handleSubmit}>
                    <label>Vehicle Collissions
                        <input name="vehicle_collission" type="number" value={this.state.vehicle_collission} onChange={this.handleChange}/>
                    </label>
                    <label>Subway Entrances
                        <input type="number" name="subway_entrances" value={this.state.subway_entrances} onChange={this.handleChange}/>
                    </label>
                    <label>Mental Health Services
                        <input type="number" name="health_services" value={this.state.health_services} onChange={this.handleChange}/>
                    </label>
                    <label>Number of Police Misconduct Reports
                        <input type="number" name="police_misconduct_reports" value={this.state.police_misconduct_reports} onChange={this.handleChange}/>
                    </label>
                <input type="submit" value="Submit"/>
                </form>
                <div>{this.state.response}</div>

            </div>

        )
    }


}

export default Query