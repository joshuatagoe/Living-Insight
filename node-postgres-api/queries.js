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

    pool.query('SELECT * FROM final_buildings_set LIMIT 20 WHERE total_services BETWEEN '+req.query.health_services1+' AND '+ req.query.health_services2+' AND total_collissions BETWEEN '+req.query.vehicle_collission1+' AND '+req.query.vehicle_collission2+' AND total_entrances BETWEEN '+req.query.subway_entrances1+' AND '+req.query.subway_entrances2, (error, results) => {
      if (error) {
        throw error
      }
      resp.status(200).json(results.rows)
    })
  }


const get_mental_health_service = (request, response) => {

pool.query('SELECT * from mental_health WHERE query_id=(SELECT * FROM mental_health WHERE house_id='+query+")", (error, results) => {
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
  pool.query(`WITH upd AS ( SELECT * FROM building_to_collissions WHERE house_id=${house_id} ) SELECT * FROM vehicle_collissions INNER JOIN upd ON vehicle_collissions.collision_id=upd.collision_id ORDER BY num_killed DESC LIMIT 20`, (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
    
  }


const get_subway_stations = (request, response) => {

  pool.query('SELECT * from mental_health WHERE query_id=(SELECT * FROM mental_health WHERE house_id='+query+")", (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
    
  }



    






  module.exports = {
      getbuildings,
      test,
      get_traffic_incidents,
  }

