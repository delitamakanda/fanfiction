<template>
    <div>
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
        }
    },
}
</script>

<style scoped>
</style>
