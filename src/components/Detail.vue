<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <Loading v-if="remoteDataBusy" />


        <div class="px-6 py-4">
            <h1>{{ fanfic.title }}</h1>

            Auteur : <router-link v-if="fanfic.author" :to="{ name: 'ShowUserFanfic', params: { username: fanfic.author, slug: fanfic.slug, id: fanfic.id } }" class=" lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ fanfic.author }}</router-link>
        </div>

        <div v-if="step === 1">

            <div class="flex flex-wrap">
              <div class="md:w-3/4 sm:w-1/2 h-12 mb-4">
                  <template v-if="$state.user && $state.user.id != null">
                      <button type="button" @click="followAuthor" class="bg-teal hover:bg-teal-darker text-white font-bold py-2 px-4 rounded-full">Suivre l'auteur</button>

                      <button type="button" @click="followFanfic" class="bg-teal hover:bg-teal-darker text-white font-bold py-2 px-4 rounded-full">Suivre l'histoire</button>

                      <button type="button" class="bg-teal hover:bg-teal-darker text-white font-bold py-2 px-4 rounded-full" @click="favorite" v-if="fanfic_like == false">
                          <svgicon icon="mood-happy-solid" width="22" height="18" color="#fff"></svgicon> +1 /
                      </button>

                      <button type="button" class="bg-red hover:bg-red-darker text-white font-bold py-2 px-4 rounded-full" @click="unfavorite" v-if="fanfic_like == true">
                          <svgicon icon="mood-sad-solid" width="22" height="18" color="#fff"></svgicon> -1 /
                      </button>
                  </template>
              </div>
              <div class="md:w-1/4 sm:w-1/2 mb-4 h-12">
                  <button type="button" @click.once="feedback" class="bg-teal hover:bg-teal-darker text-white font-bold py-2 px-4 rounded-full">Signaler</button>
              </div>
            </div>

            <div class="px-6 py-4">
                <p>Publiée le: {{fanfic.publish | date }}</p>
                <p>{{ fanfic.category}} / {{ fanfic.subcategory }} / {{ fanfic.classement }} / {{ fanfic.genres }} / {{ fanfic.total_likes }} likes / <span class="lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" @click="showModal"><u>{{ total_comments }} commentaire(s)</u> </span></p>


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
            </div>

        <div class="flex flex-wrap">

            <div class="md:w-1/4">
                <affix class="sidebar-menu" relative-element-selector="#chapters-length">
                    <ul v-for="element in chapter" v-if="element.fanfic === fanfic.id">
                        <li>
                            <router-link :to="{ name: 'Chapter', params: {id: element.id, slug: fanfic.slug } }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ element.title }}</router-link>
                        </li>
                    </ul>
                </affix>
            </div>

            <div class="md:w-3/4 py-4 px-6" id="chapters-length">
                <router-view />
            </div>
        </div>

        <modal
        v-show="isModalVisible"
        @close="closeModal"
        >
        <h3 slot="header">Voir les commentaires</h3>
        <div slot="body">
            <a v-if="step === 1" @click="writeComment" class="block lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">Ecrire un commentaire</a>
            <div v-for="com in comment" v-if="comment">
                <span>{{ com.name }}</span> | Publié le : <span>{{ com.created | date }}</span>
                <div>{{ com.body }}</div>
                <hr/>
            </div>
            <div v-if="!comment.length">Cette fanfiction n'a pas encore de commentaires. Soyez le premier :)</div>
        </div>
        </modal>
    </div>

    <div v-if="step === 2">
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
            <a v-if="step === 2" @click="goStepBack" class="inline-block align-baseline font-bold text-sm text-blue hover:text-blue-darker">Retour au chapitre</a>
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
            step: 1,
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
        goStepBack () {
            this.step--;
        },
        async operation () {
            const result = await this.$fetch('comments/new', {
                method: 'POST',
                body: JSON.stringify({
                    name: this.name,
                    email: this.email,
                    body: this.body,
                    fanfic: this.fanfic.id,
                }),
            })
            this.goStepBack();
            this.name = this.email = this.body = '';
            this.total_comments++;
            this.comment.unshift(result);
        },
        writeComment () {
            this.step = 2;
        }
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
