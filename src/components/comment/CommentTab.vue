<template>
    <div>
        <div class="tabs comment-tabs">
            <ul class="list-reset flex border-b">
                <li :class="[ fic === 'story' ? 'is-active' : ''] + ' -mb-px mr-1'"><a @click="fic='story'" class="bg-white inline-block py-2 px-4 text-blue hover:text-blue-darker font-semibold cursor-pointer">{{ $t('message.AllCommentsText')}}</a>
                </li>
                <li :class="[ fic === 'chapters' ? 'is-active' : ''] + ' -mb-px mr-1'"><a @click="fic='chapters'" class="bg-white inline-block py-2 px-4 text-blue hover:text-blue-darker font-semibold cursor-pointer">{{ $t('message.byChapterText') }}</a></li>
                <li :class="[ fic === 'answers' ? 'is-active' : ''] + ' -mb-px mr-1'"><a @click="fic='answers'" class="bg-white inline-block py-2 px-4 text-blue hover:text-blue-darker font-semibold cursor-pointer">{{ $t('message.answeredComments') }}</a></li>
            </ul>
        </div>
        <div class="comments-section">
            <h4 v-if="total">{{ $tc('message.commentairesText', this.total, { n: this.total } ) }}</h4>
            <div class="comments">
                <div id="comments-container">
                    <div class="comment" v-for="(comment, index) in allComments" v-if="(allComments && fic === 'chapters') && (comment.in_reply_to === null)" :key="index">
                        <div class="comment-user">Ecrit par : {{ comment.name }} le {{ comment.created | date }}</div>
                        <div class="comment-text">{{ comment.body }}</div>
                        <div class="border-r border-b border-l border-grey-light border-t lg:border-grey-light p-4 leading-normal mb-4" v-if="comment.in_reply_to !== null">Réponse à {{ comment.in_reply_to.name }} le {{ comment.in_reply_to.created | date }} sur le chapitre {{ comment.chapter.title }}
                            <div>{{ comment.in_reply_to.body }}</div>
                        </div>
                        <div v-if="isAnswerable">
                            <button role="button" v-if="comment.in_reply_to === null" class="no-underline bg-teal hover:bg-teal-dark text-white font-bold py-2 px-4 rounded-full" @click="showModalChapter(comment.id, comment.name, comment.chapter.id, comment.chapter.title, comment.body)">Répondre</button>
                        </div>
                        <div class="comment-text">Sur le chapitre {{ comment.chapter.title }}</div>
                    </div>
                    <div class="comment" v-for="(comment, index) in answers" v-if="(answers && fic === 'story') && (comment.in_reply_to === null)" :key="index">
                            <div class="comment-user">Ecrit par : {{ comment.name }} le {{ comment.created | date }}</div>
                            <div class="comment-text">{{ comment.body }}</div>
                            <div class="border-r border-b border-l border-grey-light border-t lg:border-grey-light p-4 leading-normal mb-4" v-if="comment.in_reply_to !== null">Réponse à {{ comment.in_reply_to.name }} le {{ comment.in_reply_to.created | date }}
                                <div>{{ comment.in_reply_to.body }}</div>
                            </div>
                            <div v-if="isAnswerable">
                                <button role="button" v-if="comment.in_reply_to === null" class="no-underline bg-teal hover:bg-teal-dark text-white font-bold py-2 px-4 rounded-full" @click="showModal(comment.id, comment.name, comment.body)">Répondre</button>
                            </div>
                            <hr />
                    </div>
                    <div class="comment" v-for="(comment, index) in answers" v-if="(answers && fic === 'answers') && (comment.in_reply_to != null)" :key="index">
                            <div class="comment-user">Ecrit par : {{ comment.name }} le {{ comment.created | date }}</div>
                            <div class="comment-text">{{ comment.body }}</div>
                            <div class="border-r border-b border-l border-grey-light border-t lg:border-grey-light p-4 leading-normal mb-4" v-if="comment.in_reply_to !== null">Réponse à {{ comment.in_reply_to.name }} le {{ comment.in_reply_to.created | date }}
                                <div>{{ comment.in_reply_to.body }}</div>
                            </div>
                            <hr />
                    </div>
                </div>
            </div>
        </div>
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
    </div>
