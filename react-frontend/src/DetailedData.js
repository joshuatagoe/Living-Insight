import React, {useRef, useEffect} from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';
import './DetailedData.css'

const {tableau } = window;






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
        this.myRef = React.createRef();
        this.fetch_vehicle_data = this.fetch_vehicle_data.bind(this)
        this.fetch_mental_health = this.fetch_mental_health.bind(this)
        this.fetch_crime_data = this.fetch_crime_data.bind(this)
    }

    componentDidMount(){
        this.props.getData();
        this.initViz();

        //this.fetch_vehicle_data();

/*        this.fetch_mental_health();
        this.fetch_crime_data(); */

    }

    initViz(){
        let url = "https://prod-useast-a.online.tableau.com/t/livinginsight/views/living_insight/Crime_2?:showAppBanner=false&:display_count=n&:showVizHome=n&:origin=viz_share_link";
        new tableau.Viz(this.myRef.current, url)
    }



    fetch_crime_data(event){
        let url = `http://ec2-52-91-13-65.compute-1.amazonaws.com:9000`;
        fetch(url)
            .then( res=> res.json())
            .then(res=> this.setState({vehicle_collissions : res}))
            .catch(err=>err);


    }

    fetch_air_quality(event){
        let url = `http://ec2-52-91-13-65.compute-1.amazonaws.com:9000`;
        fetch(url)
            .then( res=> res.json())
            .then(res=> this.setState({vehicle_collissions : res}))
            .catch(err=>err);

    }
  
    
    render(){
        let data = this.props.house;
        let info =<div>{data.house_id}</div>
        let collissions;
        if(this.state.vehicle_collissions){
            collissions =this.state.vehicle_collissions.map(()=>( <div> test</div>))
        }
        let tableauEmbed = (<div ref={this.myRef}></div>)
        return(
            <div class="bottombar">
                {tableauEmbed}
{/*                 <div class="column">
                {info}
                </div>
                <div class="column">
                    <h2>Mental Health</h2>

                </div>
                <div class="column">
                    <h2>Vehicle Collissions</h2>
                    {this.state.vehicle_collissions && collissions}
                </div>
                <div class="column">
                    <h2>Crime</h2>
                    {tableauEmbed}

                </div> */}
               
            </div>  
        )

}
}
  export default DetailedData;