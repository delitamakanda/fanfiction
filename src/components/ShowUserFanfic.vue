<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <Loading v-if="remoteDataBusy" />

        <h2>Fanfictions de {{ this.$route.params.username }}</h2>

        <article v-for="fic of fanfic">
            <router-link :to="{
              name: 'Detail',
              params: {
                slug: fic.slug,
                id: fic.id
              },
            }"
            class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker"
            >
                <h3>{{ fic.title }}</h3>
            </router-link>
            <p v-if="fic.synopsis">{{ fic.synopsis }}</p>
            <p>{{ fic.category }}</p>
            <p>{{ fic.subcategory }}</p>
            <p>{{ fic.genres }} </p>
            <p>{{ fic.classement }}</p>
            <p> {{ fic.publish | date }}</p>
            <p>{{ fic.total_likes }} likes</p>
        </article>

    </div>
</template>

<script>
import RemoteData from '../mixins/RemoteData'

export default {
    name: 'ShowUserFanfic',
    props: {
        username: {
            type: String,
            required: true
        },
        slug: {
            type: String,
            required: true
        },
        id: {
            type: Number,
            required: false
        }
    },
    mixins: [
        RemoteData({
            fanfic () {
               return `fanfics/v1/author/${this.$route.params.username}`
           },
       })
   ],
    data(){
        return{
          fanfic: [],
          errorFetch: 'Il y a un problème avec la requète.'
        }
    },
}
</script>

<style scoped>
</style>
