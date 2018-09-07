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
                            <vue-markdown :source="item.content" class="text-grey-darker text-base">{{ item.content.length > 10 ? item.content.substring(0, 10) + '...': '' }}</vue-markdown>
                        </div>
                        <div class="flex items-center">
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
import VueMarkdown from 'vue-markdown'

export default {
    name: 'Posts',
    components: {
     VueMarkdown,
   },
    mixins: [
        RemoteData({
            postList: 'posts',
        }),
    ],
    data () {
        return {
            errorFetch: 'Il y a un problème avec la requète.',
            maxCharacters: 15
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
