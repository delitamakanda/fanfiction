<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <Loading v-if="remoteDataBusy" />
        
        <footer>
            <p>Copyright 2018 {{ title }} - <button type="button" @click="showRgpdModal">Politique de confidentialité</button> - <button type="button" @click="showModal">Mentions légales</button></p>
        </footer>

        <modal
          v-show="isModalVisible"
              @close="closeModal"
            >
            <h3 slot="header">Mentions légales</h3>
            <div slot="body">
                <vue-markdown v-for="item in legal" :key="item.id">{{ item.content }}</vue-markdown>
            </div>
        </modal>

        <modal
          v-show="isRgpdModalVisible"
              @close="closeRgpdModal"
            >
            <h3 slot="header">Politique de confidentialité</h3>
            <div slot="body">
                <vue-markdown v-for="item in rgpd" :key="item.id">{{ item.content }}</vue-markdown>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from './Modal.vue'
import VueMarkdown from 'vue-markdown'
import RemoteData from '../mixins/RemoteData'

export default {
    props: {
      title: {
        type: String,
        required: true,
      }
    },
    components: {
     modal,
     VueMarkdown,
   },
   mixins: [
       RemoteData({
           legal () {
               return 'pages/legal'
           },
           rgpd () {
               return 'pages/rgpd'
           },
       })
   ],
    data(){
        return{
          isModalVisible: false,
          isRgpdModalVisible: false,
          legal: [],
          rgpd: [],
          errorFetch: 'Il y a un problème avec la requète.'
        }
    },
    methods: {
      showModal () {
         this.isModalVisible = true;
      },

      showRgpdModal () {
          this.isRgpdModalVisible = true;
      },

      closeModal() {
         this.isModalVisible = false;
       },

       closeRgpdModal () {
           this.isRgpdModalVisible = false;
       }
    },
}
</script>

<style scoped>

footer {
    text-align: center;
    padding-top: 1rem;
    padding-bottom: 1rem;
}

</style>
