<template>
  <div>
    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        {{ errorFetch }}
    </div>

    <Loading v-if="remoteDataBusy" />

    <div class="overflow-hidden">
        <img v-if="post.header" :src="post.header" class="w-full" :alt="post.title" />
        <div class="px-6 py-4">
            <div class="font-bold text-xl mb-2"> {{ post.title }}</div>
            <p class="text-grey-darker text-base">Publié le {{ post.created | date }}</p>
            <vue-markdown :source="post.content" class="text-grey-darker text-base">{{ post.content }}</vue-markdown>
        </div>
        <div class="px-6 py-4">
            <span v-for="tag of post.tags" class="inline-block bg-grey-lighter rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">
                {{ tag.word }}
            </span>
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
