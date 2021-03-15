const baseURL = "http://localhost:5000";
const $CupcakesList = $("#cupcakes-list");


async function addToDom() {
    let response = await getCupcakes()
    for (let cupcake of response.data.cupcakes) {
        flavor = cupcake.flavor
        size = cupcake.size
        rating = cupcake.rating
        image = cupcake.image

        let cupcakesListItem = 
        `
        <li> 
        ${flavor}
        ${size}
        ${rating}
        <img src="${image}"></img>
        </li>
        `

        $CupcakesList.append(
            cupcakesListItem
        )
    }
}

async function getCupcakes() {
    let response = await axios.get(`${baseURL}/api/cupcakes`)
    return response
}

addToDom()