</template>

<script>
import modal from '@/components/popins/Modal.vue'
import { mapGetters } from 'vuex'

export default {
    props: {
        allComments: Array,
        answers: Array,
        total: {type: Number, required: false},
        fanficId: {type: Object, required: false},
        isAnswerable: { type: Boolean, required: false, default: true }
    },
    data: () => ({
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
        titleFanfic: ''
    }),
    computed: {
        ...mapGetters('user', ['user']),
        validComment () {
            return !!this.body
        },
        titleUser () {
            return `Répondre à ${this.nameOfuser}`;
        }
    },
    methods: {
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
                    name: this.user.username,
                    email: this.user.email,
                    body: this.body,
                    fanfic: this.fanficId.id,
                    in_reply_to: this.idComment
                }),
            })

            this.answers.unshift(result);
            this.answers[0].in_reply_to = Object.assign({}, this.answers[0].in_reply_to, {name: this.nameOfuser, created: Date.now(), body: this.bodyText })

            this.body = '';

            this.closeModal();
        },
        async replyToCommentByChapter () {
            const result = await this.$fetch('comments-by-chapter/new', {
                method: 'POST',
                body: JSON.stringify({
                    name: this.user.username,
                    email: this.user.email,
                    body: this.body,
                    fanfic: this.fanficId.id,
                    chapter: this.chapter,
                    in_reply_to: this.idComment
                }),
            })

            this.answers.unshift(result);
            this.allComments.unshift(result);
            this.allComments[0].chapter = Object.assign({}, this.allComments[0].chapter, {title: this.chapterTitle })
            this.allComments[0].in_reply_to = Object.assign({}, this.allComments[0].in_reply_to, {name: this.nameOfuser, created: Date.now(), body: this.bodyText })

            this.body = '';

            this.closeModalChapter();
        },
    },
    components: { modal }
}
</script>

<style scoped>
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

.comments-section h4 {
  font-weight: bold;
  border-bottom: 1px solid #363636;
  padding-top: 5px;
  padding-bottom: 15px;
}

.comments-section .comments {
  color: white;
}
.comments-section .comments h4 {
  border: 0;
}

.comments-section .comment {
  background: #28282B;
  padding: 20px;
  font-size: 15px;
  margin-bottom: 20px;
}
.comments-section .comment blockquote {
  color: #eee;
  padding: 1em;
  border-left: 2px solid #76daff;
  background: rgba(0, 0, 0, 0.05);
}
.comments-section .comment code {
  font-family: Menlo, Monaco, monospace;
  background: rgba(0, 0, 0, 0.2);
  padding: 2px 5px;
  margin: 0 2px;
  border-radius: 2px;
}
.comments-section .comment .box {
  background: #1d1f20;
  padding: 20px;
}
.comments-section .comment .box pre {
  overflow: auto;
  margin: 0;
}
.comments-section .comment .box pre code {
  background: transparent;
}
.comments-section .comment .box + .box {
  padding-top: 0px;
}
.comments-section .comment a {
  color: #76daff;
  text-decoration: none;
}
.comments-section .comment .comment-user {
  border-bottom: 1px solid #555;
  padding: 10px 45px 20px;
  display: flex;
  align-items: center;
}
.comments-section .comment .comment-user .avatar img {
  width: 35px;
  height: 35px;
}
.comments-section .comment .comment-user .username {
  color: #76daff;
}
.comments-section .comment .comment-user .user-details {
  color: #666;
  margin-left: 10px;
}
.comments-section .comment .comment-user .user-details span:last-child {
  color: #999;
  font-size: 80%;
}
.comments-section .comment .comment-text {
  padding: 10px 45px 20px;
}
</style>
