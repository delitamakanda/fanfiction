<template>
  <div>
    <h1>{{ subtitle }}</h1>

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        {{ errorFetch }}
    </div>

    <form class="align-center w-full max-w-sm">
        <div class="flex items-center py-2">
            <input class="appearance-none bg-transparent border-none w-full text-grey-darker mr-3 py-1 px-2 leading-tight" type="text" placeholder="Rechercher des fanfictions..." v-model="search_term" aria-label="Search">
            <button class="bg-teal hover:bg-teal-dark text-white font-bold py-2 px-4 rounded" @click.prevent="getSearchFanfics">Rechercher</button>
        </div>
  </form>

    <section>
        <Loading v-if="remoteDataBusy" />

        <article v-for="fanfic of fanficList">
            <router-link :to="{
              name: 'Detail',
              params: {
                slug: fanfic.slug,
                id: fanfic.id
              },
            }"
            class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker"
            >
            <h2>{{ fanfic.title }}</h2>
            </router-link>
            <p v-if="fanfic.synopsis" v-html="fanfic.synopsis"></p>
            <a @click="sortByCategory">{{ fanfic.category }}</a>
            <a @click="sortBySubCategory">{{ fanfic.subcategory }}</a>
            <router-link :to="{ name: 'ShowUserFanfic', params: { username: fanfic.author, slug: fanfic.slug, id: fanfic.id } }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ fanfic.author }}</router-link>
            <p>{{ fanfic.genres }} </p>
            <p>{{ fanfic.classement }}</p>
            <p> {{ fanfic.publish | date }}</p>
            <p>{{ fanfic.total_likes }} likes</p>
        </article>
    </section>

  </div>
</template>

<script>
import RemoteData from '../mixins/RemoteData'

export default {
  name: 'List',
  mixins: [
      RemoteData({
          fanficList: 'fanfics/v1',
      }),
  ],
  data () {
    return {
        subtitle: 'Lire des histoires',
        errorFetch: 'Il y a un problème avec la requète.',
        search_term: '',
        }
    },
    methods: {
      async getSearchFanfics () {

            try {
                this.fanficList = await this.$fetch(`fanfics/v1?search=${this.search_term}`)
            } catch (e) {
                this.errorFetch = e
            }
      },
      async sortByCategory () {

      },

      async sortBySubCategory () {

      },
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
