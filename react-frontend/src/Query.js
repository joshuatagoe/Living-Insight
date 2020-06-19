import React from 'react';

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

    handleChange(evt){
        this.setState({
            [evt.target.name] : evt.target.value
            
        })
    }


    
    render(){
        return(
            <div>
                <form onSubmit={this.props.handleSubmit}>
                    <label>Vehicle Collissions
                        <input name="vehicle_collission" type="number" value={this.state.vehicle_collission} onChange={this.props.handleChange}/>
                    </label>
                    <label>Subway Entrances
                        <input type="number" name="subway_entrances" value={this.state.subway_entrances} onChange={this.props.handleChange}/>
                    </label>
                    <label>Mental Health Services
                        <input type="number" name="health_services" value={this.state.health_services} onChange={this.props.handleChange}/>
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

export default Query
