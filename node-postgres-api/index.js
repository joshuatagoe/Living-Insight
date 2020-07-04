const express = require('express')
const bodyParser = require('body-parser')
const  app = express()
const db = require('./queries')
const cors = require('cors');
const port = 9000

app.use(bodyParser.json())
app.use(
    bodyParser.urlencoded({
        extended: true,
    })
)
app.use(cors());
app.use(function(req,res,next){
    if(req.query.search_type='house_id'){
        
    }
    if(req.query.search_type='address'){

    }
})

app.get('/', (request, response)=>{
    response.json({ info: 'Node.js, Express, and Postgres API'})
})

app.get('/buildings',db.test)
app.get('/getbuildings',db.getbuildings)
app.get('/get_incidents', db.get_traffic_incidents)
app.get('/get_health_services', db.get_mental_health_service)
app.get('/get_subway_entrances', db.get_subway_entrances)
app.get('/search',(req,res)=>{
    var query_index = req.originalUrl.indexOf('?');
    var query_string = (query_index>=0)?req.originalUrl.slice(query_index+1):'';
    if(req.query.search_type='house_id'){
        res.redirect('/search_id'+query_string)
    }
    if(req.qsuery.search_type='address'){
        res.redirect('/search_address'+query_string)
    }
})
app.get('/search_id',db.search_house_id)
app.get('/search_address',db.search_address)



app.listen(port,()=>{
    console.log(`App Running on port ${port}.`)
})
