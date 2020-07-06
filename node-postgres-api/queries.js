const { query, response } = require('express');
const util = require('util')
const exec = util.promisify(require('child_process').exec);
const Pool = require('pg').Pool

const pool= new Pool({
    host: 'localhost',
    database: 'living_insight',
    user: 'postgres',
    password: 'postgres',
    port: 5432,
})




const test = (req, resp) => {
        
      pool.query('SELECT * FROM buildings LIMIT 5', (error, results) => {
        if (error) {
          throw error
        }
        resp.status(200).json(results.rows)
      })
    }
  


const getbuildings = (req, resp) => {
console.log(req.query)
    pool.query('SELECT * FROM final_buildings_set WHERE total_services BETWEEN '+req.query.health_services1+' AND '+ req.query.health_services2+' AND total_collissions BETWEEN '+req.query.vehicle_collission1+' AND '+req.query.vehicle_collission2+' AND total_entrances BETWEEN '+req.query.subway_entrances1+' AND '+req.query.subway_entrances2+' AND total_crimes BETWEEN '+req.query.crimes1+' AND '+req.query.crimes2+' ORDER BY rental_price ASC LIMIT 20', (error, results) => {
      if (error) {
        throw error
      }
      resp.status(200).json(results.rows)
    })
  }


const get_mental_health_service = (request, response) => {
house_id = request.query.house_id
pool.query(`WITH upd AS ( SELECT * FROM house_id_mental_health WHERE house_id=${house_id}) SELECT * FROM mental_health INNER JOIN upd ON mental_health.query_id=upd.query_id`, (error, results) => {
  if (error) {
    throw error
  }
  response.status(200).json(results.rows)
})
  
}

const get_complaints = (request, response) => {

  pool.query('SELECT * from mental_health WHERE query_id=(SELECT * FROM mental_health WHERE house_id='+query+")", (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
    
  }
  
const get_traffic_incidents = (request, response) => {
  house_id = request.query.house_id
  console.log(house_id)
  pool.query(`WITH upd AS ( SELECT * FROM building_to_collissions WHERE house_id=${house_id}) SELECT * FROM vehicle_collissions INNER JOIN upd ON vehicle_collissions.collision_id=upd.collision_id WHERE (num_injured,num_killed) IS NOT NULL ORDER BY (num_killed+num_injured) DESC LIMIT 20`, (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
    
  }


const get_subway_entrances = (request, response) => {
  house_id = request.query.house_id
  pool.query(`WITH upd AS ( SELECT * FROM building_to_subway WHERE house_id=${house_id}) SELECT * FROM subway_entrances INNER JOIN upd ON subway_entrances.object_id=upd.object_id LIMIT 30`, (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
    
  }

const search_house_id = ( request, response)=>{
  console.log("test")
  search = request.query.search
  console.log(search)
  pool.query(`SELECT * FROM  final_buildings_set WHERE house_id=${search}`, (error,results)=>{
    if(error){
      throw error

    }
    response.status(200).json(results.rows)

  })

}

const search_address = async ( request, response)=>{
 console.log("got to function")
 console.log(request.query)
 let search = request.query.search.toLowerCase().slice(1,-1)
console.log(search)
 search = search.replace(/^\s+|\s+$/g, '');
 search=`'${search}'`
 console.log(search)
  pool.query(`SELECT * FROM  final_buildings_set WHERE address=${search}`, async (error,results)=>{
    if(results.rows.length<1){
      try {
        const address = search
        const { stdout, stderr } = await exec(`spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-52-91-13-65.compute-1.amazonaws.com:7077 --driver-class-path /home/ubuntu/postgresql-42.2.14.jar /home/ubuntu/Housing-Insight/process_datasets/integrate_data.py ${address}`);
        const _id = stdout.replace(/\s/g, "");
	exec(`psql -U postgres -w -v v1="'${_id}'" -h 127.0.0.1 -d living_insight -f /home/ubuntu/Housing-Insight/process_datasets/integrate_data.sql`)
        console.log('stdout:', stdout);
	query_string =`SELECT * FROM  final_buildings_set WHERE house_id='${_id}'`
	console.log(query_string)
        pool.query(query_string, (error,results)=>{
		console.log(results.rows)
          if(error){
            throw error
          }
          return response.status(200).json(results.rows)

        })
    }catch(e) {
      console.error(e)
    }
    }
	else{
	return response.status(200).json(results.rows)
}
    if(error){
      throw error

    }
  })

}


const test_spark_job = async (request, response)=>{
  const address = '25 Union Square W, New York, NY 10003'
	try {
		const { stdout, stderr } = await exec(`spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-52-91-13-65.compute-1.amazonaws.com:7077 --driver-class-path /home/ubuntu/postgresql-42.2.14.jar /home/ubuntu/Housing-Insight/process_datasets/integrate_data.py '${address}'`);
                const _id  = stdout
                console.log(_id)
                exec(`psql -U postgres -w -v v1="'${_id}'" -h 127.0.0.1 -d living_insight -f /home/ubuntu/Housing-Insight/process_datasets/integrate_data.sql`)
                console.log('stdout:', stdout);
		return response.status(200).send({ data: stdout});	
} catch(e) {
	console.error(e)
}
};





    






  module.exports = {
      getbuildings,
      test,
      get_traffic_incidents,
      get_subway_entrances,
      get_mental_health_service,
      search_house_id,
      search_address,
	test_spark_job
  }

