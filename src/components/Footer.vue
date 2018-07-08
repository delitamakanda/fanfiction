<template>
    <div>
        <footer>
            <p>Copyright 2018 {{ title }} - <router-link :to="{ name: 'RGPD'}"><button type="button">Politique de confidentialité</button></router-link> - <button type="button" @click="showModal">Mentions légales</button></p>
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
           }
       })
   ],
    data(){
        return{
          isModalVisible: false,
          legal: [],
        }
    },
    methods: {
      showModal () {
         this.isModalVisible = true;
      },

      closeModal() {
         this.isModalVisible = false;
       },
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
