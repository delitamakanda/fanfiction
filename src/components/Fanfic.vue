<template>
    <div class="fanfic">
        <Loading v-if="remoteDataBusy" />
        <div class="empty" v-else-if="!fanfic">
            Fanfiction non trouvée.
        </div>
        <template v-else>
            <section class="infos">
                <h2>{{ fanfic.title }}</h2>
                <div class="info">
                    Crée le {{ fanfic.publish | date }}
                </div>
            </section>
            <section class="content">
                <div>Synopsis : {{ fanfic.synopsis }}</div>
                <div>Credits : {{ fanfic.credits }}</div>
                <div>Status : {{ fanfic.status }}</div>
                <div>Genres : {{ fanfic.genres }}</div>
                <div>Classement : {{ fanfic.classement }}</div>
                <div>Catégorie : {{ fanfic.category }}</div>
                <div>Sous - Catégorie : {{ fanfic.subcategory }}</div>
                <div>Description : {{ fanfic.description }}</div>
            </section>
            <section class="content">
                <ul>
                    <li v-for="(chap, i) in chapter" v-if="chap.fanfic === fanfic.id" :key="chap.id">
                        {{ chap.title }} - Publié le {{ chap.published | date }} - <router-link :to="{name: 'UpdateChapter', params: { chapter_id: chap.id, id: fanfic.id } }" class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">Editer le chapitre </router-link> - <button type="button" class="text-red hover:text-red-darker" @click="deleteChapter(chap.id)">Supprimer le chapitre</button>
                    </li>
                </ul>
            </section>
            <section class="action">
                <div>
                    <router-link class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" :to="{name: 'NewChapter', params: { id: fanfic.id }}">Ajouter un chapitre</router-link> - <router-link class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" :to="{name: 'UpdateFanfic', params: { id: fanfic.id }}">Editer l'histoire</router-link> - <button class="text-red hover:text-red-darker" @click="deleteStory(fanfic.id)">Supprimer l'histoire</button>
                </div>
            </section>
        </template>
    </div>
</template>

<script>
import RemoteData from '../mixins/RemoteData'

export default {
    name: 'Fanfic',
    mixins: [
        RemoteData({
            fanfic () {
                return `fanfics/${this.id}`
            },
            chapter () {
                return `chapters`
            }
        }),
    ],
    data () {
        return {
            fanfic: [],
            chapter: [],
        }
    },
    props: {
        id: {
            type: Number,
            required: true,
        },
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

        async deleteStory (id) {
            let message = confirm('Etes vous certain de supprimer cette histoire ? id# ' + id)

            if (message == true) {

                $.ajax({
                   url: '/api/fanfics/' + id,
                   type: 'DELETE',
                   data: { id: id },
                   headers: {
                       "X-CSRFToken": this.get_cookie("csrftoken"),
                   },
                   success: function() {
                       this.$router.push({ name: 'Dashboard' })
                   }.bind(this),
                   error: function(error) {
                       console.log(error);
                   }
                });
            }

        },

        async deleteChapter (chapterId) {
            let message = confirm('Supprimer le chapitre ? id# ' + chapterId)

            if (message == true) {
                $.ajax({
                   url: '/api/chapters/' + chapterId,
                   type: 'DELETE',
                   headers: {
                       "X-CSRFToken": this.get_cookie("csrftoken"),
                   },
                   data: { id: chapterId },
                   success: function() {
                       console.log("ok");
                   }.bind(this),
                   error: function(error) {
                       console.log(error);
                   }
                });



            }
        }

    }
}
</script>
