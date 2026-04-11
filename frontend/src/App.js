import React from "react";
import {BrowserRouter as Router,Routes,Route} from "react-router-dom";

import Welcome from "./components/Welcome";
import Home from "./components/Home";

import Shopping from "./components/shopping/Shopping";
import Foods from "./components/foods/Foods";
import Movies from "./components/movies/Movies";
import Travellers from "./components/travellers/Travellers";

import Cart from "./components/cart/Cart";

function App(){

return(

<Router>

<Routes>

<Route path="/" element={<Welcome/>}/>
<Route path="/home" element={<Home/>}/>

<Route path="/shopping" element={<Shopping/>}/>
<Route path="/foods" element={<Foods/>}/>
<Route path="/movies" element={<Movies/>}/>
<Route path="/travellers" element={<Travellers/>}/>

<Route path="/cart" element={<Cart/>}/>

</Routes>

</Router>

)

}

export default App
