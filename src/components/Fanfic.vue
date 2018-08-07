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
                <div>Description : {{ fanfic.description }}</div>
            </section>
            <section class="content">
                <ul>
                    <li v-for="(chap, index) in chapter" v-if="chap.fanfic === fanfic.id" :key="chap.id" :index="index">
                        {{ chap.title }} - Publié le {{ chap.published | date }}

                        <router-link :to="{name: 'UpdateChapter', params: { chapter_id: chap.id, id: fanfic.id } }" title="Editer un chapitre" class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker"><svgicon icon="edit-pencil" width="22" height="18" color="#000"></svgicon> </router-link>

                        <button type="button" title="Supprimer le chapitre" @click="deleteChapter(chap.id, index)"><svgicon icon="trash" width="22" height="18" color="#000"></svgicon></button>
                    </li>
                </ul>
            </section>
            <section class="action">
                <div>
                    <router-link class="mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker" :to="{name: 'NewChapter', params: { id: fanfic.id }}">Ajouter un chapitre</router-link>
                </div>
            </section>
        </template>
    </div>
</template>

<script>
import RemoteData from '../mixins/RemoteData'
import get_cookie from '../cookie'
import '../compiled-icons/trash'
import '../compiled-icons/edit-pencil'

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
        async deleteChapter (chapterId, index) {
            let message = confirm('Supprimer le chapitre ? id# ' + chapterId)

            if (message == true) {
                $.ajax({
                   url: '/api/chapters/' + chapterId,
                   type: 'DELETE',
                   headers: {
                       "X-CSRFToken": get_cookie("csrftoken"),
                   },
                   data: { id: chapterId },
                   success: function() {
                       console.log("ok");
                       this.chapter.splice(index, 1);
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
