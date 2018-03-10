<template>
  <div>
    <h1 v-html='post.title'></h1>

    <Loading v-if="loading" />

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="error" role="alert">
        {{ errorFetch }}
    </div>

    <p v-html='post.user'></p>
    <p v-html=''>{{ post.created | date }}</p>
    <p v-html='post.content'></p>



  </div>
</template>

<script>
export default {
  name: 'PostDetail',
  data () {
    return {
      error: null,
      post: [],
      loading: false,
      errorFetch: 'Il y a un problème avec la requète.',
    }
},

async created () {
    this.loading = true
    try {
        this.post = await this.$fetch('posts/' + this.$route.params.id)
    } catch (e) {
        this.error = e
    }
    this.loading = false
},
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
