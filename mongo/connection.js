const mongo = require('mongodb').MongoClient;




mongo.connect('mongodb://localhost:27017/D-cather', function(err, db) { 
    if (err) {
        console.log(err + " - errror")
    }
    else {
        console.log("Connected correctly to DB.");
        db.close()
    }
    
    console.log(123123)
});

