<template>
  <div>
    <h1 v-html="fanfic.title"></h1>

    <p>{{ fanfic.category}} / {{ fanfic.subcategory }}</p>

    <p>{{ fanfic.classement }} <a @click="feedback" class="link" href="#">Signaler</a></p>

    <p>Auteur : {{ fanfic.author }}</p>
    <p>[ Publiée le: {{fanfic.publish | date }} ][ Mise à Jour le:{{ fanfic.updated | date }} ]</p>

    <p>{{ fanfic.genres }} / <a href="#" @click="favorite"><svgicon icon="heart" width="22" height="18" color="#ff33cc"></svgicon>{{ fanfic.likes }} likes</a> / <router-link :to="{ name: 'NewComment', params: {id: fanfic.id}}">Ajouter un commentaire</router-link> </p>

    <p v-html="fanfic.description"></p>
    <p v-html="fanfic.synopsis"></p>
    <p v-html="fanfic.credits"></p>

    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="error" role="alert">
        {{ errorFetch }}
    </div>

    <div class="flex mb-4">

        <div class="w-1/4">
            <affix class="sidebar-menu" relative-element-selector="#chapters-length">
                <ul v-for="element of chapter" v-if="element.fanfic === fanfic.id">
                    <li><a v-bind:href="'#' + element.id">{{ element.title }}</a></li>
                </ul>
            </affix>
        </div>

        <div class="w-3/4" id="chapters-length">

            <div v-for="chap of chapter" v-if="chap.fanfic === fanfic.id">
                <h3 v-html="chap.title" :id="chap.id"></h3>

                <div v-if="chap.description !== ''" class="bg-blue-lightest border-t border-b border-blue text-blue-dark px-4 py-3" v-html="chap.description" role="alert">{{ chap.description }}</div>

                <div v-html="chap.text"></div>
            </div>
        </div>
    </div>

  </div>
</template>

<script>
import '../compiled-icons/heart'

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
            let message = confirm("Seuls les fanfictions ne répondant pas à la charte de bonne conduite du site seront supprimées.");
            if (message === true) {
              const result = await this.$fetch('feedback', {
                  method: 'POST',
                  body: JSON.stringify({
                      id: this.fanfic.id,
                  })
              })
            }
        },

        async favorite () {
            const result = await this.$fetch('favorite', {
                method: 'POST',
                body: JSON.stringify({
                    id: this.fanfic.id,
                })
            })
            this.fanfic.likes++;
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
