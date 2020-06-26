import React, {useRef, useEffect} from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';
import './DetailedData.css';
import {     get_mental_health_bin,
    get_subway_bin,
    get_collissions_bin,
    get_num_injured_bin,
    get_num_killed_bin,
    get_total_affected_bin,
    get_felonies_bin,
    get_violations_bin,
    get_misdemeanors_bin,
 } from './bins.js';

const {tableau } = window;
var viz;
var workbook;
var activeSheet;





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
        this.initViz = this.initViz.bind(this);
        this.selectMarks = this.selectMarks.bind(this)
    }

    componentDidMount(){
        this.props.getData();
        let ref = this.initViz();
        ref.addEventListener('tabswitch', (event)=>{
            console.log(event);
            this.selectMarks(viz, event.getNewSheetName());
        })
        console.log(workbook);
        console.log(activeSheet);
        


        //this.fetch_vehicle_data();

/*        this.fetch_mental_health();
        this.fetch_crime_data(); */

    }


    initViz(){
        let data = this.props.house;
        console.log(data.total_services);
        const options = {
            device: "desktop",
            onFirstInteractive: function(){ 
                let worksheet;
                viz.getWorkbook().activateSheetAsync("mental_health").then(function (sheet) {
                    worksheet = sheet;
                    console.log(worksheet);
                  })
                  // Single dimensions work just like filtering
                  // Single dimension - single value
                  .then(function () {
                    return worksheet.selectMarksAsync("Total Services (bin)", get_mental_health_bin(data.total_services),
                      tableau.SelectionUpdateType.REPLACE);
                  })
            }
        }
        let url = "https://prod-useast-a.online.tableau.com/t/livinginsight/views/living_insight_sheets/mental_health/jnt297@nyu.edu/483edf18-3de8-4b8f-ae55-55ea292941a2?:display_count=n&:showVizHome=n&:origin=viz_share_link";
        viz = new tableau.Viz(this.myRef.current, url, options)
        var tt = viz.getUrl();
        return viz;
    }


    selectMarks(viz,sheet_name){
        console.log(sheet_name);
        let worksheet;
        let data = this.props.house;
        console.log(data)

        function roundtoK(num){
            let val = Math.round(num/1000)*1000
            val = val.toString()
            val = val.substring(0,val.length-3)+"K"
            console.log(val)
            return val
        }
     
        viz.getWorkbook().activateSheetAsync(sheet_name).then(function(sheet){
            worksheet = sheet;
            sheet.getSelectedMarksAsync().then(function(marks){
                let mark = marks;
                var value_array = new Array();
                for(let k=0;k<marks.length;k++){
                let pairs = marks[k].getPairs();
                console.log(marks[k].getPairs());
                console.log("Selected Mark " + k + " , " + pairs.length + " pairs of data");
                }
            })
            console.log(roundtoK(get_total_affected_bin(data.total_affected)))
        })

        .then(function(){
            switch(sheet_name){
                case "mental_health":
                    return worksheet.selectMarksAsync("Total Services (bin)", get_mental_health_bin(data.total_services),
                      tableau.SelectionUpdateType.REPLACE);
                case "collissions":
                    return worksheet.selectMarksAsync("Total Collissions (bin)",roundtoK(get_collissions_bin(data.total_collissions)),
                      tableau.SelectionUpdateType.REPLACE);
                case "num_killed":
                    return worksheet.selectMarksAsync("Total Killed (bin)", get_num_killed_bin(data.total_killed),
                    tableau.SelectionUpdateType.REPLACE);
                case "num_injured":
                    return worksheet.selectMarksAsync("Total Injured (bin)", roundtoK(get_num_injured_bin(data.total_injured)),
                    tableau.SelectionUpdateType.REPLACE);
                case "num_entrances":
                    return worksheet.selectMarksAsync("Total Entrances (bin)", get_subway_bin(data.total_entrances),
                    tableau.SelectionUpdateType.REPLACE);
                case "num_misdemeanors":
                    return worksheet.selectMarksAsync("Total Misdemeanors (Num Misdemeanors) (bin)", get_misdemeanors_bin(data.total_misdemeanors),
                    tableau.SelectionUpdateType.REPLACE);
                case "num_felonies":
                    return worksheet.selectMarksAsync("Total Felonies (Num Felonies) (bin)", get_felonies_bin(data.total_felonies),
                    tableau.SelectionUpdateType.REPLACE);
                case "Total Affected":
                    return worksheet.selectMarksAsync("Total Affected (Num Collissions) (bin)", roundtoK(get_total_affected_bin(data.total_affected)),
                    tableau.SelectionUpdateType.REPLACE);
                case "num_violations":
                    return worksheet.selectMarksAsync("Total Violations (Num Violations) (bin)", get_violations_bin(data.total_violations),
                    tableau.SelectionUpdateType.REPLACE);
                case "crime_types":
                    return worksheet.applyFilterAsync("House Id (Building Id To Crime Id)", data.house_id,
                    tableau.FilterUpdateType.REPLACE);
                


            }

        })

    

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
                <button class="close" onClick={this.props.close}></button>
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