<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <Loading v-if="remoteDataBusy" />

        <div class="px-6 py-4">
            <h2>Fanfictions de {{ this.$route.params.username }}</h2>
        </div>

        <article class="rounded overflow-hidden" v-for="fic of fanfic">
            <div class="px-6 py-4">
                <div>
                    Publié le : {{ fic.publish | date }}
                </div>
                <div>
                    <span>{{ fic.category }}</span> /
                    <span>{{ fic.subcategory }}</span>
                </div>
                <router-link :to="{
                  name: 'Detail',
                  params: {
                    slug: fic.slug,
                    id: fic.id
                  },
                }"
                class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker"
                >
                    <div class="font-bold text-xl mb-2">{{ fic.title }}</div>
                </router-link>
                <p v-if="fic.synopsis" class="text-grey-darker text-base">{{ fic.synopsis }}</p>
                <div>
                    <p>{{ fic.genres }} / {{ fic.classement }} / {{ fic.total_likes }} likes</p>
                </div>
            </div>
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
