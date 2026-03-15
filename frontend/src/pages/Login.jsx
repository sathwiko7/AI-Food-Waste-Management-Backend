import { useState } from "react";
import API from "../api/api";

function Login(){

const [email,setEmail] = useState("");
const [password,setPassword] = useState("");

const handleLogin = async () => {

try{

const res = await API.post("/login", {
email: email,
password: password
});

localStorage.setItem("token", res.data.access_token);

alert("Login Successful");

}catch(error){

console.log(error.response?.data);
alert("Login Failed");

}

};

return(

<div style={{textAlign:"center",marginTop:"100px"}}>

<h2>Login</h2>

<input
placeholder="Email"
value={email}
onChange={(e)=>setEmail(e.target.value)}
/>

<br/><br/>

<input
placeholder="Password"
type="password"
value={password}
onChange={(e)=>setPassword(e.target.value)}
/>

<br/><br/>

<button onClick={handleLogin}>
Login
</button>

</div>

)

}

export default Login;