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
            <section class="action">
                <div> chapter - <a href="">Ajouter un chapitre</a> - <a href="">Editer</a> - <a href="#">Supprimer</a></div>
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
        }),
    ],
    props: {
        id: {
            type: Number,
            required: true,
        },
    },
}
</script>
