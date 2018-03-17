<template>
  <div>
    <h1 v-html="fanfic.title"></h1>

    <a @click="feedback">Signaler</a>

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="error" role="alert">
        {{ errorFetch }}
    </div>

    <ul v-for="element of chapter" v-if="element.fanfic === fanfic.id">
        <li><a v-bind:href="'#' + element.id">{{ element.title }}</a></li>
    </ul>

    <section>
            <p v-html="fanfic.category"></p>
            <p v-html="fanfic.subcategory"></p>
            <p v-html="fanfic.author"></p>
            <p>{{fanfic.publish | date }}</p>
            <p>{{ fanfic.updated | date }}</p>
            <p v-html="fanfic.synopsis"></p>
            <p>{{ fanfic.likes }} likes</p>
            <p v-html="fanfic.genres"></p>
            <p v-html="fanfic.classement"></p>
            <p v-html="fanfic.description"></p>
            <p v-html="fanfic.credits"></p>

            <div v-for="chap of chapter" v-if="chap.fanfic === fanfic.id">
                <h3 v-html="chap.title" :id="chap.id"></h3>

                <div v-if="chap.description !== ''" class="bg-blue-lightest border-t border-b border-blue text-blue-dark px-4 py-3" v-html="chap.description" role="alert">{{ chap.description }}</div>

                <div v-html="chap.text"></div>
            </div>
    </section>

  </div>
</template>

<script>
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
        errorFetch: 'Il y a un problème avec la requète.',
        }
    },
    async created () {
        try {
            const response = await fetch('/api/fanfics/v1/' + this.$route.params.id)
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
        async feedback () {
            const result = await fetch('api/feedback')
            console.log(result)
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
