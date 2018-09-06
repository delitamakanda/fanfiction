<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <Loading v-if="remoteDataBusy" />

        <div class="px-6 py-4">
            <h2>Fanfictions de {{ this.$route.params.username }}</h2>
        </div>

        <article class="flex flex-wrap -mx-2">
            <div class="mb-4 w-full px-2 md:w-1/2" v-for="fic of fanfic" :key="fic.id">
                <router-link :to="{
                  name: 'Detail',
                  params: {
                    slug: fic.slug,
                    id: fic.id
                  },
                }"
                class="no-underline"
                >
                <div class="border border-grey-light bg-white rounded p-4 flex flex-col justify-between leading-normal">
                    <div class="mb-8">
                        <p class="text-sm text-grey-dark flex items-center">
                            {{ fic.category }} / {{ fic.subcategory }}
                        </p>
                        <div class="text-black font-bold text-xl mb-2">{{ fic.title }}</div>
                        <p v-if="fic.synopsis" class="text-grey-darker text-base">{{ fic.synopsis }}</p>
                    </div>
                    <div class="flex items-center">
                        <div class="text-sm">
                            <p class="text-grey-dark">Publié le : {{ fic.publish | date }}</p>
                            <p class="text-grey-dark">{{ fic.genres }} / {{ fic.classement }} / {{ fic.total_likes }} likes</p>
                        </div>
                    </div>
                </div>
                </router-link>
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
            required: false
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
