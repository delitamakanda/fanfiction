<template>
  <div>
    <h1>{{ subtitle }}</h1>

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        {{ errorFetch }}
    </div>

    <div class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="text" placeholder="Rechercher des fanfictions..." v-model="search_term" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" @click.prevent="getFanfics">Rechercher</button>
    </div>

    <section>
        <Loading v-if="remoteDataBusy" />

        <article v-for="fanfic of fanficList">
            <router-link :to="{
              name: 'Detail',
              params: {
                id: fanfic.id
              },
            }">
            <h2 v-html="fanfic.title"></h2>
            </router-link>
            <p v-if="fanfic.synopsis" v-html="fanfic.synopsis"></p>
            <p v-html="fanfic.author"></p>
            <p v-html="fanfic.genres"></p>
            <p v-html="fanfic.classement"></p>
            <p> {{ fanfic.publish | date }}</p>
            <p>{{ fanfic.likes }} likes</p>
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
      async getFanfics () {

            try {
                this.fanficList = await this.$fetch(`fanfics/v1?search=${this.search_term}`)
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
