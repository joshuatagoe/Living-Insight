const { query, response } = require('express');

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
  search = request.query.search
  pool.query(`SELECT * FROM  final_buildings_set WHERE house_id=${search}`, (error,results)=>{
    if(error){
      throw error

    }
    response.status(200).json(results.rows)

  })

}

const search_address = ( request, response)=>{
 console.log("got to function")
 console.log(request.query)
 search = request.query.search
  pool.query(`SELECT * FROM  final_buildings_set WHERE address=${search}`, (error,results)=>{
    if(results.length<1){
       console.log("ai")
    }
    if(error){
      throw error

    }
    response.status(200).json(results.rows)

  })

}



    






  module.exports = {
      getbuildings,
      test,
      get_traffic_incidents,
      get_subway_entrances,
      get_mental_health_service,
      search_house_id,
      search_address
  }

