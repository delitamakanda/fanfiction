<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <Loading v-if="remoteDataBusy" />

        <h1>{{ fanfic.title }}</h1>

        <div class="flex mb-4">
          <div class="w-3/4 h-12">
              <template v-if="$state.user && $state.user.id != null">
              <button type="button" @click="followAuthor" class="bg-teal hover:bg-teal-darker text-white font-bold py-2 px-4 rounded-full">Suivre l'auteur</button>

              <button type="button" @click="followFanfic" class="bg-teal hover:bg-teal-darker text-white font-bold py-2 px-4 rounded-full">Suivre l'histoire</button>
              </template>
          </div>
          <div class="w-1/4 h-12 text-right">
              <button type="button" @click.once="feedback" class="bg-teal hover:bg-teal-darker text-white font-bold py-2 px-4 rounded-full">Signaler</button>
          </div>
        </div>

        <div>
            {{ fanfic.category}} / {{ fanfic.subcategory }} / {{ fanfic.classement }} / Publiée le: {{fanfic.publish | date }} / {{ fanfic.genres }}
        </div>

        <div>
            Auteur : <router-link v-if="fanfic.author" :to="{ name: 'ShowUserFanfic', params: { username: fanfic.author, slug: fanfic.slug, id: fanfic.id } }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ fanfic.author }}</router-link> /
            <template v-if="$state.user && $state.user.id != null">
                <button type="button" class="bg-teal hover:bg-teal-darker text-white font-bold py-2 px-4 rounded-full" @click="favorite" v-if="fanfic_like == false">
                    <svgicon icon="mood-happy-solid" width="22" height="18" color="#fff"></svgicon> +1 /
                </button>

                <button type="button" class="bg-red hover:bg-red-darker text-white font-bold py-2 px-4 rounded-full" @click="unfavorite" v-if="fanfic_like == true">
                    <svgicon icon="mood-sad-solid" width="22" height="18" color="#fff"></svgicon> -1 /
                </button>
            </template>

            {{ fanfic.total_likes }} likes / {{ total_comments }} commentaire(s) (
            <button
            type="button"
            class="btn"
            @click="showModal"
            >
            Voir les commentaires )
        </button>
        </div>

    <div v-if="fanfic.description">
        <h4>Description</h4>
        <p v-html="fanfic.description"></p>
    </div>

    <div v-if="fanfic.synopsis">
        <h4>Synopsis</h4>
        <p>{{ fanfic.synopsis }}</p>
    </div>

    <div v-if="fanfic.credits">
        <h4>Crédits</h4>
        <p>{{ fanfic.credits }}</p>
    </div>

    <div class="flex mb-4">

        <div class="w-1/4">
            <affix class="sidebar-menu" relative-element-selector="#chapters-length">
                <ul v-for="element in chapter" v-if="element.fanfic === fanfic.id">
                    <li><a v-bind:href="'#' + element.id" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ element.title }}</a></li>
                </ul>
            </affix>
        </div>

        <div class="w-3/4" id="chapters-length">

            <div v-for="chap in chapter" v-if="chap.fanfic === fanfic.id">
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
        <div v-for="com in comment" v-if="comment">
            <span>{{ com.name }}</span> | Publié le : <span>{{ com.created | date }}</span>
            <div>{{ com.body }}</div>
            <hr/>
        </div>
        <div v-if="!comment.length">Cette fanfiction n'a pas encore de commentaires. Soyez le premier :)</div>
    </div>
    </modal>

    <div>
        <Form
            class="bg-white w-full max-w-lg"
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
    </div>
</div>
</template>

<script>
import modal from './Modal.vue'
import '../compiled-icons/mood-happy-solid'
import '../compiled-icons/mood-sad-solid'

import PersistantData from '../mixins/PersistantData'
import RemoteData from '../mixins/RemoteData'

export default {
    name: 'Detail',
    props: {
        id: {
            type: Number,
            required: false
        },
        slug: {
            type: String,
            required: true
        },
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
                return `fanfics/v1/${this.$route.params.slug}`
            },
            chapter () {
                return 'chapters'
            },
            comment () {
                return `comments/${this.$route.params.id}/fanfic`
            }
        }),
    ],
    data () {
        return {
            error: null,
            fanfic_like: false,
            fanfic: [],
            chapter: [],
            comment: [],
            date: null,
            errorFetch: 'Il y a un problème avec la requète.',
            isModalVisible: false,
            name: '',
            email: '',
            body: '',
            total_comments: '',
            happy: false,
        }
    },
    computed: {
        valid () {
            return !!this.name && !!this.body
        }
    },
    async created () {
        try {
            const res_comment = await this.$fetch(`comments/${this.$route.params.id}/fanfic`)

            if (res_comment) {
                this.comment = res_comment

                this.total_comments = res_comment.length

            } else {
                throw new Error('error')
            }

            for (var i = 0; i < this.fanfic.users_like.length; i++) {
                if (this.fanfic.users_like[i].username == this.$state.user.username) {
                    this.fanfic_like = true;
                } else {
                    this.fanfic_like = false;
                }
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
            this.happy = true
        },

        async unfavorite () {
            const result = await this.$fetch('unfavorite', {
                method: 'POST',
                body: JSON.stringify({
                    id: this.fanfic.id,
                    user: this.$state.user.id
                })
            })

            this.fanfic.total_likes--
            this.happy = false
        },

        followAuthor () {
            console.log("followAuthor");
        },

        showModal() {
            this.isModalVisible = true
        },

        closeModal() {
            this.isModalVisible = false
        },

        followFanfic () {
            console.log('followFanfic')
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

            this.total_comments++

        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.w-full {
    margin: 0 auto;
}

.pointer {
    cursor: pointer;
}
</style>
