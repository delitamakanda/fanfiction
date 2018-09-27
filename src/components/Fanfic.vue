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
            <section class="infos">
                <h2>{{ fanfic.title }}</h2>
                <div class="info">
                    Crée le {{ fanfic.publish | date }}
                </div>
            </section>
            <section class="content">
                <div>Synopsis : {{ fanfic.synopsis }}</div>
                <div>Credits : {{ fanfic.credits }}</div>
                <div>Description : {{ fanfic.description }}</div>
            </section>
            <section class="content">
                <ul>
                    <li v-for="(chap, index) in chapters" v-if="chap.fanfic === fanfic.id" :key="chap.id">
                        {{ chap.title }} - Publié le {{ chap.published | date }}

                        <router-link :to="{name: 'UpdateChapter', params: { chapter_id: chap.id, id: fanfic.id } }" title="Editer un chapitre" class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker"><svgicon icon="edit-pencil" width="22" height="18" color="#000"></svgicon> </router-link>

                        <button type="button" title="Supprimer le chapitre" @click="deleteChapter(chap.id, index)"><svgicon icon="trash" width="22" height="18" color="#000"></svgicon></button>
                    </li>
                </ul>
            </section>
            <section class="action">
                <div>
                    <router-link class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" :to="{name: 'NewChapter', params: { fanfic: fanfic.id }}">Ajouter un chapitre</router-link>
                </div>
            </section>
            <section class="action">
                <h3>Commentaire(s)</h3>
                <div class="tabs comment-tabs">
                    <ul class="list-reset flex">
                        <li :class="[ fic === 'story' ? 'is-active' : ''] + ' mr-6'"><a @click="fic='story'" class="text-teal hover:text-teal-darker cursor-pointer">Tous</a>
                        </li>
                        <li :class="[ fic === 'chapters' ? 'is-active' : ''] + ' mr-6'"><a @click="fic='chapters'" class="text-teal hover:text-teal-darker cursor-pointer">Par chapitre</a></li>
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
                        <div v-for="(comment, index) in allComments" v-if="allComments && fic === 'story'" :key="comment.id">
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
                        :title="title"
                        :operation="replyToComment"
                        :valid="valid">
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
            </modal>
            <modal
            v-show="isModalChapterVisible"
            @close="closeModalChapter"
            >
                <h3 slot="header">Répondre au commentaire</h3>
                <div slot="body">
                    <Form
                        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
                        :title="title"
                        :operation="replyToCommentByChapter"
                        :valid="valid">
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
                                :disabled="!valid">
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
            chapters () {
                return `chapters/${this.id}/list`
            },
            comments () {
                return `comments/fanfic/${this.id}/list`
            },
            allComments () {
                return `comments/${this.id}/fanfic`;
            }
        }),
        confirm
    ],
    components: {
        modal,
    },
    computed: {
        valid () {
            return !!this.body
        },
        title () {
            return `Répondre à ${this.nameOfuser}`;
        },
    },
    data () {
        return {
            fanfic: [],
            chapters: [],
            comments: [],
            comment: {},
            allComments: [],
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
            idComment: ''
        }
    },
    props: {
        id: {
            type: Number,
            required: true,
        },
    },
    methods: {
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
                       console.log("ok");
                       this.chapter.splice(index, 1);
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

            this.allComments.unshift(result);
            this.allComments[0].in_reply_to = Object.assign({}, this.allComments[0].in_reply_to, {name: this.nameOfuser, created: Date.now(), body: this.bodyText })

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

            this.allComments.unshift(result);
            this.comments.unshift(result);
            this.comments[0].chapter = Object.assign({}, this.comments[0].chapter, {title: this.chapterTitle })
            this.comments[0].in_reply_to = Object.assign({}, this.comments[0].in_reply_to, {name: this.nameOfuser, created: Date.now(), body: this.bodyText })

            this.body = '';

            this.closeModalChapter();
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

</style>
