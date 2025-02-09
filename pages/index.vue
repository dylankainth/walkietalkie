<template>

    <div class="flex items-center justify-center min-h-screen">
        <div class="container mx-auto px-5 pt-3 pb-5">
            <div class="hero text-center my-10">
                <img src="/logo.svg" alt="Everyday Tourist Logo" class="w-32 h-32 mx-auto" />
                <h1 class="text-5xl font-bold">WalkieTalkie</h1>
                <p class="text-xl mt-4">Your AI Tour Guide</p>

                <div class="mt-10">
                    <NuxtLink to="/routes" type="button"
                        class="text-white bg-columbia-600 hover:bg-columbia-700 focus:ring-4 focus:ring-columbia-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-columbia-600 dark:hover:bg-columbia-700 focus:outline-none dark:focus:ring-columbia-800">
                        Get Started</NuxtLink>

                </div>
            </div>

        </div>
    </div>
</template>