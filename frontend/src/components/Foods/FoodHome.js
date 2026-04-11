import React from "react"

const foods=[

{
name:"Pizza",
price:250,
image:"https://images.unsplash.com/photo-1548365328-5c6db3224f3a"
},

{
name:"Burger",
price:150,
image:"https://images.unsplash.com/photo-1550547660-d9450f859349"
},

{
name:"Biryani",
price:300,
image:"https://images.unsplash.com/photo-1604908176997-4315b7c2b2cb"
}

]

function FoodHome(){

return(

<div>

<h2>Foods</h2>

<div style={{display:"flex",gap:"20px"}}>

{foods.map((f)=>(
<div style={{border:"1px solid grey",padding:"10px"}}>

<img src={f.image} width="200"/>

<h3>{f.name}</h3>

<p>₹{f.price}</p>

<button>Add To Cart</button>

</div>
))}

</div>

</div>

)

}

export default FoodHome
