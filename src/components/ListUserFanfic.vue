<template>
    <div>
        <h1>{{ subtitle }}</h1>

        <Loading v-if="remoteDataBusy" />

        <div class="empty" v-else-if='userFanfics.length === 0'>
            Vous n'avez pas encore de fanfictions. Libérer votre créativité !
        </div>

        <section v-else class="fanfictions-list">
            <div>
                <div v-for="(userFanfic, index) in userFanfics" :key="userFanfic.id" :index="index">
                    <div class="item-text">
                        <h3>{{ userFanfic.title }}</h3>
                    </div>

                    <div class="item-desc">
                        <p>
                            {{ userFanfic.category }}
                        </p>
                        <p>
                            {{ userFanfic.subcategory }}
                        </p>
                        <p>
                            {{ userFanfic.genres }}
                        </p>
                        <p>
                            {{ userFanfic.classement }}
                        </p>
                        <p>
                            {{ userFanfic.status}}
                        </p>
                        <div v-if="userFanfic.users_like.length > 0">
                            Utilisateurs qui aime votre fanfiction :
                            <ul>
                                <li v-for="user in userFanfic.users_like">

                                    <router-link :to="{ name: 'ShowUserFanfic', params: { username: user.username, id: user.id } }" class=" lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ user.username }} </router-link>
                                </li>
                            </ul>
                        </div>

                        <router-link class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" title="Voir" :to="{name: 'Fanfic', params: { id: userFanfic.id }}"> <svgicon icon="view-show" width="22" height="18" color="#000"></svgicon> </router-link>

                        <router-link class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" title="Editer l'histoire" :to="{name: 'UpdateFanfic', params: { id: userFanfic.id }}"><svgicon icon="edit-pencil" width="22" height="18" color="#000"></svgicon> </router-link>

                        <button @click="deleteStory(userFanfic.id, index)" title="Supprimer l'histoire"><svgicon icon="trash" width="22" height="18" color="#000"></svgicon></button>

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
