<template>

    <div class="container mx-auto px-5 pt-3 pb-5">
        <p class="text-3xl">{{ route.name }}</p>
        <p class="text-lg text-gray-500">{{ route.city }}</p>

        <div v-if="route.lines">
            <LMap style="height: 350px" :zoom="13"
                :center="[route.lines.coordinates[0][0].lat, route.lines.coordinates[0][0].lng]"
                :use-global-leaflet="false">
                <LTileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution="&amp;copy; <a href=&quot;https://www.openstreetmap.org/&quot;>OpenStreetMap</a> contributors"
                    layer-type="base" name="OpenStreetMap" />

                <LPolyline :lat-lngs="route.lines.coordinates" color="green" />
            </LMap>

        </div>
    </div>

</template>

<script>
export default {

    async mounted() {

        // fetch id from route
        const route_id = this.$route.params.id

        const response = await fetch('/api/getRoute?route_id=' + route_id, {
            method: 'GET'
        })
        const responseData = await response.json()
        this.route = responseData.body
        this.loaded = true
    },

    data() {
        return {
            loaded: false,
            route: [],
            megaRouteArray: [[{ 'lat': 51.4980303, 'lng': -0.09012629999999999 }, { 'lat': 51.498188, 'lng': -0.0903182 }], [{ 'lat': 51.498188, 'lng': -0.0903182 }, { 'lat': 51.4979702, 'lng': -0.0906276 }], [{ 'lat': 51.4979702, 'lng': -0.0906276 }, { 'lat': 51.500008, 'lng': -0.0957027 }], [{ 'lat': 51.500008, 'lng': -0.0957027 }, { 'lat': 51.499275, 'lng': -0.0968404 }], [{ 'lat': 51.499275, 'lng': -0.0968404 }, { 'lat': 51.4987892, 'lng': -0.1044554 }], [{ 'lat': 51.4987892, 'lng': -0.1044554 }, { 'lat': 51.49869280000001, 'lng': -0.11162 }], [{ 'lat': 51.49869280000001, 'lng': -0.11162 }, { 'lat': 51.5004784, 'lng': -0.1156077 }], [{ 'lat': 51.5004784, 'lng': -0.1156077 }, { 'lat': 51.5005838, 'lng': -0.1158662 }], [{ 'lat': 51.5005838, 'lng': -0.1158662 }, { 'lat': 51.5003476, 'lng': -0.1165186 }], [{ 'lat': 51.5003476, 'lng': -0.1165186 }, { 'lat': 51.5009494, 'lng': -0.1262172 }], [{ 'lat': 51.5009494, 'lng': -0.1262172 }, { 'lat': 51.5008085, 'lng': -0.1262237 }], [{ 'lat': 51.5008085, 'lng': -0.1262237 }, { 'lat': 51.5009788, 'lng': -0.1272326 }], [{ 'lat': 51.5009788, 'lng': -0.1272326 }, { 'lat': 51.501282, 'lng': -0.1293867 }], [{ 'lat': 51.501282, 'lng': -0.1293867 }, { 'lat': 51.5014438, 'lng': -0.1299586 }], [{ 'lat': 51.5014438, 'lng': -0.1299586 }, { 'lat': 51.50451169999999, 'lng': -0.1293665 }], [{ 'lat': 51.50452869999999, 'lng': -0.1292317 }, { 'lat': 51.5048656, 'lng': -0.1266321 }], [{ 'lat': 51.5048656, 'lng': -0.1266321 }, { 'lat': 51.50680269999999, 'lng': -0.1275415 }], [{ 'lat': 51.50680269999999, 'lng': -0.1275415 }, { 'lat': 51.507079, 'lng': -0.1276529 }], [{ 'lat': 51.507079, 'lng': -0.1276529 }, { 'lat': 51.5076069, 'lng': -0.1272298 }], [{ 'lat': 51.5076069, 'lng': -0.1272298 }, { 'lat': 51.5079466, 'lng': -0.1276171 }], [{ 'lat': 51.5079466, 'lng': -0.1276171 }, { 'lat': 51.5078865, 'lng': -0.1279919 }], [{ 'lat': 51.5078865, 'lng': -0.1279919 }, { 'lat': 51.5080404, 'lng': -0.1280606 }], [{ 'lat': 51.5080404, 'lng': -0.1280606 }, { 'lat': 51.5084722, 'lng': -0.1282475 }], [{ 'lat': 51.5084722, 'lng': -0.1282475 }, { 'lat': 51.5085562, 'lng': -0.1277613 }], [{ 'lat': 51.5085562, 'lng': -0.1277613 }, { 'lat': 51.5085516, 'lng': -0.1273923 }], [{ 'lat': 51.5085516, 'lng': -0.1273923 }, { 'lat': 51.5092259, 'lng': -0.1273335 }], [{ 'lat': 51.5092259, 'lng': -0.1273335 }, { 'lat': 51.5117737, 'lng': -0.1284913 }], [{ 'lat': 51.5117737, 'lng': -0.1284913 }, { 'lat': 51.51636209999999, 'lng': -0.1305102 }], [{ 'lat': 51.51636209999999, 'lng': -0.1305102 }, { 'lat': 51.5174326, 'lng': -0.1310181 }], [{ 'lat': 51.5174326, 'lng': -0.1310181 }, { 'lat': 51.5177942, 'lng': -0.130092 }], [{ 'lat': 51.5177942, 'lng': -0.130092 }, { 'lat': 51.5182531, 'lng': -0.1305555 }], [{ 'lat': 51.5182531, 'lng': -0.1305555 }, { 'lat': 51.5185388, 'lng': -0.1304014 }], [{ 'lat': 51.5185388, 'lng': -0.1304014 }, { 'lat': 51.5192853, 'lng': -0.1303397 }], [{ 'lat': 51.5192853, 'lng': -0.1303397 }, { 'lat': 51.51920670000001, 'lng': -0.1302756 }], [{ 'lat': 51.51920670000001, 'lng': -0.1302756 }, { 'lat': 51.5188767, 'lng': -0.1306825 }], [{ 'lat': 51.5188767, 'lng': -0.1306825 }, { 'lat': 51.5188309, 'lng': -0.1304987 }]]
        }
    }
}
</script>