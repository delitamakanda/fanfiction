<template>
    <footer>
        <p>Copyright 2018 {{ title }} - <a href="#">Politique de confidentialité</a> - <a @click="showModal">Mentions légales</a></p>
    </footer>
    
    <modal
      v-show="isModalVisible"
      @close="closeModal"
    >
    <h3 slot="header">Mentions légales</h3>
    <div slot="body">
        // TODO: 
    </div>
    </modal>
</template>

<script>
import modal from './Modal.vue';

export default {
    props: {
      title: {
        type: String,
        required: true,
      }
    },
    components: {
     modal,
   },
    data(){
        return{
          isModalVisible: false,
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
}

</style>
