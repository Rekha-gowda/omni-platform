import React from "react"
import {Link} from "react-router-dom"

function Home(){

return(

<div style={{textAlign:"center"}}>

<h1>OMNI PLATFORM</h1>

<div style={{display:"flex",justifyContent:"space-around"}}>

<Link to="/shopping">
<button>Shopping</button>
</Link>

<Link to="/foods">
<button>Foods</button>
</Link>

<Link to="/movies">
<button>Movies</button>
</Link>

<Link to="/travellers">
<button>Travellers</button>
</Link>

</div>

</div>

)

}

export default Home
