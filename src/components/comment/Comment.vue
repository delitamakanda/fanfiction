<template>
<div>
    <div class="lg:ml-20 lg:mr-48" v-for="comment in comments" :key="comment.id">
        <div class="flex mt-3">
            <div class="lg:w-3/5 w-full">
                <div class="bg-white shadow mt-4 p-3 pb-1 relative">
                    <div class="flex items-center">
                        <div>
                            <h5>
                                {{ comment.name }}
                                <span class="text-gray-600 text-sm" v-if="isPrivate && comment.email">
                                {{ comment.email }}
                                </span>
                                sur
                                <router-link class="text-blue no-underline hover:underline" :to="{
                                    name: 'Detail',
                                    params: {
                                        slug: comment.fanfic.slug,
                                        id: comment.fanfic.id
                                    },
                                }">
                                {{ comment.fanfic.title }}
                                </router-link>
                                .
                            </h5>
                            <p class="text-xs font-normal text-grey mt-1">
                                <span class="cursor-pointer hover:underline">
                                {{ comment.created | date }}
                                </span>
                                ·
                                <span class="cursor-pointer hover:underline">
                                {{ comment.chapter.title }}
                                </span>
                            </p>
                        </div>
                    </div>
                    <div class="absolute pin-r pin-t mt-3 mr-3">
                        <svg class="w-4 h-4 text-right" viewbox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg">
                            <path d="M576 736v192q0 40-28 68t-68 28h-192q-40 0-68-28t-28-68v-192q0-40 28-68t68-28h192q40 0 68 28t28 68zm512 0v192q0 40-28 68t-68 28h-192q-40 0-68-28t-28-68v-192q0-40 28-68t68-28h192q40 0 68 28t28 68zm512 0v192q0 40-28 68t-68 28h-192q-40 0-68-28t-28-68v-192q0-40 28-68t68-28h192q40 0 68 28t28 68z">
                            </path>
                        </svg>
                    </div>
                    <h5 class="text-sm font-normal my-3">
                        {{ comment.body }}
                    </h5>
                    <!-- <div class="border">
                        <img alt="" src="https://scontent-sit4-1.xx.fbcdn.net/v/t1.0-0/p526x296/24796353_1561364460621145_3004549137840390947_n.jpg?oh=e9c249e251879520538cc3a924ee7711&oe=5B1DD598">
                    </div>
                    <div class="flex py-1">
                        <button class="appearance-none flex-1 flex items-center justify-center py-2 text-center text-red hover:bg-grey-lighter">
                            <svg class="w-4 h-4 mr-1" id="Layer_1" style="enable-background:new 0 0 496.158 496.158;" version="1.1" viewbox="0 0 496.158 496.158" x="0px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" y="0px">
                                <path d="M0,248.085C0,111.063,111.069,0.003,248.075,0.003c137.013,0,248.083,111.061,248.083,248.082
                                    c0,137.002-111.07,248.07-248.083,248.07C111.069,496.155,0,385.087,0,248.085z" style="fill:#E04F5F;">
                                </path>
                                <path d="M374.116,155.145c-34.799-34.8-91.223-34.8-126.022,0h-0.029c-34.801-34.8-91.224-34.8-126.023,0
                                    c-34.801,34.8-29.783,86.842,0,126.022c31.541,41.491,89.129,109.944,126.023,109.944h0.029c36.895,0,94.481-68.453,126.022-109.944
                                    C403.9,241.988,408.916,189.946,374.116,155.145z" style="fill:#FFFFFF;">
                                </path>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                                <g>
                                </g>
                            </svg>
                            Love
                        </button>
                    </div> -->
                    
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    props: {
        comments: Array,
        isPrivate: Boolean
    },
    data: () => ({
    }),
    computed: {
    },
    methods: {

    },
    components: {  }
}
</script>

<style scoped>

</style>
