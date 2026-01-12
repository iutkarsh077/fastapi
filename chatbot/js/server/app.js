import 'dotenv/config'
import express from "express";
import router from "./helpers/Router.js";
import cors from "cors";
const app = express();

const PORT = process.env.PORT || 4000

app.use(express.json());

app.use(cors({
    origin: "http://localhost:5173",
    methods: ["GET", "POST"]
}))

app.use("/api", router);

app.get("/health", (req, res)=>{
    return res.status(200).json({message: "Health is good", status: true})
})

app.listen(PORT, ()=>{
    console.log(`Server is running at port ${PORT}`)
})