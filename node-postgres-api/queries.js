const { query, response } = require('express');

const Pool = require('pg').Pool

const pool= new Pool({
    host: 'localhost',
    database: 'living_insight',
    user: 'postgres',
    password: 'postgres',
    port: 5432,
})



const getbuildings = (request, response) => {
    query = ""
    if(req.query.mentalhealthtype=="rating"):
      query+= " WHERE mental_health_rating="+req.query.mentalhealth;
    else if(req.query.mentalhealthtype=="precise"):
      query+= " WHERE mental_health_services_num="+req.query.mentalhealth;
    
      
    pool.query('SELECT * FROM buildings'+query, (error, results) => {
      if (error) {
        throw error
      }
      response.status(200).json(results.rows)
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

  pool.query('SELECT * from mental_health WHERE query_id=(SELECT * FROM mental_health WHERE house_id='+query+")", (error, results) => {
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
  }

