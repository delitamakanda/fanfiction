<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <Loading v-if="remoteDataBusy" />

        <template v-if="this.$route.params.username">
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
                  <!--<div>
                    <button type="button" class="text-xs font-semibold rounded-full px-4 py-1 leading-normal bg-white border border-teal text-teal hover:bg-teal hover:text-white">{{ $t('message.messageLabel') }}</button>
                </div>-->
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
        </div>
    </div>
</template>

<script>
import Fanfic from '@/components/fanfic/Fanfic'
import RemoteData from '../mixins/RemoteData'
import get_cookie from '../cookie'
import '../compiled-icons/trash'
import '../compiled-icons/edit-pencil'
import '../compiled-icons/view-show'
import { mapActions, mapState, mapGetters } from 'vuex'

export default {
    created () {
        let user = (this.$route.params.username === undefined) ? this.user.username : this.$route.params.username;
        let status = (this.$route.params.username === undefined) ? '' : 'publié';
        this.fetchFanficsPublishedByAuthor({ status: status, author: user })
        this.fetchStarredAuthors({ author: user })
        this.fetchStarredFanfics({ author: user })
        if ( this.$route.params.username !== undefined) {
            this.fetchProfileUser({ username: this.$route.params.username })
        }
    },
    computed: {
        ...mapGetters('user', ['user']),
        ...mapState('fanfic', ['fanfics', 'starred_authors', 'starred_fanfics']),
        ...mapState('user', ['profile'])
    },
    mixins: [
        RemoteData({}),
    ],
    props: {
        username: {
            type: String,
            required: false
        },
        slug: {
            type: String,
            required: false
        },
        id: {
            type: Number,
            required: false
        }
    },
    data(){
        return{
            subtitle: this.$t('message.vosFanfictionsLabel'),
            errorFetch: this.$t('message.errorFetch'),
        }
    },
    methods: {
        ...mapActions('fanfic', ['clearFanficsPublished', 'fetchFanficsPublishedByAuthor', 'fetchStarredAuthors', 'fetchStarredFanfics']),
        ...mapActions('user', ['fetchProfileUser'])
    },
    components: { Fanfic },
}
</script>

<style scoped>
</style>
