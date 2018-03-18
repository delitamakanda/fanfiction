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
                    Crée le {{ fanfic.publish | date }}
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
                    &bull; {{ chap.title }} - Publié le {{ chap.published | date }} - <router-link :to="{name: 'UpdateChapter', params: { chapter_id: chap.id }}">Editer le chapitre </router-link>
                </div>
            </section>
            <section class="action">
                <div>
                    <router-link :to="{name: 'NewChapter', params: { id: fanfic.id }}">Ajouter un chapitre</router-link> - <router-link :to="{name: 'UpdateFanfic', params: { id: fanfic.id }}">Editer l'histoire</router-link> - <button @click.prevent="deleteStory(fanfic.id)">Supprimer l'histoire</button></div>
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
            data: null
        }
    },
    props: {
        id: {
            type: Number,
            required: true,
        },
    },
    methods: {
        async deleteStory (id) {
            let message = confirm('Etes vous certain de supprimer cette histoire ?')

            if (message == true) {
                //console.log(id)
                const result = await this.$fetch('fanfics/'+ id)

                if (result) {
                    fetch(`api/fanfics/${this.id}`, {method: 'DELETE', credentials: 'include', body: JSON.stringify(result)})
                    this.$router.push({ name: 'Dashboard' })
                }
            }

        }

    }
}
</script>
