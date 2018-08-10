<template>
  <div>
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

        <article class="rounded overflow-hidden" v-for="fanfic of fanficList">
            <div class="px-6 py-4">
                <div>
                    Publié le : {{ fanfic.publish | date }}
                </div>
                <div>
                    <span>{{ fanfic.category }}</span> /
                    <span>{{ fanfic.subcategory }}</span>
                </div>
                <router-link :to="{
                  name: 'Detail',
                  params: {
                    slug: fanfic.slug,
                    id: fanfic.id
                  },
                }"
                class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker"
                >
                <div class="font-bold text-xl mb-2">{{ fanfic.title }}</div>
                </router-link>
                <p v-if="fanfic.synopsis" v-html="fanfic.synopsis" class="text-grey-darker text-base"></p>
                Auteur: <router-link :to="{ name: 'ShowUserFanfic', params: { username: fanfic.author, slug: fanfic.slug, id: fanfic.id } }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ fanfic.author }}</router-link>
                <div>
                    <p>{{ fanfic.genres }} / {{ fanfic.classement }} / {{ fanfic.total_likes }} likes</p>
                    <p></p>
                    <p> </p>
                    <p></p>
                </div>
            </div>
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
          fanficList: 'fanfics/v1?category=&subcategory=&status=publié',
      }),
  ],
  data () {
    return {
        errorFetch: 'Il y a un problème avec la requète.',
        search_term: '',
        }
    },
    methods: {
      async getSearchFanfics () {

            try {
                this.fanficList = await this.$fetch(`fanfics/v1?category=&subcategory=&status=publié&search=${this.search_term}`)
            } catch (e) {
                this.errorFetch = e
            }
      },
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
