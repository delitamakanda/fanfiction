<template>
    <div>
        <footer>
            <p>Copyright 2018 {{ title }} - <button type="button" @click="showPDC">Politique de confidentialité</button> - <button type="button" @click="showModal">Mentions légales</button></p>
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
          v-show="isModalPDCVisible"
              @close="closeModal"
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
           rgpd () {
               return 'pages/rgpd'
           },
           legal () {
               return 'pages/legal'
           }
       })
   ],
    data(){
        return{
          isModalVisible: false,
          isModalPDCVisible: false,
          legal: [],
          rgpd: [],
        }
    },
    methods: {
      showModal () {
         this.isModalVisible = true;
      },

      showPDC () {
          this.isModalPDCVisible = true;
      },

      closeModal() {
         this.isModalVisible = false;
         this.isModalPDCVisible = false;
       },
    },
}
</script>

<style scoped>

footer {
    text-align: center;
}

</style>
