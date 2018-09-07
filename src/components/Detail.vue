<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <Loading v-if="remoteDataBusy" />

        <div class="w-full">
          <div class="px-6 py-4">
            <div class="font-bold text-xl mb-2">{{ fanfic.title }}</div>
            <p class="text-grey-darker text-base">
              Par <router-link v-if="fanfic.author" :to="{ name: 'ShowUserFanfic', params: { username: fanfic.author, slug: fanfic.slug, id: fanfic.id } }" class=" lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ fanfic.author }}</router-link>
            </p>
          </div>
        </div>

        <div v-if="step === 1">

            <div class="flex flex-wrap">
              <div class="md:w-3/4 sm:w-1/2 h-12 mb-4">
                  <template v-if="$state.user && $state.user.id != null">
                      <button v-if="!followUser" type="button" @click="followAuthor" class="bg-teal hover:bg-teal-darker text-white font-bold py-2 px-4 rounded-full">Suivre l'auteur</button>

                      <button v-if="followUser" type="button" @click="DisFollowAuthor" class="bg-red hover:bg-red-darker text-white font-bold py-2 px-4 rounded-full">Ne plus suivre l'auteur</button>

                      <button v-if="!followStory" type="button" @click="followFanfic" class="bg-teal hover:bg-teal-darker text-white font-bold py-2 px-4 rounded-full">Suivre l'histoire</button>

                      <button v-if="followStory" type="button" @click="DisFollowFanfic" class="bg-red hover:bg-red-darker text-white font-bold py-2 px-4 rounded-full">Ne plus suivre l'histoire</button>

                      <button type="button" class="bg-teal hover:bg-teal-darker text-white font-bold py-2 px-4 rounded-full" @click="favorite" v-if="!like">
                          <svgicon icon="mood-happy-solid" width="22" height="18" color="#fff"></svgicon> +1 /
                      </button>

                      <button type="button" class="bg-red hover:bg-red-darker text-white font-bold py-2 px-4 rounded-full" @click="unfavorite" v-if="like">
                          <svgicon icon="mood-sad-solid" width="22" height="18" color="#fff"></svgicon> -1 /
                      </button>
                  </template>
              </div>
              <div class="md:w-1/4 sm:w-1/2 mb-4 h-12">
                  <button type="button" @click.once="feedback" class="bg-teal hover:bg-teal-darker text-white font-bold py-2 px-4 rounded-full">Signaler</button>
              </div>
            </div>

            <div class="w-full rounded overflow-hidden shadow">
                <div class="px-6 py-4">
                    <p class="text-grey-darker text-base">Publiée le: {{fanfic.publish | date }}</p>
                    <p class="text-grey-darker text-base">Mise à jour : {{ fanfic.updated | date }}</p>
                    <div class="text-grey-darker text-base" v-if="fanfic.description">
                        <h4>Description</h4>
                        <p v-html="fanfic.description"></p>
                    </div>
                    <div class="text-grey-darker text-base"  v-if="fanfic.synopsis">
                        <h4>Synopsis</h4>
                        <p>{{ fanfic.synopsis }}</p>
                    </div>
                    <div class="text-grey-darker text-base"  v-if="fanfic.credits">
                        <h4>Crédits</h4>
                        <p>{{ fanfic.credits }}</p>
                    </div>
                </div>
                <div class="px-6 py-4">
                    <span class="inline-block bg-grey-lighter rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">{{ fanfic.category}}</span>
                    <span class="inline-block bg-grey-lighter rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">{{ fanfic.subcategory }}</span>
                    <span class="inline-block bg-grey-lighter rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">{{ fanfic.classement }} </span>
                    <span class="inline-block bg-grey-lighter rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">{{ fanfic.genres }} </span>
                    <span class="inline-block bg-grey-lighter rounded-full px-3 py-1 text-sm font-semibold text-grey-darker">{{ fanfic.total_likes }} likes</span>
                    <span class="lg:inline-block lg:mt-0 text-teal hover:text-teal-darker pointer" @click="showModal"><u>{{ total_comments }} commentaire(s)</u> </span>
                  </div>
            </div>

        <div class="flex flex-wrap mt-4">
            <aside class="w-full md:w-1/4 ">
                <div class="sidebar-menu ">
                    <ul v-for="(element, index) in chapterList">
                        <li :key="index">
                            <span @click="selectChapter($event)" :id="element.id" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker pointer underline">{{ index + 1 }} - {{ element.title }}
                            </span>
                        </li>
                    </ul>
                </div>
            </aside>

            <section class="w-full md:w-3/4 ">
                <div v-for="(chapter, index) in chapterList" :key="chapter.id" :id="chapter.id" v-if="chapterIsVisible && chapter.id == target" class="shadow-md p-4 rounded bg-white">
                    <h3>{{ chapter.title }}</h3>

                    <div v-if="chapter.description !== ''" class="bg-blue-lightest border-t border-b border-blue text-blue-dark px-4 py-3" v-html="chapter.description" role="alert">{{ chapter.description }}</div>

                    <div v-html="chapter.text"></div>

                    <div v-show="!writeToChapterComment" class="text-center"><p @click="writeCommentToChapter" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker pointer underline">Commentez le chapitre</p></div>

                    <div v-if="writeToChapterComment">
                        <Form
                            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
                            title="Nouveau commentaire"
                            :operation="writeComChapter"
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
                            <input type="hidden" name="chapter" id="chapter" v-model="chapter.id" />
                            <input type="hidden" name="title" id="title" v-model="chapter.title" />
                            <input type="hidden" name="order" id="order" v-model="chapter.order" />
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
            </section>
        </div>

        <modal
        v-show="isModalVisible"
        @close="closeModal"
        >
        <h3 slot="header">Voir les commentaires</h3>
        <div slot="body">
            <p v-if="step === 1" @click="writeComment" class="pointer block lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">Donnez votre avis sur cette histoire.</p>
            <div class="tabs comment-tabs">
                <ul class="list-reset flex">
                    <li :class="[ fic === 'story' ? 'is-active' : ''] + ' mr-6'"><a @click="fic='story'" class="text-teal hover:text-teal-darker pointer">Tous</a>
                    </li>
                    <li :class="[ fic === 'chapters' ? 'is-active' : ''] + ' mr-6'"><a @click="fic='chapters'" class="text-teal hover:text-teal-darker pointer">Par chapitre</a></li>
                </ul>
            </div>
            <div class="box comment-content">
                <div v-for="(com, index) in comment" v-if="comment && fic === 'story'" :key="index">
                    <span>{{ com.name }}</span> | Publié le : <span>{{ com.created | date }}</span>
                    <div>{{ com.body }}</div>
                    <div class="border-r border-b border-l border-grey-light border-t lg:border-grey-light bg-white p-4 leading-normal mb-4" v-if="com.in_reply_to !== null">Réponse à {{ com.in_reply_to.name }} le {{ com.in_reply_to.created | date }}
                        <div>{{ com.in_reply_to.body }}</div>
                    </div>
                    <hr/>
                </div>
                <div v-if="!comment.length && fic === 'story'">Cette fanfiction n'a pas encore de commentaires. Soyez le premier :)</div>
                <div v-for="(com_chapter, index) in CommentByChapter" v-if="CommentByChapter && fic === 'chapters'" :key="index">
                    <span>{{ com_chapter.name }}</span> | Publié le : <span>{{ com_chapter.created | date }} sur le chapitre {{com_chapter.chapter.title }}</span>
                    <div>{{ com_chapter.body }}</div>
                    <div class="border-r border-b border-l border-grey-light border-t lg:border-grey-light bg-white p-4 leading-normal mb-4" v-if="com_chapter.in_reply_to !== null">Réponse à {{ com_chapter.in_reply_to.name }} le {{ com_chapter.in_reply_to.created | date }} sur le chapitre {{ com_chapter.chapter.title }}
                        <div>{{ com_chapter.in_reply_to.body }}</div>
                    </div>
                    <hr/>
                </div>
                <div v-if="!CommentByChapter.length && fic === 'chapters'">Cette fanfiction n'a pas encore de commentaires. Soyez le premier :)</div>
            </div>
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
            <p v-if="step === 2" @click="goStepBack" class="pointer inline-block align-baseline font-bold text-sm text-blue hover:text-blue-darker">Retour au chapitre</p>
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
    data () {
        return {
            error: null,
            like: false,
            users: [],
            fanfic: [],
            chapterList: [],
            comment: [],
            CommentByChapter: [],
            date: null,
            errorFetch: 'Il y a un problème avec la requète.',
            isModalVisible: false,
            name: '',
            email: '',
            body: '',
            chapter: '',
            order: '',
            title: '',
            total_comments: '',
            step: 1,
            followStory: false,
            followUser: false,
            followStoryText: '',
            followUserText: '',
            chapterIsVisible: false,
            target: '',
            userFollow: [],
            fanficFollow: [],
            followUserId: '',
            followStoryId: '',
            writeToChapterComment: false,
            fic: 'story'
        }
    },
    computed: {
        valid () {
            return !!this.name && !!this.body
        },
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
            chapterList () {
                return `chapters/${this.$route.params.id}/list`
            },
            comment () {
                return `comments/${this.$route.params.id}/fanfic`
            },
            CommentByChapter () {
                return `comments/fanfic/${this.$route.params.id}/list`
            }
        }),
    ],
    async created () {
        try {
            const res_comment = await this.$fetch(`comments/${this.$route.params.id}/fanfic`);

            if (res_comment) {
                this.total_comments = res_comment.length
            } else {
                throw new Error('error')
            }

            if (this.$state.user !== null && this.$state.user.id !== null) {
                const res_followUser = await this.$fetch('follow-user')
                const res_followStories = await this.$fetch('follow-stories')

                if (res_followUser && res_followStories) {

                    this.userFollow = res_followUser
                    this.fanficFollow = res_followStories

                    for (let x = 0; x < this.userFollow.length; x++) {
                        if ((this.userFollow[x].hasOwnProperty("user_from") && this.userFollow[x].user_from === this.$state.user.id) && this.userFollow[x].hasOwnProperty("user_to") && this.userFollow[x].user_to === this.fanfic.author) {
                            this.followUser = true;
                            this.followUserId = this.userFollow[x].id;
                        }
                    }

                    for (let y = 0; y < this.fanficFollow.length; y++) {
                        if ((this.fanficFollow[y].hasOwnProperty("from_user") && this.fanficFollow[y].from_user === this.$state.user.id) && (this.fanficFollow[y].hasOwnProperty("to_fanfic") && this.fanficFollow[y].to_fanfic === this.fanfic.id)) {
                            this.followStory = true;
                            this.followStoryId = this.fanficFollow[y].id;
                        }
                    }
                }
            }

            let data = this.fanfic.users_like

            for(let i = 0 ; i < data.length; i++){
                if(data[i].hasOwnProperty("username") && data[i].username === this.$state.user.username) {
                    this.like = true;
                }
            }
        } catch (e) {
            this.error = e
        }

        this.step = 1;
    },
    methods: {
        selectChapter (event) {
            let targetId = event.currentTarget.id
            this.target = targetId
            this.chapterIsVisible = true
            this.writeToChapterComment = false
        },
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
            this.like = true
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
            this.like = false
        },
        async followAuthor () {
            const result = await this.$fetch('follow-user', {
                method: 'POST',
                body: JSON.stringify({
                    user_from: this.$state.user.id,
                    user_to: this.fanfic.author
                })
            })

            this.followUser = true;
        },
        async DisFollowAuthor () {
            const result = await this.$fetch('follow-user', {
                method: 'DELETE',
                body: JSON.stringify({
                    id: this.followUserId
                })
            })

            this.followUser = false
        },
        showModal() {
            this.isModalVisible = true
        },
        closeModal() {
            this.isModalVisible = false
        },
        async followFanfic () {
            const result = await this.$fetch('follow-stories', {
                method: 'POST',
                body: JSON.stringify({
                    from_user: this.$state.user.id,
                    to_fanfic: this.fanfic.id
                })
            })
            this.followStory = true
        },
        async DisFollowFanfic () {
            const result = await this.$fetch('follow-stories', {
                method: 'DELETE',
                body: JSON.stringify({
                    id: this.followStoryId
                })
            })

            this.followStory = false
        },
        goStepBack () {
            this.step = 1;
        },
        writeCommentToChapter () {
            this.writeToChapterComment = true;
        },
        async writeComChapter () {
            const result = await this.$fetch('comments-by-chapter/new', {
                method: 'POST',
                body: JSON.stringify({
                    name: this.name,
                    email: this.email,
                    body: this.body,
                    fanfic: this.fanfic.id,
                    chapter: $('input[name="chapter"]').val()
                }),
            })

            this.name = this.email = this.body = '';
            this.total_comments++;

            this.CommentByChapter.unshift(result);
            this.comment.unshift(result);
            this.CommentByChapter[0].chapter = Object.assign({}, this.CommentByChapter[0].chapter, {title: $('input[name="title"]').val(), order: $('input[name="order"]').val()})

            this.writeToChapterComment = false;
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

            this.closeModal();
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

.comment-content {
    background: white;
}

.comment-tabs {
    margin-bottom: 10px;
}

.tabs li.is-active a {
    border-bottom: 1px solid;
    font-weight: bold;
}
</style>
