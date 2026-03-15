import { useState } from "react";
import API from "../api/api";

function DonorDashboard() {

const [foodName, setFoodName] = useState("");
const [quantity, setQuantity] = useState("");
const [location, setLocation] = useState("");

const addFood = async () => {

try {

const token = localStorage.getItem("token");

if(!token){
alert("Please login first");
return;
}

const res = await API.post(
"/add-food",
{
food_name: foodName,
quantity: Number(quantity),
location: location
},
{
headers:{
Authorization: `Bearer ${token}`
}
}
);

console.log(res.data);

alert("Food Added Successfully!");

setFoodName("");
setQuantity("");
setLocation("");

} catch (error) {

console.log("Add Food Error:", error.response?.data);
alert("Error Adding Food");

}

};

return (

<div style={{textAlign:"center", marginTop:"80px"}}>

<h2>Donor Dashboard</h2>

<h3>Add Food Donation</h3>

<input
placeholder="Food Name"
value={foodName}
onChange={(e)=>setFoodName(e.target.value)}
/>

<br/><br/>
<input
type="number"
placeholder="Quantity"
value={quantity}
onChange={(e)=>setQuantity(e.target.value)}
/>

<br/><br/>

<input
placeholder="Location"
value={location}
onChange={(e)=>setLocation(e.target.value)}
/>

<br/><br/>

<button onClick={addFood}>
Add Food
</button>

</div>

)

}

export default DonorDashboard;