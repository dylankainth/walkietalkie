<script setup lang="ts">
definePageMeta({
    auth: { unauthenticatedOnly: true, navigateAuthenticatedTo: '/' }
})

const { signIn, status, data } = useAuth()
</script>

<template>
    <div>

        <div class="flex min-h-screen items-center justify-center">
            <div class="container mx-auto px-5 pt-3 pb-5">
                <div class="flex justify-center">
                    <div class="flex bg-gray-100 p-4 rounded-2xl shadow-md w-80">
                        <div class="w-full text-center">
                            <p class="font-bold text-lg text-gray-900">Log in</p>

                            <!-- add a signin with google button -->
                            <div class="pt-5">
                                <img src="/signinbutton.svg" alt="Sign in with Google" class=" h-70 mx-auto"
                                    @click="signIn('google')" />
                            </div>
                        </div>




                    </div>
                </div>
            </div>
        </div>


    </div>
</template>