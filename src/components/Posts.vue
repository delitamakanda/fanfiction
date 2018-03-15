<template>
  <div>
    <h1>{{ subtitle }}</h1>

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        {{ errorFetch }}
    </div>

    <section>
        <Loading v-if="remoteDataBusy" />

        <div v-for="post of postList">
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
      subtitle: 'News',
      // error: null,
      // loading: false,
      errorFetch: 'Il y a un problème avec la requète.'
    }
}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
