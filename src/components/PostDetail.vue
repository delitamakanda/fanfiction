<template>
  <div>
    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        {{ errorFetch }}
    </div>

    <Loading v-if="remoteDataBusy" />

    <div class="overflow-hidden bg-white rounded">
        <img v-if="post.header" :src="post.header" class="w-full" :alt="post.title" />
        <div class="px-6 py-4">
            <div class="mb-8">
                <p class="text-sm text-grey-dark flex items-center">
                    <span v-for="tag of post.tags" class="inline-block bg-grey-lighter rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">
                        {{ tag.word }}
                    </span>
                </p>
            </div>
            <div class="font-bold text-xl mb-2"> {{ post.title }}</div>
            <vue-markdown :source="post.content" class="text-grey-darker text-base">{{ post.content }}</vue-markdown>
        </div>
        <div class="px-6 py-4">
            <div class="flex items-center">
                <!--<img class="w-10 h-10 rounded-full mr-4" src="https://pbs.twimg.com/profile_images/885868801232961537/b1F6H4KC_400x400.jpg" alt="Avatar of Jonathan Reinink">-->
                <div class="text-sm">
                    <p class="text-black leading-none">Par {{ post.user }}</p>
                    <p class="text-grey-dark">Publiée le {{ post.created | date }}</p>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import RemoteData from '../mixins/RemoteData'
import VueMarkdown from 'vue-markdown'

export default {
  name: 'PostDetail',
  components: {
   VueMarkdown,
 },
  mixins: [
      RemoteData({
          post () {
              return`posts/${this.$route.params.slug}`
          }
      })
  ],
  data () {
    return {
        errorFetch: 'Il y a un problème avec la requète.',
        post: [],
    }
},
props: {
    slug: {
        type: String,
        required: true,
    },
},

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
