<template>
  <div>
    <h1>{{ subtitle }}</h1>

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="error" role="alert">
        Can't load the fics
    </div>

    <section>
        <article v-for="fanfic of fanfics.results">
            <router-link :to="{
              name: 'Detail',
              params: {
                id: fanfic.id
              },
            }">
            <h2 v-html="fanfic.title"></h2>
            </router-link>
            <p v-html="fanfic.author"></p>
        </article>
    </section>

  </div>
</template>

<script>
export default {
  name: 'List',
  data () {
    return {
        subtitle: 'Lire des histoires',
        error: null,
        fanfics: [],
        }
    },
    async created () {
        try {
            const response = await fetch('/api/fanfics')
            if (response.ok) {
                this.fanfics = await response.json()
            } else {
                throw new Error('error')
            }
        } catch (e) {
            this.error = e
        } finally {

        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
