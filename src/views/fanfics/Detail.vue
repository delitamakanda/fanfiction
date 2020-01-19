<template>
<div>
    <!-- <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        {{ errorFetch }}
    </div>

    <Loading v-if="remoteDataBusy" />

    <div class="flex">
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
      <div class="w-3/5">
          <h2 class="font-bold text-center text-xl mb-2">{{ obj_fanfic.title }}</h2>
          <p class="text-grey-darker text-base text-center">
            {{ $t('message.authorLabel') }} : <router-link v-if="obj_fanfic.author" :key="obj_fanfic.id" :to="{ name: 'ShowUserFanfic', params: { username: obj_fanfic.author.username, slug: obj_fanfic.slug, id: obj_fanfic.id } }" class=" lg:inline-block lg:mt-0 text-teal-500 hover:text-teal-600">{{ obj_fanfic.author.username }}</router-link>
          </p>
          <p class="text-grey-darker text-center text-base">{{ $t('message.publishedAtLabel') }} : {{obj_fanfic.publish | date }} - {{ $t('message.miseAJourLabel') }} : {{ obj_fanfic.updated | date }}</p>
      </div>
      <div class="w-1/5">
          <button type="button" @click.once="feedback" class="bg-teal-500 hover:bg-teal-500 text-white font-bold py-2 px-4 rounded-full">{{ $t('message.signalerLabel') }}</button>
          <button type="button" @click="printFanfic" class="bg-teal-500 hover:bg-teal-500 text-white font-bold py-2 px-4 rounded-full">{{ $t('message.formatPDFLabel') }}</button>
      </div>
    </div>

    <div class="w-full rounded overflow-hidden shadow">
        <div class="px-6 py-4">
            <div class="text-grey-darker text-base" v-if="obj_fanfic.description">
                <h4>{{ $t('message.descriptionLabel') }}</h4>
                <p v-html="obj_fanfic.description"></p>
            </div>
            <div class="text-grey-darker text-base"  v-if="obj_fanfic.synopsis">
                <h4>{{ $t('message.synopsisLabel') }}</h4>
                <p>{{obj_fanfic.synopsis }}</p>
            </div>
            <div class="text-grey-darker text-base"  v-if="obj_fanfic.credits">
                <h4>{{ $t('message.creditsLabel') }}</h4>
                <p>{{obj_fanfic.credits }}</p>
            </div>
            <div class="text-grey-500 text-base">
                <h4>{{ $t('message.textStatus')}}</h4>
                <p>{{ obj_fanfic.status }}</p>
            </div>
        </div>
        <div class="px-4 py-4">
            <div class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">{{ obj_fanfic.category}}</div>
            <div class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">{{ obj_fanfic.subcategory }}</div>
            <div class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">{{ obj_fanfic.classement }} </div>
            <div class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">{{ obj_fanfic.genres }} </div>
            <div class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-grey-darker">{{ obj_fanfic.views }} {{ 'view' | pluralize(obj_fanfic.views) }}</div>
            <div class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-grey-darker">{{ obj_fanfic.total_likes }} {{'like' | pluralize(obj_fanfic.total_likes) }}</div>
            <div class="cursor-pointer inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-grey-darker" @click="readReviews">{{ commentsCount }} {{ 'review' | pluralize(commentsCount)}}</div>
            <div class="inline-block text-blue-500 hover:text-blue-800 cursor-pointer" @click="writeComment">{{ $t('message.writeCommentLabel', {n: obj_fanfic.title}) }}</div>
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

    <div v-if="obj_fanfic.recommended_fanfics" class="shadow-md my-4 px-4 py-4 rounded bg-white">
        <h3>{{ $t('message.recommendedFanficsLabel') }}:</h3>
        <div v-for="f in obj_fanfic.recommended_fanfics">
            <ul class="list-disc list-inside">
                <router-link class="text-teal-500 hover:text-teal-700 cursor-pointer" :key="f.id" :to="{
                  name: 'Detail',
                  params: {
                    slug: f.slug,
                    id: f.id
                  },
                }">
                <li>{{ f.title }}</li>
                </router-link>
            </ul>
        </div>
    </div>
    <popin ref="comment"></popin>
    <modal ref="commentForm"></modal>-->
</div>
</template>

<script>
import popin from '@/components/popins/PopinComment.vue'
import modal from '@/components/popins/PopinCommentForm.vue'
import '@/compiled-icons/mood-happy-solid'
import '@/compiled-icons/mood-sad-solid'

import RemoteData from '@/mixins/RemoteData'
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
    components: { modal, popin },
    data () {
        return {
            error: null,
            like: false,
            selecteur: null,
            errorFetch: this.$t('message.errorFetch'),
            followStory: false,
            followUser: false,
            counter: null,
            datas: null
        }
    },
    computed: {
        ...mapState('fanfic', ['obj_fanfic']),
        ...mapState('chapter', ['chapters']),
        ...mapState('comment', ['comments']),
        ...mapGetters('user', ['user']),
        ...mapGetters('comment', ['commentsCount']),
        ...mapState('other', ['followedStory', 'followedAuthor', 'followUserId', 'followStoryId']),
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
        RemoteData(),
    ],
    created () {
        this.fetchFanfic({ slug: this.slug })
        //this.fetchChapters({ id: this.id, status: 'publié'})
        //this.fetchAllComments({ id: this.id })
        this.fetchFollowStory()
        this.fetchFollowAuthor()
    },
    mounted () {
        this.$root.$comment = this.$refs.comment.openModal
        this.$root.$commentForm = this.$refs.commentForm.openModal
    },
    methods: {
        ...mapActions('fanfic', ['fetchFanfic', 'clearFanfic']),
        ...mapActions('comment', ['fetchAllComments', 'postComment']),
        ...mapActions('chapter', ['fetchChapters', 'clearChapters']),
        ...mapActions('other', ['sendFormPreventAbuse', 'postUnfavorited', 'postFavorited', 'fetchFollowStory', 'fetchFollowAuthor', 'addFollowStory', 'removeFollowStory', 'addFollowAuthor', 'removeFollowAuthor', 'clearFollowAuthor', 'clearFollowStory']),
        ...mapMutations('comment', ['updateChapterComment', 'addChapterComment']),
        ...mapMutations('fanfic', ['incrementLike', 'decrementLike']),
        ...mapMutations('other', ['setFollowUserId', 'setFollowStoryId']),
        readReviews () {
            this.$root
              .$comment(this.obj_fanfic, this.allCommWithoutAnswer)
        },
        readReviewsChapters () {
            this.$root
              .$comment(this.chapterSelected, this.allChapterCommWithoutAnswer)
        },
        writeComment () {
            this.$root
              .$commentForm(this.obj_fanfic, this.allCommWithoutAnswer)
              .then(res => {
                  if (res.status) {
                      let data = res.r
                     this.postComment(data)
                  }
              })
              .catch(err => console.log(err))
        },
        writeChapterComment () {
            this.$root
              .$commentForm(this.chapterSelected, this.allChapterCommWithoutAnswer)
              .then(res => {
                  if (res.status) {
                      let data = res.r
                      this.datas = data
                      this.postChapterCom(data)
                  }
              })
              .catch(err => console.log(err))
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
        datas(val, old) {
            this.clearChapterComments()
            if (val) {
                this.fetchChapterComments({ id: this.id })
            }
        },
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
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
