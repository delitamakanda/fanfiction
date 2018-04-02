<template>
  <div>
    <h1>{{ subtitle }}</h1>

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        {{ errorFetch }}
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

    <pagination
        :total-pages="4"
        :total="5"
        :per-page="5"
        :current-page="this.currentPage"
        @pagechanged="onPageChange"
    />

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
        currentPage: 1,
        //error: null,
        //fanfics: [],
        //loading: false,
        //souscat: [],
        //remoteDataLoading: 42,
        errorFetch: 'Il y a un problème avec la requète.',
        }
    },
    /*async created () {
        this.loading = true
        try {
            this.fanfics = await this.$fetch('fanfics')
            this.souscat = await this.$fetch('subcategory')
        } catch (e) {
            this.error = e
        }
        this.loading = false
    },*/
    methods: {
        onPageChange(page) {
            console.log(page)
            this.currentPage = page
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
