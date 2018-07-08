<template>
  <div>
    <h1>{{ subtitle }}</h1>

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        {{ errorFetch }}
    </div>

    <section>
        <Loading v-if="remoteDataBusy" />

        <div class="overflow-hidden" v-for="item in postList">
            <div class="px-6 py-4">
                <div class="font-bold text-xl mb-2">
                    <router-link :to="{
                        name: 'PostDetail',
                        params: {
                          slug: item.slug
                        },
                    }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">
                        <h3>{{ item.title }}</h3>
                    </router-link>
                </div>
                <p class="text-grey-darker text-base"> Par {{ item.user }}</p>
                <p class="text-grey-darker text-base"> Publiée le {{ item.created | date }}</p>
            </div>
            <div class="px-6 py-4">
                <span v-for="tag in item.tags" class="inline-block bg-grey-lighter rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">
                    {{ tag.word }}
                </span>
            </div>
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
