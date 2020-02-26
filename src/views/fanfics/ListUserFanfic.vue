<template>
  <div>
    <div
      class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative"
      v-if="hasRemoteErrors"
      role="alert"
    >{{ errorFetch }}</div>

    <Loading v-if="remoteDataBusy" />

    <h3>{{ subtitle }}</h3>

    <div class="empty" v-if="fanfics && !fanfics.length">{{ $t('message.emptyMessageFanfiction') }}</div>

    <div class="flex flex-wrap -mx-2" v-if="fanfics && isPrivate">
      <div class="mb-4 w-full px-1 md:w-1/2" v-for="item in fanfics" :key="item.id">
        <router-link
          class="no-underline"
          :to="{
                    name: 'EditFanfic',
                    params: {
                        id: item.id
                    },
                }"
        >
          <div
            class="border border-grey-light bg-white rounded p-4 flex flex-col justify-between leading-normal"
          >
            <div class="mb-8">
              <p
                class="text-sm text-grey-dark italic flex items-center float-right"
              >{{ item.status }}</p>
              <p
                class="text-sm text-grey-dark flex items-center"
              >{{ item.category }} / {{ item.subcategory }}</p>
              <div class="text-black font-bold text-xl mb-2">{{ item.title }}</div>
              <p v-if="item.synopsis" v-html="item.synopsis" class="text-grey-darker text-base"></p>

              <p
                v-if="item.description"
                class="text-grey-darker text-base"
              >{{ item.description | readMore(120, '...') }}</p>
            </div>
            <div class="flex items-center">
              <div class="text-sm">
                <p
                  class="text-black leading-none"
                >{{ $t('message.authorLabel') }} : {{ item.author.username }}</p>
                <p
                  class="text-grey-dark"
                >{{ $t('message.publishedAtLabel' )}} : {{ item.publish | date }}</p>
                <p
                  class="text-grey-dark"
                >{{ item.genres }} / {{ item.classement }} / {{ item.total_likes }} {{ 'like' | pluralize(item.total_likes) }} / {{ item.views }} {{ 'view' | pluralize(item.views) }}</p>
              </div>
            </div>
          </div>
        </router-link>
        <button type="button" 
          :title="$tc('message.removeStoryDisclaimerText', item.title, item.id, {a: item.title, n: item.id})" 
          @click="deleteStory(item)"
          class="bg-blue-500 hover:bg-blue-700 rounded-full text-white font-bold p-2"
        >
          <svgicon icon="trash" width="22" height="18" color="#FFFFFF"></svgicon>
        </button>
      </div>
    </div>
    <div class="flex flex-wrap -mx-2" v-else>
        <fanfic
            v-for="item in fanfics"
            class="mb-4 w-full px-1 md:w-1/2"
            :fanfic="item"
            :displayDescription="true"
            :key="item.id"
        />
    </div>

    <!-- <template v-if="this.$route.params.username !== undefined">
            <div class="mb-4 bg-white max-w-sm">
              <div class="sm:flex sm:items-center px-6 py-4">
                <img v-if="profile.photo !== null" class="block h-24 mx-auto mb-4 sm:mb-0 sm:mr-4 sm:ml-0" :src="profile.photo" alt="">
                <avatar v-else :email="profile.user.email" />
                <div class="text-center sm:text-left sm:flex-grow">
                  <div class="mb-4">
                    <p class="text-xl leading-tight">{{ profile.user.username }}</p>
                    <p v-if="profile.bio" class="text-sm leading-tight text-grey-dark">{{ profile.bio }}</p>
                    <a v-for="(social, i) in profile.social" v-if="profile.social.length > 1" class="hover:text-teal-dark text-teal font-bold mr-4" :key="i" :href="'https://' + social.network + '.com/' + social.nichandle" target="_blank">{{ social.nichandle }}</a>
                  </div>
                  <div>
                    <button type="button" class="text-xs font-semibold rounded-full px-4 py-1 leading-normal bg-white border border-teal text-teal hover:bg-teal hover:text-white">{{ $t('message.messageLabel') }}</button>
                </div>
                </div>
              </div>
            </div>
        </template>

        <h3>{{ subtitle }}</h3>

        <div class="empty" v-if='fanfics.length === 0'>
            {{ $t('message.emptyMessageFanfiction') }}
        </div>

        <div class="flex flex-wrap -mx-2">
            <fanfic
                v-for="(fanfic,i) in fanfics"
                class="mb-4 w-full px-1 md:w-1/2"
                :fanfic="fanfic"
                :key="i"
            />
        </div>

        <h3>{{ $t('message.favoriteAuthorsLabel') }}</h3>

        <div class="empty" v-if='starred_authors.length === 0'>
            {{ $t('message.emptyMessageStarredAuthors') }}
        </div>

        <div
            v-for="(fanfic,i) in starred_authors"
            :key="i"
            class="flex flex-wrap"
        >
            <router-link :key="fanfic.user_to.id" :to="{ name: 'ShowUserFanfic', params: { username: fanfic.user_to.username } }" class="text-teal-500 hover:text-teal-800">
                <avatar :email="fanfic.user_to.email" class="h-16 w-16 md:h-24 md:w-24 rounded-full mx-auto" />
                <div class="text-center">
                  <h2 class="text-lg">{{ fanfic.user_to.username }}</h2>
                </div>
            </router-link>
        </div>

        <h3>{{ $t('message.favoriteStoriesLabel') }}</h3>

        <div class="empty" v-if='starred_fanfics.length === 0'>
            {{ $t('message.emptyMessageStarredFanfiction') }}
        </div>

        <div class="flex flex-wrap -mx-2">
            <fanfic
                v-for="(fanfic,i) in starred_fanfics"
                class="mb-4 w-full px-1 md:w-1/2"
                :fanfic="fanfic.to_fanfic"
                :key="i"
            />
    </div>-->
  </div>
