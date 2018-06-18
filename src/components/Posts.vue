<template>
  <div>
    <h1>{{ subtitle }}</h1>

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        {{ errorFetch }}
    </div>

    <section>
        <Loading v-if="remoteDataBusy" />

        <div v-for="item in postList">
                <router-link :to="{
                    name: 'PostDetail',
                    params: {
                      id: item.id
                    },
                }">
                    <h3>{{ item.title }}</h3>
                </router-link>
                <p> Par {{ item.user }}</p>
                <p> Publiée le {{ item.created | date }}</p>
                <a v-for="tag in item.tags" class="tag">
                    {{ tag.word }}
                </a>

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
      errorFetch: 'Il y a un problème avec la requète.'
    }
}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
