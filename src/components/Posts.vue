<template>
  <div>
    <h1>{{ subtitle }}</h1>

    <Loading v-if="loading" />

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="error" role="alert">
        Can't load the posts
    </div>

    <div v-for="post of posts.results">
            <router-link :to="{
                name: 'PostDetail',
                params: {
                  id: post.id
                },
            }">
                <h3 v-html="post.title"></h3>
            </router-link>
            <p v-html="post.user"></p>
            <p>{{ post.created | date }}</p>

    </div>

  </div>
</template>

<script>
export default {
  name: 'Posts',
  data () {
    return {
      subtitle: 'News',
      error: null,
      posts: [],
      loading: false,
    }
},

async created () {
    this.loading = true
    try {
        this.posts = await this.$fetch('posts')
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
