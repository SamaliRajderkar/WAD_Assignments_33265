var express=require("express")
var app=express()
var BodyParser=require("body-parser")
var mongoose=require("mongoose")


app.use(express.static('public'))
app.use(express.json());
app.use(express.urlencoded({ extended: true }));


//Connecting database
mongoose.connect('mongodb://localhost:27017/Database', { useNewUrlParser: true, useUnifiedTopology: true });

var database=mongoose.connection
database.on('error',()=>console.log("Error in connecting to database"))
database.once('open',()=>console.log("Connected to database"))

app.post("/sign_up",(req,res)=>{
    
    //User Input
    var name=req.body.names
    var age=req.body.age
    var email=req.body.email
    var mobile=req.body.mobile
    var gender=req.body.gender
    var password=req.body.password

    var data=
    {
        "name":name,
        "age":age,
        "email":email,
        "mobile":mobile,
        "gender":gender,
        "password":password,
    }

    database.collection('users').insertOne(data,(err,collection)=>{
      if (err) {
        console.error("Error inserting record:", err);
        res.status(500).send("Error inserting record");
    } else {
        console.log("Record inserted successfully");
        res.redirect('signup_success.html');
    }

    })

    return res.redirect('signup_success.html')
})


app.get("/",(req,res)=>{ 
    res.setHeader("Access-Control-Allow-Origin", "*");
res.sendFile(__dirname + '/index.html');}
).listen(3000);//As local host used
console.log("Listening to port");
