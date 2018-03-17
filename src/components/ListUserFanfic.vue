<template>
    <div>
        <h1>{{ subtitle }}</h1>
        <Loading v-if="loading" />

        <div class="empty" v-else-if='userFanfics.length === 0'>
            Vous n'avez pas encore de fanfictions. Libérer votre créativité !
        </div>

        <section v-else class="fanfictions-list">
            <div v-for="userFanfic of userFanfics">
                <router-link :to="{name: 'fanfic', params: { id: userFanfic.id }}"> <h3>{{ userFanfic.title }}</h3> </router-link>
            </div>
        </section>

        <!--<Fanfic v-if="id" :id="id" />-->

        <router-view />
    </div>
</template>

<script>
import Fanfic from './Fanfic.vue'

export default {
    name: 'ListUserFanfic',
    data(){
        return{
            subtitle: 'Vos fanfictions',
            error: null,
            userFanfics: [],
            loading: false,
            id: null,
        }
    },
    components: {
        Fanfic,
    },
    async created () {
        this.loading = true
        try {
            this.userFanfics = await this.$fetch('fanfics/author/' + this.$state.user.username)
        } catch (e) {
            this.error = e
        }
        this.loading = false
    },
}
</script>

<style scoped>
</style>
