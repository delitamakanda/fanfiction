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
                <div v-for="(chap, i) of chapter" v-if="chap.fanfic === fanfic.id">
                    &bull; {{ chap.title }} - Publié le {{ chap.published | date }} - <router-link :to="{name: 'UpdateChapter', params: { chapter_id: chap.id, id: fanfic.id } }">Editer le chapitre </router-link>
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
                    this.$fetch(`fanfics/${this.id}`, {method: 'DELETE', body: JSON.stringify(result)})
                    this.$router.push({ name: 'Dashboard' })
                }
            }

        }

    }
}
</script>
