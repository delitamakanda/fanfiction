<template>
  <div>
    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        {{ errorFetch }}
    </div>

    <Loading v-if="remoteDataBusy" />

    <h1> {{ post.title }}</h1>
    <p>Ecrit par {{ post.user }}</p>
    <p>Publié le {{ post.created | date }}</p>
    <p v-html='post.content'></p>

    <a v-for="tag of post.tags" class="tag">
        {{ tag.word }}
    </a>
  </div>
</template>

<script>
import RemoteData from '../mixins/RemoteData'

export default {
  name: 'PostDetail',
  mixins: [
      RemoteData({
          post () {
              return`posts/${this.$route.params.id}`
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
    id: {
        type: Number,
        required: true,
    },
},

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
