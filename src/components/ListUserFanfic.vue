<template>
    <div>
        <h1>{{ subtitle }}</h1>

        <Loading v-if="remoteDataBusy" />

        <div class="empty" v-else-if='userFanfics.length === 0'>
            Vous n'avez pas encore de fanfictions. Libérer votre créativité !
        </div>

        <section v-else class="fanfictions-list">
            <ol>
                <li v-for="(userFanfic, index) in userFanfics" :key="userFanfic.id" :index="index">
                    <router-link class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" :to="{name: 'Fanfic', params: { id: userFanfic.id }}"> <h3>{{ userFanfic.title }} - {{ userFanfic.category }} - {{ userFanfic.subcategory }} </h3> </router-link>
                    <button class="text-red hover:text-red-darker" @click="deleteStory(userFanfic.id, index)">x</button>
                </li>
            </ol>
        </section>

        <router-view />
    </div>
</template>

<script>
import Fanfic from './Fanfic.vue'
import RemoteData from '../mixins/RemoteData'

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
        }
    },
    components: {
        Fanfic,
    },
    methods: {
        get_cookie(name) {
            var value;
            if (document.cookie && document.cookie !== '') {
                document.cookie.split(';').forEach(function (c) {
                    var m = c.trim().match(/(\w+)=(.*)/);

                    if(m !== undefined && m[1] == name) {
                        value = decodeURIComponent(m[2]);
                    }
                });
            }
            return value;
        },
        async deleteStory (userFanficId, index) {
            let message = confirm('Etes vous certain de supprimer cette histoire ? id# ' + userFanficId);

            if (message == true) {

                $.ajax({
                   url: '/api/fanfics/' + userFanficId,
                   type: 'DELETE',
                   data: { id: userFanficId },
                   headers: {
                       "X-CSRFToken": this.get_cookie("csrftoken"),
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
    }
}
</script>

<style scoped>
</style>
