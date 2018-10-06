<template>
    <div>
        <template v-if="this.$route.params.username">
            <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
                {{ errorFetch }}
            </div>

            <Loading v-if="remoteDataBusy" />

            <div class="mb-4 bg-white max-w-sm overflow-hidden">
              <div class="sm:flex sm:items-center px-6 py-4">
                <img v-if="userProfile.photo" class="block h-16 sm:h-24 rounded-full mx-auto mb-4 sm:mb-0 sm:mr-4 sm:ml-0" :src="userProfile.photo" alt="">
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

            <article class="flex flex-wrap -mx-2">
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
        </template>
        <template v-else-if="$state.user !== null && $state.user.username !== null">
            <h1>{{ subtitle }}</h1>

            <Loading v-if="remoteDataBusy" />

            <div class="empty" v-else-if='userFanfics.length === 0'>
                Vous n'avez pas encore de fanfictions. Libérer votre créativité !
            </div>

            <section v-else class="fanfictions-list">
                <div class="max-w-md w-full">
                    <div v-for="(userFanfic, index) in userFanfics" :key="userFanfic.id" :index="index" class="border-r border-b border-l border-grey-light border-t lg:border-grey-light bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal mb-4">
                        <div class="mb-8">
                            <div class="text-black font-bold text-xl mb-2">{{ userFanfic.title }}</div>
                            <p class="text-grey-darker text-base">
                                {{ userFanfic.category }}
                            </p>
                            <p class="text-grey-darker text-base">
                                {{ userFanfic.subcategory }}
                            </p>
                            <p class="text-grey-darker text-base">
                                {{ userFanfic.genres }}
                            </p>
                            <p class="text-grey-darker text-base">
                                {{ userFanfic.classement }}
                            </p>
                            <p class="text-grey-darker text-base">
                                {{ userFanfic.status}}
                            </p>

                            <p v-if="userFanfic.description" class="text-grey-darker text-base">
                                {{ userFanfic.description | readMore(120, '...') }}
                            </p>

                            <div class="flex items-center">
                                <div class="text-sm" v-if="userFanfic.users_like.length > 0">
                                    Utilisateurs qui aime votre fanfiction :
                                        <span class="mr-4" v-for="user in userFanfic.users_like">

                                            <router-link :to="{ name: 'ShowUserFanfic', params: { username: user.username, id: user.id } }" class=" lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ user.username }} </router-link>
                                        </span>
                                </div>

                                <router-link class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" title="Voir" :to="{name: 'Fanfic', params: { id: userFanfic.id }}"> <svgicon icon="view-show" width="22" height="18" color="#000"></svgicon> </router-link>

                                <router-link class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" title="Editer l'histoire" :to="{name: 'UpdateFanfic', params: { id: userFanfic.id }}"><svgicon icon="edit-pencil" width="22" height="18" color="#000"></svgicon> </router-link>

                                <button @click="deleteStory(userFanfic.id, index)" title="Supprimer l'histoire"><svgicon icon="trash" width="22" height="18" color="#000"></svgicon></button>

                            </div>
                        </div>
                    </div>
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
            subtitle: 'Vos fanfictions',
            userFanfics: [],
            userProfile: [],
            isActive: false,
            loadingEmail: false,
            fanfic: [],
            socialAccount: [],
            errorFetch: 'Il y a un problème avec la requète.'
        }
    },
    components: {
        Fanfic,
    },
    mounted () {
        this.getProfileUser()
    },
    methods: {
        async deleteStory (userFanficId, index) {
            let message = confirm('Etes vous certain de supprimer cette histoire ? id# ' + userFanficId);

            if (message == true) {

                $.ajax({
                   url: '/api/fanfics/' + userFanficId,
                   type: 'DELETE',
                   data: { id: userFanficId },
                   headers: {
                       "X-CSRFToken": get_cookie("csrftoken"),
                   },
                   success: function() {
                       console.log("ok");
                       this.userFanfics.splice(index, 1);
                   }.bind(this),
                   error: function(error) {
                       console.log(error);
                   }
                });
            }
        },
        async getProfileUser () {
            this.userProfile = await this.$fetch(`users/${this.$route.params.username}/profile`)
            this.loadingEmail = true
            this.socialAccount = await this.$fetch(`users/${this.userProfile.id}/socialaccount`)
        },
    }
}
</script>

<style scoped>
</style>
