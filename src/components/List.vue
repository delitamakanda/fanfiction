<template>
  <div>
    <h1>{{ subtitle }}</h1>

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        Can't load the fics
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
            <p v-html="fanfic.author"></p>
            <p v-html="fanfic.genres"></p>
            <p> {{ moment(fanfic.publish).format('DD/MM/YYYY') }}</p>
            <p>{{ fanfic.likes }} likes</p>
        </article>
    </section>

  </div>
</template>

<script>
import moment from 'moment'
import RemoteData from '../mixins/RemoteData'

export default {
  name: 'List',
  mixins: [
      RemoteData({
          fanficList: 'fanfics',
      }),
  ],
  data () {
    return {
        subtitle: 'Lire des histoires',
        //error: null,
        //fanfics: [],
        //loading: false,
        //souscat: [],
        //remoteDataLoading: 42,
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
        moment,
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
