<template>
    <div>
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
                return `fanfics/author/${this.$state.user.username}`
            },
        }),
    ],
    data(){
        return{
            subtitle: 'Vos fanfictions',
            userFanfics: [],
            isActive: false
        }
    },
    components: {
        Fanfic,
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
        toggle(userFanfic) {
            return this.isActive === userFanfic;
        }
    }
}
</script>

<style scoped>
</style>
