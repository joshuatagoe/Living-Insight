const express = require('express')
const bodyParser = require('body-parser')
const  app = express()
const db = require('./queries')
const port = 9000

app.use(bodyParser.json())
app.use(
    bodyParser.urlencoded({
        extended: true,
    })
)

app.get('/', (request, response)=>{
    response.json({ info: 'Node.js, Express, and Postgres API'})
})

app.get('/buildings',db.getbuildings)



app.listen(port,()=>{
    console.log(`App Running on port ${port}.`)
})
