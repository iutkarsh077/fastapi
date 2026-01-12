import axios from "axios"
async function ChatResponse(req, res){
    const question = req.query.question;

    console.log("Question is: ", question)
    try {
        const response = await axios.get("http://localhost:8000/chat",{
            params:  { question: question }
        });

        console.log("Response of python: ", response.data);

        return res.status(201).json({message: "Everything working fine", data: response.data})
    } catch (error) {
        console.log(error);
        return res.status(500).json({message: "Internal Server Error"})
    }
}

export default ChatResponse