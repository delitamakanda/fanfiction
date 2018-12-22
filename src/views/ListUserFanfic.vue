<template>
    <div>
        <template v-if="this.$route.params.username">
            <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
                {{ errorFetch }}
            </div>

            <Loading v-if="remoteDataBusy" />

            <div class="mb-4 bg-white max-w-sm">
              <div class="sm:flex sm:items-center px-6 py-4">
                <img v-if="userProfile.photo" class="block h-24 mx-auto mb-4 sm:mb-0 sm:mr-4 sm:ml-0" :src="userProfile.photo" alt="">
                <avatar v-else-if="loadingEmail" :email="userProfile.user.email" />
                <div class="text-center sm:text-left sm:flex-grow">
                  <div class="mb-4">
                    <p class="text-xl leading-tight">Fanfictions de {{ this.$route.params.username }}</p>
                    <p v-if="userProfile.bio" class="text-sm leading-tight text-grey-dark">{{ userProfile.bio }}</p>
                    <a v-for="social in socialAccount" v-if="socialAccount.length > 0" class="hover:text-teal-dark text-teal font-bold mr-4" :href="'https://' + social.network + '.com/' + social.nichandle" target="_blank">{{ social.nichandle }}</a>
                  </div>
                  <div>
                    <button type="button" class="text-xs font-semibold rounded-full px-4 py-1 leading-normal bg-white border border-teal text-teal hover:bg-teal hover:text-white">{{ $t('message.messageLabel') }}</button>
                </div>
                </div>
              </div>
            </div>

            <div class="tabs fanfic-tabs">
                <ul class="list-reset flex border-b">
                    <li :class="[ tabs === 'fanfic' ? 'is-active' : ''] + ' -mb-px mr-1'"><a @click="tabs='fanfic'" class="bg-white inline-block py-2 px-4 text-blue hover:text-blue-darker font-semibold cursor-pointer">{{ $t('message.myStoriesLabel') }}</a>
                    </li>
                    <li :class="[ tabs === 'authors' ? 'is-active' : ''] + ' -mb-px mr-1'"><a @click="tabs='authors'" class="bg-white inline-block py-2 px-4 text-blue hover:text-blue-darker font-semibold cursor-pointer">{{ $t('message.favoriteAuthorsLabel') }}</a></li>
                    <li :class="[ tabs === 'fanfictions' ? 'is-active' : ''] + ' -mb-px mr-1'"><a @click="tabs='fanfictions'" class="bg-white inline-block py-2 px-4 text-blue hover:text-blue-darker font-semibold cursor-pointer">{{ $t('message.favoriteStoriesLabel') }}</a>
                    </li>
                </ul>
            </div>
            <article class="flex flex-wrap -mx-2 fanfic-content" v-if="tabs === 'fanfic'">
                <div class="mb-4 w-full px-2 md:w-1/2" v-for="fic of userFanfics" :key="fic.id">
                    <router-link :to="{
                      name: 'Detail',
                      params: {
                        slug: fic.slug,
                        id: fic.id
                      },
                    }"
                    class="no-underline"
                    >
                    <Fanfic :fanfic="fic" :displayAuthorName="false" />
                    </router-link>
                </div>
            </article>
            <article class="-mx-2 fanfic-content" v-if="tabs === 'authors'">
                <ul v-for="author in starredAuthor">
                    <li>
                        <router-link :to="{ name: 'ShowUserFanfic', params: { username: author.user_to.username } }" class=" lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ author.user_to.username }}</router-link>

                    </li>
                </ul>
            </article>
            <article class="-mx-2 fanfic-content" v-if="tabs === 'fanfictions'">
                <ul v-for="fanfic in starredFanfic">
                    <li>
                        <router-link class="hover:text-teal-dark text-teal" :to="{
                          name: 'Detail',
                          params: {
                            slug: fanfic.to_fanfic.slug,
                            id: fanfic.to_fanfic.id
                          },
                        }">
                            {{ fanfic.to_fanfic.title }}
                        </router-link>
                    </li>
                </ul>
            </article>
        </template>
        <template v-else-if="user && user.username != null">
            <h2>{{ subtitle }}</h2>

            <Loading v-if="remoteDataBusy" />

            <div class="empty" v-else-if='userFanfics.length === 0'>
                {{ $t('message.emptyMessageFanfiction') }}
            </div>

            <section v-else class="fanfictions-list-perso">
                <div class="w-full mb-4" v-for="(userFanfic, i) in userFanfics" :key="userFanfic.id" :index="i" >
                    <router-link class="no-underline" :title="$t('message.watchLabel')" :to="{name: 'Fanfic', params: { id: userFanfic.id }}">
                        <Fanfic :fanfic="userFanfic" :displayAuthorName="false" :displayDescription="true" />
                    </router-link>
                </div>
                <div class="w-full">
                    <h2>{{ $t('message.NotificationsLabel') }}</h2>
                    <ul v-for="notification in notifications.results">
                        <li>{{ notification.user.username }} {{ notification.verb }} {{ notification.target }} - {{ notification.created | date }}</li>
                    </ul>
                </div>
            </section>

            <router-view />
        </template>
    </div>
</template>

<script>
import Fanfic from '@/components/Fanfic'
import RemoteData from '../mixins/RemoteData'
import get_cookie from '../cookie'
import '../compiled-icons/trash'
import '../compiled-icons/edit-pencil'
import '../compiled-icons/view-show'
import { mapGetters } from 'vuex'

export default {
    created () {
        if ( this.$route.params.username) {this.getProfileUser()}
        if (this.user && this.user.id != null) { this.getNotifications()}
    },
    computed: {
        ...mapGetters('user', ['user']),
    },
    mixins: [
        RemoteData({
            userFanfics () {
                return this.$route.params.username ? `fanfics/v1/author/${this.$route.params.username}`: `fanfics/author/${this.user.username}`
            },
            starredAuthor () {
                return `following-authors/${this.$route.params.username}`
            },
            starredFanfic () {
                return `following-stories/${this.$route.params.username}`
            }
        }),
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
            userFanfics: [],
            userProfile: [],
            tabs: 'fanfic',
            isActive: false,
            loadingEmail: false,
            fanfic: [],
            socialAccount: [],
            errorFetch: this.$t('message.errorFetch'),
            notifications: [],
            starredFanfic: [],
            starredAuthor: []
        }
    },
    methods: {
        async getProfileUser () {
            this.userProfile = await this.$fetch(`users/${this.$route.params.username}/profile`)
            this.loadingEmail = true
            this.socialAccount = await this.$fetch(`users/${this.userProfile.id}/socialaccount`)
        },
        async getNotifications () {
            this.notifications = await this.$fetch('notifications')
        }
    },
    components: {
        Fanfic
    },
}
</script>

<style scoped>
.tabs li.is-active a {
    border-bottom: 1px solid;
    font-weight: bold;
}

.fanfic-content {
    background: white;
}

.fanfic-tabs {
    margin-bottom: 10px;
}
</style>
