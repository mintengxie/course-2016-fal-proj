const express = require('express');
const app = express();
const bodyParser = require('body-parser')
const MongoClient = require('mongodb').MongoClient

var db

MongoClient.connect('mongodb://localhost:27017/repo', (err, database) => {
  if (err) return console.log(err)
  db = database
  app.listen(process.env.PORT || 3000, () => {
    console.log('listening on 3000')
  })
})

app.set('view engine', 'ejs')
app.use(bodyParser.urlencoded({extended: true}))
app.use(bodyParser.json())
app.use(express.static('public'))


app.get('/', (req, res) => {
  db.collection("aydenbu_huangyh.statistic_data").find().toArray((err, result) => {
    if (err) return console.log(err)
    res.render('bubble.ejs', {tdata: result})
  })
})

app.post('/histogram', (req, res) => {
  db.collection("aydenbu_huangyh.public_earning_crime_boston").find().toArray((err, result) => {
    if (err) return console.log(err)
//    console.log('saved to database')
    res.render('histogram.ejs', {tdata: result})
  })
})

app.post('/bubble', (req, res) => {
  db.collection("aydenbu_huangyh.statistic_data").find().toArray((err, result) => {
    if (err) return console.log(err)
//    console.log('saved to database')
    res.render('bubble.ejs', {tdata: result})
  })
})

// Note: request and response are usually written as req and res respectively.
