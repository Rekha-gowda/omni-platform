import React from "react"
import {useNavigate} from "react-router-dom"

function Signup(){

const navigate = useNavigate()

function handleSignup(){

navigate("/login")

}

return(

<div style={{textAlign:"center"}}>

<h2>Signup</h2>

<input placeholder="Username"/><br/><br/>
<input placeholder="Email"/><br/><br/>
<input type="password" placeholder="Password"/><br/><br/>

<button onClick={handleSignup}>Create Account</button>

</div>

)

}

export default Signup
