<template>
    <div>
        <Loading v-if="remoteDataBusy" />
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <section>
            <div class="max-w-md w-full lg:flex mb-4" v-for="item in postList" track-by="item.id">
                <div v-if="item.header" class="h-48 lg:h-auto lg:w-48 flex-none bg-cover rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden" :style="{backgroundImage: 'url(' + item.header + ')' }" :title="item.title">
                </div>
                <div v-else class="h-48 lg:h-auto lg:w-48 flex-none bg-cover rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden" :style="{backgroundColor: '#ddd' }" :title="item.title"></div>
                <router-link :to="{name: 'PostDetail', params: {slug: item.slug},}" class="no-underline">
                    <div class="border-r border-b border-l border-grey-light lg:border-l-0 lg:border-t lg:border-grey-light bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal">
                        <div class="mb-8">
                            <p class="text-sm text-grey-dark flex items-center">
                                <span v-for="tag in item.tags" class="inline-block bg-grey-lighter rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">
                                    #{{ tag.word }}
                                </span>
                            </p>
                            <div class="text-black font-bold text-xl mb-2">{{ item.title }}</div>
                            <p class="text-grey-darker text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
                        </div>
                        <div class="flex items-center">
                            <!--<img class="w-10 h-10 rounded-full mr-4" src="https://pbs.twimg.com/profile_images/885868801232961537/b1F6H4KC_400x400.jpg" alt="Avatar of Jonathan Reinink">-->
                            <div class="text-sm">
                                <p class="text-black leading-none">Par {{ item.user }}</p>
                                <p class="text-grey-dark">Publiée le {{ item.created | date }}</p>
                            </div>
                        </div>
                    </div>
                </router-link>
            </div>
        </section>
    </div>
</template>

<script>
import RemoteData from '../mixins/RemoteData'

export default {
    name: 'Posts',
    mixins: [
        RemoteData({
            postList: 'posts',
        }),
    ],
    data () {
        return {
            errorFetch: 'Il y a un problème avec la requète.'
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
