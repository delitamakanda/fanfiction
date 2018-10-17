<template>
    <div class="fanfic">
        <Loading v-if="remoteDataBusy" />
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>
        <div class="empty" v-else-if="!fanfic">
            Fanfiction non trouvée.
        </div>
        <template v-else>
            <section class="update-infos" v-if="isEditingFanfic">
                <form
                @submit.prevent="edit"
                enctype="multipart/form-data"
                class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <h2>Editer {{ fanfic.title }}</h2>
                <div class="flex flex-wrap -mx-3 mb-6">
                    <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
                      <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="category">
                        Catégorie
                      </label>
                      <div class="relative">
                          <select disabled class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="category" name="category" v-model="fanfic.category">
                              <option value="">Sélectionner</option>
                              <option v-for="(option, index) of dataCategories" v-bind:value="option.id">{{ option.name }}</option>
                          </select>
                          <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                          </div>
                      </div>
                    </div>
                    <div class="w-full md:w-1/2 px-3">
                      <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="subcategory">
                          Sous - Catégories
                      </label>
                      <div class="relative">
                          <select disabled class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="subcategory" name="subcategory" v-model="fanfic.subcategory">
                              <option value="">Sélectionner</option>
                              <option v-for="(option, index) of dataSubCategories" v-bind:value="option.id">{{ option.name }}</option>
                          </select>
                          <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                          </div>
                      </div>
                    </div>
                  </div>
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="title">
                          Titre de l'histoire
                        </label>
                        <Input
                            name="title"
                            v-model="fanfic.title"
                            placeholder="Titre de l'histoire"
                            maxlength="255"
                            required />
                    </div>
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="synopsis">
                          Synopsis
                        </label>
                        <Input
                            type="textarea"
                            name="synopsis"
                            v-model="fanfic.synopsis"
                            placeholder="Synopsis"
                            maxlength="1000"
                            rows="4" />
                    </div>
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="credits">
                          Crédits
                        </label>
                        <Input
                            type="textarea"
                            name="credits"
                            v-model="fanfic.credits"
                            placeholder="Crédits"
                            maxlength="350" />
                    </div>
                    <div class="mb-6">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="description">
                          Description de l'histoire
                        </label>
                        <Input
                            type="textarea"
                            name="description"
                            v-model="fanfic.description"
                            placeholder="Description"
                            maxlength="1000"
                            rows="4" />
                    </div>
                    <div class="flex flex-wrap -mx-3 mb-2">
                        <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                            <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="classement">
                              Classement
                            </label>
                            <div class="relative">
                                <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="classement" name="classement" v-model="fanfic.classement">
                                    <option value="">Sélectionner</option>
                                    <option value="g">G</option>
                                    <option value="13">13+</option>
                                    <option value="r">R</option>
                                    <option value="18">18+</option>
                                </select>
                                <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                                </div>
                            </div>
                      </div>
                      <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2">
                          Genres
                        </label>
                        <div class="relative">
                            <label :for="select[0]" v-for="select in dataGenresFormatted">
                                <input :value="select[0]" v-model="fanfic.genres" :id="select[0]" type="checkbox">
                                {{ select[1] }}<br>
                            </label>
                        </div>
                      </div>
                      <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                          <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="status">
                            Status
                          </label>
                          <div class="relative">
                            <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="status" v-model="fanfic.status">
                                <option value="">Sélectionner</option>
                                <option value="brouillon">Brouillon</option>
                                <option value="publié">Publié</option>
                            </select>
                            <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                            </div>
                          </div>
                      </div>
                  </div>
                    <button
                        type="button"
                        @click="editFanfic"
                        class="secondary inline-block align-baseline font-bold text-sm text-blue hover:text-blue-darker">
                        Retour à la l'histoire
                    </button>
                    <button
                        type="submit"
                        class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded">
                        Editer l' histoire
                    </button>
                </form>
            </section>
            <section class="infos" v-else>
                <h2>{{ fanfic.title }}</h2>
                <div class="info">
                    Crée le {{ fanfic.publish | date }}
                </div>

                <div v-if="fanfic.synopsis">Synopsis : {{ fanfic.synopsis }}</div>
                <div>Credits : {{ fanfic.credits }}</div>
                <div v-if="fanfic.description">Description : {{ fanfic.description }}</div>

                <button type="button" @click="editFanfic" title="Editer l'histoire"><svgicon icon="edit-pencil" width="22" height="18" color="#000"></svgicon></button>

                <button @click="deleteStory(fanfic.id)" title="Supprimer l'histoire"><svgicon icon="trash" width="22" height="18" color="#000"></svgicon></button>
            </section>
            <section class="update-chapters" v-if="isEditingChapter">
                <form
                @submit.prevent="editingChapter"
                enctype="multipart/form-data"
                class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                    <h2>Editer le chapitre</h2>
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="title">
                          Titre du chapitre
                        </label>
                        <Input
                            name="title"
                            v-model="chapters.title"
                            placeholder="Titre du chapitre"
                            maxlength="255"
                            required />
                    </div>
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="description">
                          Description du chapitre
                        </label>
                        <Input
                            type="textarea"
                            name="description"
                            v-model="chapters.description"
                            placeholder="Description du chapitre"
                            maxlength="1000"
                            rows="4" />
                    </div>
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="text">
                          Chapitre
                        </label>
                        <trumbowyg v-model="chapters.text"></trumbowyg>
                    </div>
                    <div class="mb-4">
                        <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="status_chapter">
                          Status
                        </label>
                        <div class="relative">
                          <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="status_chapter" v-model="chapters.status">
                              <option value="">Sélectionner</option>
                              <option value="brouillon">Brouillon</option>
                              <option value="publié">Publié</option>
                          </select>
                          <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                          </div>
                        </div>
                    </div>
                    <Input
                        type="hidden"
                        name="fanfic"
                        v-model="chapters.fanfic" />
                    <button
                        type="button"
                        @click="closeChapterEditing"
                        class="secondary inline-block align-baseline font-bold text-sm text-blue hover:text-blue-darker">
                        Retour à la l'histoire
                    </button>
                    <button
                        type="submit"
                        class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded">
                        Editer le chapitre
                    </button>
                </form>
            </section>
            <section class="chapters">
                <ul>
                    <li v-for="(chap, index) in chapters" v-if="chap.fanfic === fanfic.id" :key="chap.id">
                        {{ chap.title }} - Publié le {{ chap.published | date }}

                        <button type="button" title="Editer un chapitre" class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" @click="editChapter(chap.id)"><svgicon icon="edit-pencil" width="22" height="18" color="#000"></svgicon> </button>

                        <button type="button" title="Supprimer le chapitre" @click="deleteChapter(chap.id, index)"><svgicon icon="trash" width="22" height="18" color="#000"></svgicon></button>
                    </li>
                </ul>
            </section>
            <section class="action">
                <div>
                    <router-link class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" :to="{name: 'NewChapter', params: { fanfic: fanfic.id }}">Ajouter un chapitre</router-link>
                </div>
            </section>
            <section class="action" v-if="anwserByComments.length > 0 && comments.length > 0">
                <h3>Commentaire(s)</h3>
                <div class="tabs comment-tabs">
                    <ul class="list-reset flex border-b">
                        <li :class="[ fic === 'story' ? 'is-active' : ''] + ' -mb-px mr-1'"><a @click="fic='story'" class="bg-white inline-block py-2 px-4 text-blue hover:text-blue-darker font-semibold cursor-pointer">Tous</a>
                        </li>
                        <li :class="[ fic === 'chapters' ? 'is-active' : ''] + ' -mb-px mr-1'"><a @click="fic='chapters'" class="bg-white inline-block py-2 px-4 text-blue hover:text-blue-darker font-semibold cursor-pointer">Par chapitre</a></li>
                    </ul>
                </div>
                <div class="box comment-content">
                    <div>
                        <div v-for="(comment, index) in comments" v-if="comments && fic === 'chapters'" :key="comment.id">
                            Ecrit par : {{ comment.name }} le {{ comment.created | date }} sur le chapitre {{ comment.chapter.title }}
                            <div>{{ comment.body }}</div>
                            <div class="border-r border-b border-l border-grey-light border-t lg:border-grey-light bg-white p-4 leading-normal mb-4" v-if="comment.in_reply_to !== null">Réponse à {{ comment.in_reply_to.name }} le {{ comment.in_reply_to.created | date }} sur le chapitre {{ comment.chapter.title }}
                                <div>{{ comment.in_reply_to.body }}</div>
                            </div>
                            <span v-if="comment.in_reply_to === null" class="cursor-pointer lg:inline-block text-teal hover:text-teal-darker italic underline" @click="showModalChapter(comment.id, comment.name, comment.chapter.id, comment.chapter.title, comment.body)">Répondre</span>
                            <hr />
                        </div>
                        <div v-for="(comment, index) in anwserByComments" v-if="anwserByComments && fic === 'story'" :key="comment.id">
                                Ecrit par : {{ comment.name }} le {{ comment.created | date }}
                                <div>{{ comment.body }}</div>
                                <div class="border-r border-b border-l border-grey-light border-t lg:border-grey-light bg-white p-4 leading-normal mb-4" v-if="comment.in_reply_to !== null">Réponse à {{ comment.in_reply_to.name }} le {{ comment.in_reply_to.created | date }}
                                    <div>{{ comment.in_reply_to.body }}</div>
                                </div>
                                <span v-if="comment.in_reply_to === null" class="cursor-pointer lg:inline-block text-teal hover:text-teal-darker italic underline" @click="showModal(comment.id, comment.name, comment.body)">Répondre</span>
                                <hr />
                        </div>
                    </div>
                </div>
            </section>
            <modal
            v-show="isModalVisible"
            @close="closeModal"
            >
                <h3 slot="header">Répondre au commentaire</h3>
                <div slot="body">
                    <Form
                        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
                        :title="titleUser"
                        :operation="replyToComment"
                        :valid="validComment">
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
                            :disabled="!validComment">
                            Ajouter un commentaire
                        </button>
                    </template>
                </Form>
                </div>
            </modal>
            <modal
            v-show="isModalChapterVisible"
            @close="closeModalChapter"
            >
                <h3 slot="header">Répondre au commentaire</h3>
                <div slot="body">
                    <Form
                        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
                        :title="titleUser"
                        :operation="replyToCommentByChapter"
                        :valid="validComment">
                        <div class="mb-4">
                            <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="body">
                                Commentaire
                            </label>
                            <Input
                            type="textarea"
                            name="bodyText"
                            v-model="body"
                            placeholder=""
                            rows="6"
                            required />
                        </div>
                        <template slot="actions">
                            <button
                                type="submit"
                                class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                                :disabled="!validComment">
                                Ajouter un commentaire
                            </button>
                        </template>
                    </Form>
                </div>
            </modal>
        </template>
    </div>
