<template>
    <div>
        <h1>{{ subtitle }}</h1>
        <Loading v-if="loading" />

        <div class="empty" v-else-if='userFanfics.length === 0'>
            Vous n'avez pas encore de fanfictions. Libérer votre créativité !
        </div>

        <section v-else class="fanfictions-list">
            <div v-for="userFanfic of userFanfics">
                <h3 v-html="userFanfic.title"></h3>
                <span>{{ userFanfic.category }} {{ userFanfic.subcategory }} {{ userFanfic.genres }} {{ userFanfic.classement }}</span>
                <p>{{ userFanfic.created | date }}</p>
                <p>{{ userFanfic.updated | date }}</p>
                <p v-if="userFanfic.synopsis">{{ userFanfic.synopsis }}</p>
                <p v-html="userFanfic.status"></p>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    name: 'Dashboard',
    data(){
        return{
            subtitle: 'Vos fanfictions',
            error: null,
            userFanfics: [],
            loading: false,
        }
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
