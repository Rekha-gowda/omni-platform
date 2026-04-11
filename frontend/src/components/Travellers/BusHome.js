import React from "react"

function BusHome(){

const seats=[]

for(let i=1;i<=30;i++){

seats.push(i)

}

return(

<div>

<h2>Bus Booking</h2>

<div style={{
display:"grid",
gridTemplateColumns:"repeat(5,60px)",
gap:"10px"
}}>

{seats.map((s)=>(
<button>{s}</button>
))}

</div>

</div>

)

}

export default BusHome
