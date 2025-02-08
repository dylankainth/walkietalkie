<script setup>

const { data } = useAuth()
</script>

<template>
    <div class="flex min-h-screen">
        <div class="container mx-auto px-5 pt-3 pb-5">
            <div class="flex justify-center">
                <div class="flex items-center bg-gray-100 p-4 rounded-2xl shadow-md w-80">
                    <img class="w-16 h-16 bg-gray-300 mr-4 rounded-full" :src="data.user.image" alt="Avatar">
                    <div class="px-2">
                        <p class="font-bold text-lg text-gray-900">{{ data.user.name }}</p>
                        <p class="text-gray-600 text-sm">{{ data.user.email }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>


</template>

<style scoped>
/* Additional custom styles if needed */
</style>