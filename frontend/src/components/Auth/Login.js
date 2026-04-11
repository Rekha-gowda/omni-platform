import React from "react"
import {Link,useNavigate} from "react-router-dom"

function Login(){

const navigate = useNavigate()

function handleLogin(){

navigate("/home")

}

return(

<div style={{textAlign:"center"}}>

<h2>Login</h2>

<input placeholder="Email"/><br/><br/>
<input type="password" placeholder="Password"/><br/><br/>

<button onClick={handleLogin}>Login</button>

<p>New User?</p>

<Link to="/signup">Signup</Link>

</div>

)

}

export default Login