</template>

<script>
import Fanfic from "@/components/fanfic/Fanfic";
import RemoteData from "@/mixins/RemoteData";
import get_cookie from "@/cookie";
import "@/compiled-icons/trash";
import "@/compiled-icons/edit-pencil";
import "@/compiled-icons/view-show";
import { mapActions, mapState, mapGetters } from "vuex";
import confirm from '@/mixins/confirm';

export default {
  created() {
    if(!this.isPrivate) {
      this.fetchFanficsPublishedByAuthor({ status:'publié', author: this.username });
    } else {
      this.fetchFanficsPublishedByAuthor({ author: this.username, status:'' });
    }
  },
  computed: {
    ...mapGetters("user", ["user"]),
    ...mapState("fanfic", ["fanfics"])
  },
  mixins: [
    RemoteData({}),
    confirm
  ],
  props: {
    username: {
      type: String,
      required: true
    },
    slug: {
      type: String,
      required: false
    },
    id: {
      type: Number,
      required: false
    },
    isPrivate: {
        type: Boolean,
        required: false,
        default: true
    }
  },
  data() {
    return {
      subtitle: this.$t("message.vosFanfictionsLabel"),
      errorFetch: this.$t("message.errorFetch")
    };
  },
  methods: {
    ...mapActions("fanfic", [
      "fetchFanficsPublishedByAuthor",
      "clearFanficsPublished",
      "removeFanfic"
    ]),
    deleteStory (story) {
      const message = this.$tc('message.removeStoryDisclaimerText', story.title, story.id, { a: story.title, n: story.id })

        this.confirm(message, () => {
            this.removeFanfic({ id: story.id })
            this.$router.replace(this.$route.params.wantedRoute || { name: 'NewFanfic'})
        })
    },
  },
  components: { Fanfic },
  watch: {
    fanfics(val, oldVal) {
      console.log('val', val)
      console.log('oldVal', oldVal)
    }
  }
};
</script>

<style scoped>
</style>
