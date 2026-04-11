import React from "react"
import {Link} from "react-router-dom"

function Welcome(){

return(

<div style={{
backgroundImage:"url(https://images.unsplash.com/photo-1518770660439-4636190af475)",
height:"100vh",
textAlign:"center",
color:"white"
}}>

<h1>OMNI PLATFORM</h1>

<Link to="/login">
<button>Explore</button>
</Link>

</div>

)
}

export default Welcome
