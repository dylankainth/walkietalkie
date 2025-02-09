<template>
    <div>
        <audio controls ref="audio">
            <source src="https://file-examples.com/storage/fe91620ae767a4f0a97a5e9/2017/11/file_example_MP3_700KB.mp3"
                type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        {{ currentTime }}
    </div>
</template>

<script>
export default {
    computed: {


    }
}
</script>
