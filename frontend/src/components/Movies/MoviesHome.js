import React from "react"

const movies=[

{
name:"Avengers",
image:"https://images.unsplash.com/photo-1489599849927-2ee91cede3ba"
},

{
name:"Avatar",
image:"https://images.unsplash.com/photo-1517602302552-471fe67acf66"
}

]

function MoviesHome(){

return(

<div>

<h2>Movies</h2>

{movies.map((m)=>(

<div>

<img src={m.image} width="200"/>

<h3>{m.name}</h3>

<button>Book Ticket</button>

</div>

))}

</div>

)

}

export default MoviesHome
