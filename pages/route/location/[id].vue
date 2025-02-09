<template>
    <div>
        <div v-if="loading">
            <p>Loading...</p>
        </div>
        <div v-if="!loading && placeInfo"> <audio ref="audioPlayer" controls autoplay loop
                :src="'data:audio/mp3;base64,' + placeInfo.data.audio_file" @timeupdate="updateCurrentTime"> </audio>

            <h1>Transcript</h1>
            <p>
                <span v-for="(timedWord, index) in placeInfo.data.transcript_file" :key="index"> <span
                        :class="{ 'highlighted': currentTime >= timedWord.start_time }"> {{ timedWord.word }}
                    </span>
                    <span> </span> </span>
            </p>
        </div>
    </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';

export default {
    setup() {
        const audioPlayer = ref(null);
        const currentTime = ref(0);

        const updateCurrentTime = () => {
            if (audioPlayer.value) {
                currentTime.value = audioPlayer.value.currentTime;
            }
        };

        return { audioPlayer, currentTime, updateCurrentTime }; // Return reactive data
    },
    data() {
        return {
            loading: true,
            placeInfo: null
        };
    },
    mounted() {
        this.fetchPlaceInfo();
    },
    methods: {
        async fetchPlaceInfo() {
            this.loading = true;
            try {
                const placeInfoData = await fetch("/api/createLocationTrack", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        place_name: "Queenstown Gondala"
                    })
                });

                if (!placeInfoData.ok) {
                    throw new Error(`HTTP error! status: ${placeInfoData.status}`); // Handle errors
                }

                this.placeInfo = await placeInfoData.json();
            } catch (error) {
                console.error("Error fetching place info:", error);
                // Handle the error, e.g., display an error message
                this.errorMessage = "Error loading data. Please try again later."
            } finally {
                this.loading = false;
            }
        },
    }
};
</script>

<style scoped>
.highlighted {
    font-weight: bold;
}
</style>