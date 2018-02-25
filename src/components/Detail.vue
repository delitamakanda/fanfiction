<template>
  <div>
    <h1></h1>

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="error" role="alert">
        Can't load the fic
    </div>

    <ul v-for="element of chapter.results" v-if="element.fanfic === fanfic.id">
        <li><a v-bind:href="'#' + element.id">{{ element.title }}</a></li>
    </ul>

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

            <div v-for="chap of chapter.results" v-if="chap.fanfic === fanfic.id">
                <h3 v-html="chap.title" :id="chap.id"></h3>

                <div v-if="chap.description !== ''" class="bg-blue-lightest border-t border-b border-blue text-blue-dark px-4 py-3" v-html="chap.description" role="alert">{{ chap.description }}</div>

                <div v-html="chap.text"></div>
            </div>
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
        chapter: [],
        date: null,
        }
    },
    async created () {
        try {
            const response = await fetch('/api/fanfics/' + this.$route.params.id)
            const res = await fetch('api/chapters');

            if (response.ok) {
                this.fanfic = await response.json()
                this.chapter = await res.json()
            } else {
                throw new Error('error')
            }
        } catch (e) {
            this.error = e
        }
    },
    methods: {
        moment
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
