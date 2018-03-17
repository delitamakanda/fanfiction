<template>
    <div class="fanfic">
        <h2>{{ fanfic.title }}</h2>
        <Loading v-if="remoteDataBusy" />
        <div class="empty" v-else-if="!fanfic">
            Fanfiction non trouvée.
        </div>
        <template v-else>
            <section class="infos">
                <div class="info">
                    Crée le {{ fanfic.created | date }}
                </div>
                <div class="info">
                    Mis à jour le {{ fanfic.updated | date }}
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
                <div v-for="(chap, i) of chapter" v-if="chap.fanfic === fanfic.id">
                    &bull; {{ chap.title }} - Publié le {{ chap.published | date }} - <a href="">Editer le chapitre </a>
                </div>
            </section>
            <section class="action">
                <div><a href="">Ajouter un chapitre</a> - <a href="">Editer l'histoire</a> - <a href="#">Supprimer l'histoire</a></div>
            </section>
        </template>
    </div>
</template>

<script>
import RemoteData from '../mixins/RemoteData'

export default {
    mixins: [
        RemoteData({
            fanfic () {
                return `fanfics/v1/${this.id}`
            },
            chapter () {
                return `chapters`
            }
        }),
    ],
    data () {
        return {
            nbChapter: ''
        }
    },
    props: {
        id: {
            type: Number,
            required: true,
        },
    },
    created () {
        this.nbChapter = 0
    }
}
</script>
