export default defineEventHandler(async (event) => {

    // read the body searchQuery: "placesearchquery" and use above google api
    // to search for the place and return the result

    // im in a nuxt.js function, get the body
    const body = await readBody(event)

    // get the searchQuery
    const searchQuery = JSON.parse(body).searchQuery

    // get google api key from .env GMAPS_API_KEY
    const apiKey = process.env.GMAPS_API_KEY


    const response = await fetch(`https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&input=${searchQuery}&inputtype=textquery&key=${apiKey}`)

    const responseData = await response.json()



    return {
        "timestamp": Date.now(),
        "coords": {
            "accuracy": null,
            "latitude": responseData.candidates[0].geometry.location.lat,
            "longitude": responseData.candidates[0].geometry.location.lng,
            "altitude": null,
            "altitudeAccuracy": null,
            "heading": null,
            "speed": null
        }
    }
 
});