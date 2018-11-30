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
                    <!--<button type="button" class="text-xs font-semibold rounded-full px-4 py-1 leading-normal bg-white border border-teal text-teal hover:bg-teal hover:text-white">Message</button>-->
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
                    <div class="border border-grey-light bg-white rounded p-4 flex flex-col justify-between leading-normal">
                        <div class="mb-8">
                            <p class="text-sm text-grey-dark flex items-center">
                                {{ fic.category }} / {{ fic.subcategory }}
                            </p>
                            <div class="text-black font-bold text-xl mb-2">{{ fic.title }}</div>
                            <p v-if="fic.synopsis" class="text-grey-darker text-base">{{ fic.synopsis }}</p>
                        </div>
                        <div class="flex items-center">
                            <div class="text-sm">
                                <p class="text-grey-dark">Publié le : {{ fic.publish | date }}</p>
                                <p class="text-grey-dark">{{ fic.genres }} / {{ fic.classement }} / {{ fic.total_likes }} likes</p>
                            </div>
                        </div>
                    </div>
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
        <template v-else-if="$state.user !== null && $state.user.username !== null">
            <h2>{{ subtitle }}</h2>

            <Loading v-if="remoteDataBusy" />

            <div class="empty" v-else-if='userFanfics.length === 0'>
                Vous n'avez pas encore de fanfictions. Libérer votre créativité !
            </div>

            <section v-else class="fanfictions-list flex -mx-2">
                <div class="md:w-2/3 px-2 w-full">
                    <div v-for="(userFanfic, index) in userFanfics" :key="userFanfic.id" :index="index" class="border-r border-b border-l border-grey-light border-t lg:border-grey-light bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal mb-4">
                        <div class="mb-8">
                            <div class="text-black font-bold text-xl mb-2">{{ userFanfic.title }} <router-link class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" title="Voir" :to="{name: 'Fanfic', params: { id: userFanfic.id }}"> <svgicon icon="view-show" width="22" height="18" color="#000"></svgicon> </router-link></div>
                            <p class="text-grey-darker text-base">
                                {{ userFanfic.category }} / {{ userFanfic.subcategory }}
                            </p>

                            <p class="text-grey-darker text-base">
                                {{ userFanfic.genres }} / {{ userFanfic.classement }} / {{ userFanfic.status}}
                            </p>

                            <p v-if="userFanfic.description" class="text-grey-darker text-base">
                                {{ userFanfic.description | readMore(120, '...') }}
                            </p>

                            <div class="flex items-center">
                                <div class="text-grey-darker text-base" v-if="userFanfic.users_like.length > 0">
                                    Utilisateurs qui aime votre fanfiction :
                                        <span class="mr-4" v-for="user in userFanfic.users_like">

                                            <router-link :to="{ name: 'ShowUserFanfic', params: { username: user.username, id: user.id } }" class=" lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ user.username }} </router-link>
                                        </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="w-full md:w-1/3 px-2">
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
import Fanfic from './Fanfic.vue'
import RemoteData from '../mixins/RemoteData'
import get_cookie from '../cookie'
import '../compiled-icons/trash'
import '../compiled-icons/edit-pencil'
import '../compiled-icons/view-show'

export default {
    name: 'ListUserFanfic',
    mixins: [
        RemoteData({
            userFanfics () {
                return this.$route.params.username ? `fanfics/v1/author/${this.$route.params.username}`: `fanfics/author/${this.$state.user.username}`
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
    components: {
        Fanfic,
    },
    created () {
        if ( this.$route.params.username) {this.getProfileUser()}
        if (this.$state.user && this.$state.user.id != null) { this.getNotifications()}
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
    }
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
