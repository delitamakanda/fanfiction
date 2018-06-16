<template>
  <div>
    <h1 v-html="fanfic.title"></h1>

    <p>{{ fanfic.category}} / {{ fanfic.subcategory }}</p>

    <p>{{ fanfic.classement }} <a @click="feedback" class="link" href="#">Signaler</a></p>

    <p>Auteur : {{ fanfic.author }}</p>
    <p>[ Publiée le: {{fanfic.publish | date }} ][ Mise à Jour le:{{ fanfic.updated | date }} ]</p>

    <p>
        {{ fanfic.genres }} /
        <a href="#" @click="favorite"><svgicon icon="heart" width="22" height="18" color="#ff33cc"></svgicon>{{ fanfic.total_likes }} likes</a> /
        <span v-if="comment.results.length <= 1">{{ comment.results.length }} commentaire</span>
        <span v-else>{{ comment.results.length }} commentaires</span> /
        <a @click="onPrint" class="link" href="#">Vue imprimable</a> /
        <button
           type="button"
           class="btn"
           @click="showModal"
         >
           Voir les commentaires
         </button> /
         <a @click="followFanfic" class="link" href="#">Suivre l'histoire</a>
    </p>

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

    <modal
      v-show="isModalVisible"
      @close="closeModal"
    >
    <h3 slot="header">Voir les commentaires</h3>
    <div slot="body">
        <Form
        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
        title="Nouveau commentaire"
        :operation="operation"
        :valid="valid">
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="name">
                  Nom ou Pseudo
                </label>
                <Input
                    name="name"
                    v-model="name"
                    placeholder=""
                    maxlength="255"
                    required />
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="email">
                  E-mail
                </label>
                <Input
                    name="email"
                    v-model="email"
                    placeholder="Votre e-mail (seul l'auteur le verra)"
                    maxlength="255" />
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="body">
                  Commentaire
                </label>
                <Input
                    type="textarea"
                    name="body"
                    v-model="body"
                    placeholder=""
                    rows="6"
                    required />
            </div>
            <template slot="actions">
                <button
                    type="submit"
                    class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                    :disabled="!valid">
                    Ajouter un commentaire
                </button>
            </template>
        </Form>
        <div v-for="com of comment.results" v-if="comment.results">
            <span>{{ com.name }}</span> <span v-if="com.email"> | {{ com.email }} </span> | Publié le : <span>{{ com.created | date }}</span>
            <div>{{ com.body }}</div>
            <hr/>
        </div>
        <div v-if="!comment.results">Cette fanfiction n'a pas encore de commentaires. Soyez le premier :)</div>
    </div>
    </modal>

  </div>
</template>

<script>
import modal from './Modal.vue'
import '../compiled-icons/heart'

import PersistantData from '../mixins/PersistantData'
import RemoteData from '../mixins/RemoteData'

export default {
  name: 'Detail',
  props: {
      id: {
          type: Number,
          required: true
      }
  },
  components: {
     modal,
   },
  mixins: [
      PersistantData('NewComment', [
          'name',
          'email',
          'body',
      ]),
      RemoteData({
          fanfic () {
              return `fanfics/${this.$route.params.id}`
          },
      }),
  ],
  data () {
    return {
        error: null,
        fanfic: [],
        chapter: [],
        comment: [],
        date: null,
        errorFetch: 'Il y a un problème avec la requète.',
        isModalVisible: false,
        name: '',
        email: '',
        body: '',
        }
    },
    computed: {
        valid () {
            return !!this.name && !!this.body
        }
    },
    async created () {
        try {
            const response = await fetch('/api/fanfics/v1/' + this.$route.params.id)
            const res = await fetch('api/chapters')
            const res_comment = await this.$fetch(`comments/${this.$route.params.id}/fanfic`)

            if (response.ok) {
                this.fanfic = await response.json()
                this.chapter = await res.json()
                this.comment = res_comment
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
                    user: this.$state.user.id
                })
            })
            this.fanfic.total_likes++
        },

        onPrint () {
          console.log('print')
        },

        showModal() {
         this.isModalVisible = true
       },

       closeModal() {
         this.isModalVisible = false
       },

       followFanfic () {
        console.log('follow')
       },

       async operation () {
            const result = await this.$fetch('comments/new', {
                method: 'POST',
                body: JSON.stringify({
                    name: this.name,
                    email: this.email,
                    body: this.body,
                    fanfic: this.$route.params.id,
                }),
            })
            this.name = this.email = this.body = ''
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.w-full {
    margin: 0 auto;
}
</style>
