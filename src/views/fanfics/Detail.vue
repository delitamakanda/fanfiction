<template>
<div v-if="obj_fanfic && obj_fanfic.author && obj_fanfic.author.username">
    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        {{ errorFetch }}
    </div>

    <Loading v-if="remoteDataBusy" />

    <nav class="text-black font-bold my-4" aria-label="Breadcrumb">
        <ol class="list-none p-0 inline-flex">
            <li class="flex items-center">
                {{ obj_fanfic.category }}
                <svg class="fill-current w-3 h-3 mx-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"/></svg>
            </li>
            <li class="flex items-center text-gray-500">
                {{ obj_fanfic.subcategory }}
            </li>
        </ol>
    </nav>

    <div class="w-full">
        <div class="flex flex-col justify-between leading-normal">
            <div class="mb-8">
            <p class="text-sm text-gray-600 flex items-center">
                {{ obj_fanfic.status }}
            </p>
            <div class="text-gray-900 font-bold text-xl mb-2">{{ obj_fanfic.title }}</div>
            <p class="text-gray-700 text-base" v-if="obj_fanfic.description">
                {{ obj_fanfic.description }}
            </p>
            <p class="text-grey-700 text-base"  v-if="obj_fanfic.synopsis">
                {{ $t('message.synopsisLabel') }}: {{obj_fanfic.synopsis }}
            </p>
            <p class="text-grey-700 text-base"  v-if="obj_fanfic.credits">
                {{ $t('message.creditsLabel') }}: {{obj_fanfic.credits }}
            </p>
            <p class="text-gray-700 text-base">
                {{ obj_fanfic.genres }} - {{ obj_fanfic.classement }} - {{ obj_fanfic.publish | date }} -  id: {{ obj_fanfic.id }} - {{ obj_fanfic.total_likes }} {{'like' | pluralize(obj_fanfic.total_likes) }} - {{ obj_fanfic.views }} {{ 'view' | pluralize(obj_fanfic.views) }} - {{ $t('message.publishedAtLabel') }} : {{obj_fanfic.publish | date }} <span v-if="obj_fanfic.updated"> - {{ $t('message.miseAJourLabel') }} : {{ obj_fanfic.updated | date }}</span> - {{ commentsCount }} {{ 'review' | pluralize(commentsCount) }} - <router-link :to="{ name: 'Reviews', params: { isPrivate: false, fanficId: obj_fanfic.id } }">{{ $t('message.commentairesLabel') }}</router-link>
            </p>
            </div>
            <div class="flex items-center">
            <router-link :key="obj_fanfic.id" :to="{ name: 'ShowUserFanfic', params: { username: obj_fanfic.author.username, slug: obj_fanfic.slug, id: obj_fanfic.id, isPrivate: false }}">
                <avatar :email="obj_fanfic.author.email" class="h-16 w-16 md:h-10 md:w-10 rounded-full mx-auto" :alt="obj_fanfic.author.username" />
            </router-link>
            <div class="text-sm">
                <router-link :key="obj_fanfic.id" :to="{ name: 'ShowUserFanfic', params: { username: obj_fanfic.author.username, slug: obj_fanfic.slug, id: obj_fanfic.id }}">
                    <p class="text-gray-900 leading-none">
                        {{ obj_fanfic.author.username }}
                    </p>
                </router-link>
                <p class="text-gray-600">{{ obj_fanfic.publish | date }}</p>
            </div>
            </div>
        </div>
    </div>

    <div class="clearfix">
        <div class="float-right">
            <div class="inline-block relative w-64">
                <select v-model.lazy="selecteur" class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline">
                    <option v-for="(chapter, i) in chapters" :key="chapter.id" :value="chapter.id">{{ i + 1 }} - {{ chapter.title }}</option>
                </select>
                <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                </div>
            </div>
        </div>
    </div>

    <div v-if="chapterSelected" class="w-full">
        <h3>{{ chapterSelected.title }}</h3>
        <p>{{ $t('message.publishedAtLabel') }} : {{ chapterSelected.published | date }}</p>
        <div v-html="chapterSelected.text"></div>
    </div>

    <Form
        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
        title=""
        :operation="writeComment"
        :valid="valid">
        <div class="mb-4">
            <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="name">
                {{ $t('message.UsernameOrPseudoLabel') }}
            </label>
            <Input
            name="name"
            v-model="form.name"
            :placeholder="$t('message.UsernameOrPseudoLabel')"
            maxlength="255"
            required />
        </div>
        <div class="mb-4">
            <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="email">
                {{ $t('message.formContactEmailLabel') }}
            </label>
            <Input
            name="email"
            v-model="form.email"
            :placeholder="$t('message.emailPlaceholderLabel')"
            maxlength="255" />
        </div>
        <div class="mb-4">
            <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="body">
                {{ $t('message.formContactMessageLabel') }}
            </label>
            <Input
            type="textarea"
            name="body"
            v-model="form.body"
            :placeholder="$t('message.formContactMessageLabel')"
            rows="6"
            required />
        </div>
        <template slot="actions">
            <div class="flex items-center justify-between">
                <button
                class="bg-blue-500 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
                type="submit"
                :disabled="!valid">
                {{ $t('message.donnezVotreAvisLabel') }}
            </button>
        </div>
        </template>
    </Form>

    <div class="w-full my-8 text-center">
        <button type="button" @click.once="feedback" class="bg-teal-500 hover:bg-teal-500 text-white font-bold py-2 px-4 rounded-full">{{ $t('message.signalerLabel') }}</button>
        <button type="button" @click="printFanfic" class="bg-teal-500 hover:bg-teal-500 text-white font-bold py-2 px-4 rounded-full">{{ $t('message.formatPDFLabel') }}</button>
    </div>

    <div v-if="obj_fanfic.recommended_fanfics && obj_fanfic.recommended_fanfics.length" class="flex flex-col w-full flex-wrap">
        <div class="flex items-center justify-between bg-gray-200 p-4">
            <span class="text-lg text-tial-800 font-semibold">{{ $t('message.recommendedFanficsLabel') }}</span>
            <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><polyline points="6 9 12 15 18 9"></polyline></svg>	
        </div>
        <div class="flex flex-wrap flex-col md:flex-row">
            <div 
            v-for="f in obj_fanfic.recommended_fanfics" 
            class="flex flex-wrap bg-white border-b border-blue-tial-100 md:w-1/2 lg:w-1/3" 
            :key="f.id">
                <div class="flex w-full m-4">
                    <div class="flex items-center">
                        <div class="flex flex-col p-4">
                            <h3 class="font-bold text-md text-tial-400">
                                <router-link :key="f.id" :to="{
                                    name: 'Detail',
                                    params: {
                                        slug: f.slug,
                                        id: f.id
                                    },
                                }">
                                {{ f.title }}
                                </router-link>
                            </h3>
                            <span class="font-light text-sm">
                                {{ f.total_likes }} {{'like' | pluralize(f.total_likes) }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <!-- <div class="flex">
      <div class="w-1/5">
          <template v-if="user && user.id != null">
              <button v-if="!followUser" v-model="getAuthorFollowed" type="button" @click="followAuthor" class="bg-teal-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded-full">{{ $t('message.followAuthorText') }}</button>

              <button v-if="followUser" v-model="getAuthorFollowed" type="button" @click="DisFollowAuthor" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-full">{{ $t('message.NotFollowAuthorText') }}</button>

              <button v-if="!followStory" v-model="getStoriesFollowed" type="button" @click="followFanfic" class="bg-teal-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded-full">{{ $t('message.followFanficText') }}</button>

              <button v-if="followStory" v-model="getStoriesFollowed" type="button" @click="DisFollowFanfic" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-full">{{ $t('message.NotFollowFanficText') }}</button>

              <button type="button" class="inline-flex items-center bg-teal-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded-full" v-model="getUserLiked" @click="favorite" v-if="!like">
                  <svgicon icon="mood-happy-solid" width="22" height="18" color="#fff"></svgicon> {{ counter }}
              </button>

              <button type="button" class="inline-flex items-center bg-red-500 hover:bg-red-darker text-white font-bold py-2 px-4 rounded-full" v-model="getUserLiked" @click="unfavorite" v-if="like">
                  <svgicon icon="mood-sad-solid" width="22" height="18" color="#fff"></svgicon> {{ counter }}
              </button>
          </template>
      </div>
      
    </div>

    <div class="shadow-md my-4 px-4 py-4 rounded bg-white">
        <div class="inline-block relative w-64">
          <select v-model.lazy="selecteur" class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline">
            <option v-for="(chapter, i) in chapters" :key="chapter.id" :value="chapter.id">{{ i + 1 }} - {{ chapter.title }}</option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
          </div>
        </div>
        <div class="py-4" v-if="chapterSelected">
            <h3>{{ chapterSelected.title }}</h3>
            <p>{{ $t('message.publishedAtLabel') }} : {{ chapterSelected.published | date }}</p>
            <div v-html="chapterSelected.text"></div>

            <div class="cursor-pointer inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-grey-darker" @click="readReviewsChapters">{{ commentsChapterCount(selecteur) }} {{ 'review' | pluralize(commentsChapterCount(selecteur)) }}</div>
            <div class="inline-block text-blue-500 hover:text-blue-800 cursor-pointer" @click="writeChapterComment">{{ $t('message.writeCommentChapterLabel', {n: chapterSelected.title}) }}</div>
        </div>
    </div>
    -->
</div>
</template>

<script>
import '@/compiled-icons/mood-happy-solid'
import '@/compiled-icons/mood-sad-solid'

import RemoteData from '@/mixins/RemoteData'
import PersistantData from '@/mixins/PersistantData'
import * as _ from 'lodash'

import { mapGetters, mapActions, mapState, mapMutations } from 'vuex'

export default {
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
    data () {
        return {
            error: null,
            like: false,
            selecteur: null,
            errorFetch: this.$t('message.errorFetch'),
            followStory: false,
            followUser: false,
            counter: null,
            form: {
                name: '',
                email: '',
                body: '',
            }
        }
    },
    computed: {
        ...mapState('fanfic', ['obj_fanfic']),
        ...mapState('chapter', ['chapters']),
        ...mapGetters('user', ['user']),
        ...mapGetters('comment', ['commentsCount']),
        ...mapState('comment', ['comments']),
        ...mapState('other', ['followedStory', 'followedAuthor', 'followUserId', 'followStoryId']),
        valid () {
            return !!this.form.name && !!this.form.body
        },
        chapterSelected () {
            if (!this.selecteur) return
            let arr = []
            this.chapters.map(c => {
                arr.push(c)
            })
            return arr.find(a => a.id === this.selecteur)
        },
        getUserLiked () {
            let data = this.obj_fanfic.users_like

            if (!_.isEmpty(data)) {
                data.forEach(d => {
                    if (d.hasOwnProperty('username') && d.username === this.user.username) {
                        this.like = true
                    }
                })
            }
        },
        getAuthorFollowed () {
            let data = this.followedAuthor
            if (!_.isEmpty(data)) {
                data.forEach(d => {
                    if ((d.id !== undefined ) && (d.hasOwnProperty("user_from") && d.user_from === this.user.id) && (d.hasOwnProperty("user_to") && d.user_to === this.obj_fanfic.author.id)) {
                        this.followUser = true;
                        let o = d.id
                        this.setFollowUserId(o)
                    }
                })
            }
        },
        getStoriesFollowed () {
            let data = this.followedStory
            if (!_.isEmpty(data)) {
                data.forEach(d => {
                    if ((d.id !== undefined ) && (d.hasOwnProperty("from_user") && d.from_user === this.user.id) && (d.hasOwnProperty("to_fanfic") && d.to_fanfic === this.obj_fanfic.id)) {
                        this.followStory = true;
                        let y = d.id
                        this.setFollowStoryId(y)
                    }
                })
            }
        }
    },
    mixins: [
        PersistantData('NewComment', [
            'name',
            'email',
            'body',
        ]),
        RemoteData(),
    ],
    created () {
        this.fetchFanfic({ slug: this.slug })
        this.fetchChapters({ id: this.id, status: 'publié'})
        this.fetchAllComments({ id: this.id, isActive: true })
        
        //this.fetchFollowStory()
        //this.fetchFollowAuthor()
    },
    methods: {
        ...mapActions('fanfic', ['fetchFanfic', 'clearFanfic']),
        ...mapActions('comment', ['postComment', 'fetchAllComments']),
        ...mapActions('chapter', ['fetchChapters', 'clearChapters']),
        ...mapActions('other', ['sendFormPreventAbuse', 'postUnfavorited', 'postFavorited', 'fetchFollowStory', 'fetchFollowAuthor', 'addFollowStory', 'removeFollowStory', 'addFollowAuthor', 'removeFollowAuthor', 'clearFollowAuthor', 'clearFollowStory']),
        ...mapMutations('fanfic', ['incrementLike', 'decrementLike']),
        ...mapMutations('other', ['setFollowUserId', 'setFollowStoryId']),
        writeComment () {
            const data = {
                name: this.form.name,
                email: this.form.email,
                body: this.form.body,
                fanfic: this.chapterSelected.fanfic,
                chapter: this.chapterSelected.id
            }
            this.postComment(data)
            this.form.name = ''
            this.form.email = ''
            this.form.body = ''
        },
        printFanfic () {
            window.open(`/help/fanfic/${this.obj_fanfic.id}/pdf`, '_blank')
        },
        feedback () {
            let message = confirm(this.$t('message.feedBackTextLabel'));
            if (message === true) {
                this.sendFormPreventAbuse({ id: this.obj_fanfic.id })
            }
        },
        favorite () {
            this.postFavorited({ id: this.obj_fanfic.id, user: this.user.id })
            this.incrementLike(this.obj_fanfic)
            this.like = true
        },
        unfavorite () {
            this.postUnfavorited({ id: this.obj_fanfic.id, user: this.user.id })
            this.decrementLike(this.obj_fanfic)
            this.like = false
        },
        followAuthor () {
            this.addFollowAuthor({ user_from: this.user.id, user_to: this.obj_fanfic.author.id })
            this.followUser = true;
        },
        DisFollowAuthor () {
            this.removeFollowAuthor({ id: this.followUserId })
            this.followUser = false
        },
        followFanfic () {
            this.addFollowStory({ from_user: this.user.id, to_fanfic: this.obj_fanfic.id })
            this.followStory = true
        },
        DisFollowFanfic () {
            this.removeFollowStory({ id: this.followStoryId })
            this.followStory = false
        }
    },
    watch: {
        followStory (val, old) {
            this.clearFollowStory()
            if (val || !val) {
                this.fetchFollowStory()
            }
        },
        followUser (val, old) {
            this.clearFollowAuthor()
            if (val || !val) {
                this.fetchFollowAuthor()
            }
        },
        chapters(val, oldVal) {
            if (this.chapters && this.chapters.length) {
                this.selecteur = this.chapters[0].id
            }
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
