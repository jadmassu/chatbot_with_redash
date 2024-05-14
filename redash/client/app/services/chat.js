import { axios } from "@/services/axios";

const Chat = {
    openai: data => axios.post('api/chat', data),
    // openai: data => axios.post("192.168.1.17:5000", "/getQuery", data),
    //getQuery 
    //getvisulaization 

};

export default Chat; 