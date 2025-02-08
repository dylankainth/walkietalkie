<template>
    <div>

        <input type="text" class="w-full border border-gray-200 rounded-lg p-2 mt-2" v-model="searchQuery" />
        <button type="button" @click="performSearch"
            class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            Search
        </button>


        {{ searchResults }}
    </div>
</template>

<script>
export default {
    // get the prop pickedLocation
    data() {
        return {
            searchQuery: '',
            searchResults: []
        }
    },
    methods: {
        async performSearch() {
            const searchQuery = await fetch('/jsbackend/placeSearch', {
                method: 'POST',
                body: JSON.stringify({
                    searchQuery: this.searchQuery
                })
            })

            this.searchResults = await searchQuery.json()

        }
    },
    props: {
        pickedLocation: {
            type: Object,
            required: false
        }
    },

}
</script>