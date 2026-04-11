import React, {useEffect, useState} from "react";

function Shopping(){

const [products,setProducts] = useState([]);

useEffect(()=>{

fetch("http://127.0.0.1:8000/shopping/products/")
.then(res=>res.json())
.then(data=>setProducts(data))

},[])

return(

<div>

<h2>Shopping</h2>

{products.map(p=>(
<div key={p.id}>

<img src={p.image} width="150"/>

<h3>{p.name}</h3>

<p>₹ {p.price}</p>

</div>
))}

</div>

)

}

export default Shopping;
