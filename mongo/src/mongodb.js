const mongoose = require("mongoose")




mongoose.connect("mongodb://localhost:27017/D-cather")
.then(()=>{
    console.log("mongodb connected")
})

.catch(()=>{
    console.log("failed to connect")
})

const LogInSchema = new mongoose.Schema({
    name:{
        type:String,
        required: true
    },
    password:{
        type:String,
        required: true
    }
})


const GoodsSchema = new mongoose.Schema({
   
    goods:{
        type:Array,
        required: true
    }
})

const colection = new mongoose.model("Collection1", GoodsSchema,"Collection1")
module.exports = colection
