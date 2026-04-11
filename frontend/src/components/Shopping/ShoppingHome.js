import React, { useState } from "react"

const products=[

{
id:1,
name:"Men T Shirt",
price:499,
image:"https://images.unsplash.com/photo-1521572163474-6864f9cf17ab"
},

{
id:2,
name:"Women Dress",
price:899,
image:"https://images.unsplash.com/photo-1520975922320-7c0b2b1e91c2"
},

{
id:3,
name:"Kids Shirt",
price:299,
image:"https://images.unsplash.com/photo-1518837695005-2083093ee35b"
}

]

function ShoppingHome(){

const [cart,setCart] = useState([])

function addToCart(product){

setCart([...cart,product])

alert(product.name + " added to cart")

}

return(

<div>

<h2>Shopping</h2>

<h3>Cart Items: {cart.length}</h3>

<div style={{display:"flex",gap:"20px"}}>

{products.map((p)=>(
<div key={p.id} style={{border:"1px solid grey",padding:"10px"}}>

<img src={p.image} width="200"/>

<h3>{p.name}</h3>

<p>₹{p.price}</p>

<button onClick={()=>addToCart(p)}>
Add To Cart
</button>

</div>
))}

</div>

</div>

)

}

export default ShoppingHome