</template>

<script>
import modal from './Modal.vue'

import RemoteData from '../mixins/RemoteData'
import confirm from '../mixins/confirm'

import get_cookie from '../cookie'
import '../compiled-icons/trash'
import '../compiled-icons/edit-pencil'

export default {
    name: 'Fanfic',
    mixins: [
        RemoteData({
            fanfic () {
                return `fanfics/${this.id}`
            },
            comments () {
                return `comments/fanfic/${this.id}/list`
            },
            anwserByComments () {
                return `comments/${this.id}/fanfic`;
            }
        }),
        confirm
    ],
    components: {
        modal,
    },
    computed: {
        validComment () {
            return !!this.body
        },
        titleUser () {
            return `Répondre à ${this.nameOfuser}`;
        },
    },
    data () {
        return {
            fanfic: [],
            chapters: [],
            comments: [],
            comment: {},
            anwserByComments: [],
            errorFetch: 'Il y a un problème avec la requète.',
            fic: 'story',
            isModalVisible: false,
            isModalChapterVisible: false,
            name: '',
            email: '',
            body: '',
            chapter: '',
            chapterTitle: '',
            in_reply_to: '',
            nameOfuser: '',
            bodyText: '',
            idComment: '',
            isEditingFanfic: false,
            isEditingChapter: false,
            error: null,
            dataCategories: [],
            dataSubCategories: [],
            dataGenres: {},
            titleFanfic: '',
            description: '',
            synopsis: '',
            credits: '',
            author: '',
            genres: [],
            classement: '',
            status: '',
            category: '',
            subcategory: '',
            loadingGenres: false,
            dataGenresFormatted: {},
            text: '',
            chapter_id: ''
        }
    },
    props: {
        id: {
            type: Number,
            required: true,
        }
    },
    async created () {
        this.dataGenresFormatted = await this.$fetch('fanfics/genres')
        this.loadingGenres = true
        this.dataGenresFormatted = this.dataGenresFormatted[0]['genres']

        this.dataCategories = await this.$fetch('category')
        this.dataSubCategories = await this.$fetch('subcategory')
    },
    mounted () {
        this.getChaptersList()
    },
    methods: {
        async getChaptersList () {
            this.chapters = await this.$fetch(`chapters/${this.id}/list`)
        },
        async deleteChapter (chapterId, index) {
            const message = `Supprimer le chapitre id #${chapterId} ?`

            this.confirm(message, () => {
                $.ajax({
                   url: '/api/chapters/' + chapterId,
                   type: 'DELETE',
                   headers: {
                       "X-CSRFToken": get_cookie("csrftoken"),
                   },
                   data: { id: chapterId },
                   success: function() {
                       this.chapters.splice(index, 1);
                   }.bind(this),
                   error: function(error) {
                       console.log(error);
                   }
                });
            });
        },
        showModal(commentId, commentName, commentBody) {
            this.isModalVisible = true
            this.nameOfuser = commentName
            this.idComment = commentId
            this.bodyText = commentBody
        },
        showModalChapter(commentId, commentName, commentChapterId, commentChapterTitle, commentBody) {
            this.isModalChapterVisible = true
            this.nameOfuser = commentName
            this.chapter = commentChapterId
            this.idComment = commentId
            this.chapterTitle = commentChapterTitle
            this.bodyText = commentBody
        },
        closeModal() {
            this.isModalVisible = false
        },
        closeModalChapter() {
            this.isModalChapterVisible = false
        },
        async replyToComment () {
            const result = await this.$fetch('comments/new', {
                method: 'POST',
                body: JSON.stringify({
                    name: this.$state.user.username,
                    email: this.$state.user.email,
                    body: this.body,
                    fanfic: this.fanfic.id,
                    in_reply_to: this.idComment
                }),
            })

            this.anwserByComments.unshift(result);
            this.anwserByComments[0].in_reply_to = Object.assign({}, this.anwserByComments[0].in_reply_to, {name: this.nameOfuser, created: Date.now(), body: this.bodyText })

            this.body = '';

            this.closeModal();
        },
        async replyToCommentByChapter () {
            const result = await this.$fetch('comments-by-chapter/new', {
                method: 'POST',
                body: JSON.stringify({
                    name: this.$state.user.username,
                    email: this.$state.user.email,
                    body: this.body,
                    fanfic: this.fanfic.id,
                    chapter: this.chapter,
                    in_reply_to: this.idComment
                }),
            })

            this.anwserByComments.unshift(result);
            this.comments.unshift(result);
            this.comments[0].chapter = Object.assign({}, this.comments[0].chapter, {title: this.chapterTitle })
            this.comments[0].in_reply_to = Object.assign({}, this.comments[0].in_reply_to, {name: this.nameOfuser, created: Date.now(), body: this.bodyText })

            this.body = '';

            this.closeModalChapter();
        },
        async deleteStory (userFanficId) {
            const message = `Etes vous certain de supprimer cette histoire ? id# ${userFanficId} ?`

            this.confirm(message, () => {
                $.ajax({
                   url: '/api/fanfics/' + userFanficId,
                   type: 'DELETE',
                   data: { id: userFanficId },
                   headers: {
                       "X-CSRFToken": get_cookie("csrftoken"),
                   },
                   success: function() {
                       this.$router.replace(this.$route.params.wantedRoute || { name: 'ListUserFanfic'})
                   }.bind(this),
                   error: function(error) {
                       console.log(error);
                   }
                });
            })
        },
        editFanfic () {
            this.isEditingFanfic = !this.isEditingFanfic
        },
        async editChapter (id) {
            this.chapters = await this.$fetch(`chapters/${id}`)
            this.isEditingChapter = true
            this.chapter_id = id
        },
        async closeChapterEditing () {
            this.isEditingChapter = false
            this.getChaptersList()
        },
        async edit () {
            const result = await this.$fetch(`fanfics/${this.$route.params.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    title: this.fanfic.title,
                    description: this.fanfic.description,
                    synopsis: this.fanfic.synopsis,
                    credits: this.fanfic.credits,
                    author: this.fanfic.author,
                    genres: this.fanfic.genres,
                    classement: this.fanfic.classement,
                    status: this.fanfic.status,
                    category: this.fanfic.category,
                    subcategory: this.fanfic.subcategory,
                }),
            })
            this.isEditingFanfic = false
        },
        async editingChapter () {
            const result = await this.$fetch(`chapters/${this.chapter_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    title: this.chapters.title,
                    description: this.chapters.description,
                    text: this.chapters.text,
                    fanfic: this.chapters.fanfic,
                    author: this.$state.user.id,
                    status: this.chapters.status
                }),
            })
            this.closeChapterEditing()
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.action + .action {
    margin-top: 10px;
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

.w-full {
    margin: 0 auto;
}
</style>
