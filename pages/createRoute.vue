<template>

    <div class="container mx-auto px-5 pt-3 pb-5">


        <p class="text-3xl">Create a route</p>
        <p class="text-lg text-gray-500">Oh, the places we'll go!</p>

        <div class="pt-5">
            <div class="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm text-center">
                <p class="font-bold text-lg text-gray-900">Your Location</p>

                <div v-if="location.status === 'waiting'">
                    <div class="pt-2 flex justify-center items-center">
                        <button @click="getLocation()" type="button"
                            class="text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                            Get my location</button>
                    </div>
                </div>

                <div v-if="location.status === 'loading'">

                    <div role="status">
                        <svg aria-hidden="true"
                            class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600 mx-auto"
                            viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                                fill="currentColor" />
                            <path
                                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                                fill="currentFill" />
                        </svg>
                        <span class="sr-only">Loading...</span>
                    </div>

                </div>



                <div v-if="location.status === 'success'">
                    <div class="pt-2">
                        <p class="text-gray-500">Latitude: {{ location.data.coords.latitude }}</p>
                        <p class="text-gray-500">Longitude: {{ location.data.coords.longitude }}</p>
                    </div>
                </div>

                <div v-if="location.status === 'error'">
                    <div class="pt-2">
                        <p class="text-red-500">Error getting location</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="pt-5">
            <div class="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm text-center">
                <p class="font-bold text-lg text-gray-900">Get those steps in?</p>
                <p class="text-gray-600 text-sm">Walking Distance: {{ walkingDistance < 1000 ? walkingDistance + 'm' :
                    (walkingDistance / 1000).toFixed(1) + 'km' }}</p>
                        <input id="default-range" type="range" v-model="walkingDistance" min="100" max="10000"
                            step="100" class="w-full h-2 bg-gray-200 rounded-lg  cursor-pointer">
            </div>
        </div>


        <div class="pt-5">
            <div class="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm text-center">
                <p class="font-bold text-lg text-gray-900">Where would you like to end the tour?</p>
                <button @click="setEndLocationToStart" type="button"
                    class="text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                    Same as start</button>
                <LocationPicker :pickedLocation="endLocation.data" />
            </div>
        </div>

        <div v-if="!loadedQuestions" class="pt-3">
            <div role="status">
                <svg aria-hidden="true"
                    class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600 mx-auto"
                    viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                        fill="currentColor" />
                    <path
                        d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                        fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
            </div>
        </div>


        <div v-if="loadedQuestions" class="pt-3 pb-20">

            <div v-for="question in questionsList" :key="question._id" class="pt-2">
                <div class="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm ">

                    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900">{{ question.questionText }}</h5>

                    <div v-if="question.responseType == 'multipleChoice'">
                        <div v-for="option in question.permittedResponses" :key="option" class="pt-2 inline-block">
                            <span @click="multipleChoiceSelectOption(question._id, option)"
                                :class="{ 'bg-blue-500 text-white': multipleChoiceIsSelected(question._id, option), 'bg-gray-200': !multipleChoiceIsSelected(question._id, option) }"
                                class="cursor-pointer px-3 py-1 rounded-full mr-2">
                                {{ option }}
                            </span>
                        </div>
                    </div>

                    <div v-if="question.responseType == 'multipleChoiceMultiple'">
                        <div v-for="option in question.permittedResponses" :key="option" class="pt-2 inline-block">
                            <span @click="multipleChoiceMultipleSelectOption(question._id, option)"
                                :class="{ 'bg-blue-500 text-white': multipleChoiceMultipleIsSelected(question._id, option), 'bg-gray-200': !multipleChoiceMultipleIsSelected(question._id, option) }"
                                class="cursor-pointer px-3 py-1 rounded-full mr-2">
                                {{ option }}
                            </span>
                        </div>
                    </div>

                    <div v-if="question.responseType == 'text'">
                        <input type="text" class="w-full border border-gray-200 rounded-lg p-2 mt-2"
                            v-model="question.answer" />
                    </div>
                </div>

            </div>

            <div class="pt-2">
                <button type="button" @click="submitRoute" v-if="loadedRoute == false"
                    class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                    Submit
                </button>
                <button type="button" v-if="loadedRoute == true"
                    class="disabled w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                    <div role="status">
                        <svg aria-hidden="true"
                            class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600 mx-auto"
                            viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                                fill="currentColor" />
                            <path
                                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                                fill="currentFill" />
                        </svg>
                        <span class="sr-only">Loading...</span>
                    </div>
                </button>
            </div>

        </div>


    </div>
</template>

<script>
export default {
    data() {
        return {
            loadedQuestions: false,
            loadedRoute: false,
            questionsList: [],
            endLocation: {
                data: null
            },
            location: {
                status: 'waiting',
                data: null,
            },
            walkingDistance: 2000
        }
    },
    methods: {
        async getLocation() {

            this.location.status = 'loading';
            try {
                const pos = await new Promise((resolve, reject) => {
                    navigator.geolocation.getCurrentPosition(resolve, reject);
                });
                this.location.data = pos;
                this.location.status = 'success';
            } catch (err) {
                this.location.status = 'error';
                console.error(err);
            }
        },
        setEndLocationToStart() {
            this.endLocation.data = this.location.data
        },
        submitRoute() {
            // for each in questionList, make sure that the answer is not empty
            const allQuestionsAnswered = this.questionsList.every(question => {
                if (question.responseType === 'multipleChoiceMultiple') {
                    return question.answer.length > 0
                }
                return question.answer !== ''
            })

            if (!allQuestionsAnswered) {
                alert('Please answer all questions')
                return
            } else {
                this.loadedRoute = true
                // send the answers to the server
                fetch('/api/createRoute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        questionsList: this.questionsList
                    })
                })

                // route the user to the route they made from the id returned by the server

            }
        },
        multipleChoiceMultipleSelectOption(questionId, option) {
            this.questionsList = this.questionsList.map(question => {
                if (question._id === questionId) {
                    if (question.answer.includes(option)) {
                        question.answer = question.answer.filter(answer => answer !== option)
                    } else {
                        question.answer.push(option)
                    }
                }
                return question
            })
        },
        multipleChoiceMultipleIsSelected(questionId, option) {
            const question = this.questionsList.find(question => question._id === questionId)
            if (question.answer.includes(option)) {
                return true
            }
            return false
        },
        multipleChoiceSelectOption(questionId, option) {
            // edit the 'selection' of questionsList with id of questionId
            this.questionsList = this.questionsList.map(question => {
                if (question._id === questionId) {
                    question.answer = option
                }
                return question
            })
        },
        multipleChoiceIsSelected(questionId, option) {
            // check if the 'selection' of questionsList with id of questionId is equal to option
            const question = this.questionsList.find(question => question._id === questionId)
            if (question.answer === option) {
                return true
            }
            return false
        }
    },
    async mounted() {

        const response = await fetch('/api/generateQuestions', {
            method: 'GET'
        })
        const responseData = await response.json()
        this.questionsList = responseData.body

        // for all in questionsList, add a new key 'answer' with value of [] if responseType is multipleChoiceMultiple
        this.questionsList = this.questionsList.map(question => {
            if (question.responseType === 'multipleChoiceMultiple') {
                question.answer = []
            }
            return question
        })

        this.loadedQuestions = true
    }
}
</script>