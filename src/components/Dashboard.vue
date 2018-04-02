<template>
    <div>
        <p>Vous êtes connecter en tant que {{ user.username }}.</p>
        <Loading v-if="loading" />

        <router-link v-if="$route.name !== 'ListUserFanfic'" class="secondary" tag="button" :to="{name: 'ListUserFanfic'}">
            Voir mes fanfictions
        </router-link>
        <router-link v-if="$route.name !== 'NewFanfic'" tag="button" :to="{name: 'NewFanfic'}">
            Ecrire une fanfiction
        </router-link>

        <router-link v-if="$route.name !== 'ChangePassword'" tag="button" :to="{ name: 'ChangePassword' }">
            Changer le mot de passe
        </router-link>

        <router-view />
    </div>
</template>

<script>
export default {
    name: 'Dashboard',
    data(){
        return{
            error: null,
            user: [],
            loading: false,
        }
    },
    async created () {
        this.loading = true
        try {
            this.user = await this.$fetch('user')
        } catch (e) {
            this.error = e
        }
        this.loading = false
    },
}
</script>

<style scoped>
</style>
