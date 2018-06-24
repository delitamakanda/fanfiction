<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <Loading v-if="remoteDataBusy" />

        <vue-markdown v-for="item in rgpd" :key="item.id">{{ item.content }}</vue-markdown>
    </div>
</template>

<script>
import VueMarkdown from 'vue-markdown'
import RemoteData from '../mixins/RemoteData'

export default {
    name: 'RGPD',
    components: {
     VueMarkdown,
   },
   mixins: [
       RemoteData({
           rgpd () {
               return 'pages/rgpd'
           },
       })
   ],
    data(){
        return{
          rgpd: [],
          errorFetch: 'Il y a un problème avec la requète.'
        }
    },
}
</script>

<style scoped>
</style>
