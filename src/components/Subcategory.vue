<template>
  <div>
    <h1>{{ subtitle }}</h1>
    <Loading v-if="loading" />

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="error" role="alert">
        {{ errorFetch }}
    </div>

    <h2 v-html="cats.name"></h2>
    <p v-html="cats.description"></p>

    <div v-for="subcat of subcats" v-if="subcat.category === cats.id">
        <h3 v-html="subcat.name"></h3>
        <img v-if="subcat.image" v-bind:src="subcat.image" />
        <p v-html="subcat.description"></p>
        
        <button
          type="button"
          class="btn"
          @click="showModal"
        >
          Voir les fanfictions
        </button>
        
        <modal
          v-show="isModalVisible"
          @close="closeModal"
        />
    </div>

  </div>
</template>

<script>
import modal from './components/Modal.vue';

export default {
  name: 'Subcategory',
  props: {
      id: {
          type: Number,
          required: true
      }
  },
  components: {
    modal,
  },
  data () {
    return {
      subtitle: '',
      error: null,
      subcats: [],
      cats: [],
      fics: [],
      loading: false,
      errorFetch: 'Il y a un problème avec la requète.',
      isModalVisible: false,
    }
    },
    async created () {
        this.loading = true
        try {
            this.subcats = await this.$fetch('subcategory')
            this.cats = await this.$fetch('category/' + this.$route.params.id)
            this.fics = await this.$fetch('fanfics')
        } catch (e) {
            this.error = e
        }
        this.loading = false
    },
    
    methods: {
    
      showModal() {
        this.isModalVisible = true;
      },
      
      closeModal() {
        this.isModalVisible = false;
      }
      
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
