const express = require("express")
const app = express()
const path = require("path")
const hbs = require("hbs")
const collection = require("./mongodb")
const cors = require('cors');

const tempelatePath = path.join(__dirname, '../templates')


app.use(cors());
app.use(express.json())
app.set("view engine", "hbs")
app.set("views", tempelatePath)
app.use(express.urlencoded({extended: false}))



app.get("/", (req, res) => {
    res.render("login")
})

app.post("/signup", async (req, res) =>{
    const data = {
        name: req.body.name,
        password: req.body.password
    }

    await collection.insertMany([data])

    res.render("home")
})


app.get("/login", async (req, res) =>{
    
   // var query = req.params.query;
    
    let query = req.query.query;
    
  //  console.log(collection);
    
    
    var arr = {key1:'value1', key2:'value2'}
    
     var findResult2 = await collection.find();
     
     
      var ArrJson =  Array();
      
        var container = [];
     
     findResult2.forEach(function(obj) {
         
         var test = JSON.stringify(obj);
         
        
         
          var test2 =  JSON.parse(test);
    
    var re = JSON.stringify(test2.goods).replace("[", "").replace("{", "").replace("}", "").replace("]", "");
    
    
   // console.log(re);
    
    var array = re.split(",\"");
    
    //console.log(array)
    
    var arrayj = Array();
    
  
    
    array.forEach(function (item, index) {
        
        var pattern = RegExp(query, 'i'); // pattern: /a/gi
        
        
        if (item.match(pattern)) {
 var cpa = item.split(":"); 
            if (cpa[1])
            {
            
           
            var item = cpa[0].replace("\"","").trim();
            var price = cpa[1].replace("\"","").trim();
            var id = test2._id.trim();
            var market = test2.market.trim();
            var category = test2.category_name.trim();
            
       
            container.push({item: item, price: price, category: category, id: id, market: market});
			}
          
}
//console.log(arrayj)

});
    

         
         
     })
         
         
         container.sort(function(a, b) {
    return parseFloat(a.price) - parseFloat(b.price);
});
         
         res.setHeader('Access-Control-Allow-Origin', '*'); /* @dev First, read about security */
         res.setHeader('Access-Control-Allow-Credentials', true);
         res.setHeader('Access-Control-Allow-Methods','*'); // 30 days
         res.setHeader('Access-Control-Allow-Headers', 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers'); //
         
         res.send(container)
   
       
})


app.get("/signup", (req, res) => {
    res.render("signup")
})



app.get('/info', (req, res) => {
  const data = {
    name: 'John Doe',
    email: 'johndoe@example.com',
    age: 30
  };
  res.json(data);
});


var keys = collection.find({}).limit(2);
//console.log(keys);
 


app.listen(3000, () =>{
    
    
    console.log("port conected")
})
