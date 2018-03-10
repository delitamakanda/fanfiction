<template>
  <div>
    <h1>{{ subtitle }}</h1>
    <Loading v-if="loading" />

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="error" role="alert">
        {{ errorFetch }}
    </div>

    <div v-for="category of categories">
        <router-link :to="{
              name: 'Subcategory',
              params: {
                id: category.id
              },
            }">
            <h3 v-html="category.name"></h3>
            <p v-html="category.description"></p>
        </router-link>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Category',
  data () {
    return {
      subtitle: 'Parcourir les catégories',
      error: null,
      categories: [],
      loading: false,
      errorFetch: 'Il y a un problème avec la requète.',
    }
    },
    async created () {
        this.loading = true
        try {
            this.categories = await this.$fetch('category')
        } catch (e) {
            this.error = e
        }
        this.loading = false
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
