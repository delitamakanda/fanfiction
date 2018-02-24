<template>
  <div>
    <h1></h1>

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="error" role="alert">
        Can't load the fic
    </div>

    <section>
            <h2 v-html="fanfic.title"></h2>
            <p v-html="fanfic.category"></p>
            <p v-html="fanfic.subcategory"></p>
            <p v-html="fanfic.author"></p>
            <p>{{ moment(fanfic.publish).format('DD/MM/YYYY')}}</p>
            <p>{{ moment(fanfic.updated).format('DD/MM/YYYY')}}</p>
            <p v-html="fanfic.synopsis"></p>
            <p>{{ fanfic.likes }} likes</p>
            <p v-html="fanfic.genres"></p>
            <p v-html="fanfic.classement"></p>
            <p v-html="fanfic.description"></p>
            <p v-html="fanfic.credits"></p>
    </section>

  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'Detail',
  props: {
      id: {
          type: Number,
          required: true
      }
  },
  data () {
    return {
        error: null,
        fanfic: [],
        date: null,
        }
    },
    async created () {
        try {
            const response = await fetch('/api/fanfics/' + this.$route.params.id)
            if (response.ok) {
                this.fanfic = await response.json()
                console.log(this.fanfic);
            } else {
                throw new Error('error')
            }
        } catch (e) {
            this.error = e
        } finally {

        }
    },
    methods: {
        moment
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
