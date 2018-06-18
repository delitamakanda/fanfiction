<template>
    <div>
        <footer>
            <p>Copyright 2018 {{ title }} - <a href="#" @click="showPDC">Politique de confidentialité</a> - <a  href="#" @click="showModal">Mentions légales</a></p>
        </footer>

        <modal
          v-show="isModalVisible"
              @close="closeModal"
            >
            <h3 slot="header">Mentions légales</h3>
            <div slot="body">
                <vue-markdown>## this is the default slot 1</vue-markdown>
            </div>
        </modal>

        <modal
          v-show="isModalPDCVisible"
              @close="closeModal"
            >
            <h3 slot="header">Politique de confidentialité</h3>
            <div slot="body">
                <vue-markdown>## this is the default slot 2</vue-markdown>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from './Modal.vue';
import VueMarkdown from 'vue-markdown';

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
    data(){
        return{
          isModalVisible: false,
          isModalPDCVisible: false,
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
