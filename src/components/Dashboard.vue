<template>
    <div class="px-6 py-4">
        <Loading v-if="loading" />

              <p>Vous êtes connecter en tant que {{ user.username }}.</p>

              <router-link v-if="$route.name !== 'ListUserFanfic'" tag="button" :to="{name: 'ListUserFanfic'}">
                  Voir mes fanfictions
              </router-link>
              <router-link v-if="$route.name !== 'NewFanfic'" tag="button" :to="{name: 'NewFanfic'}">
                  Ecrire une fanfiction
              </router-link>

              <router-link v-if="$route.name !== 'ChangePassword'" tag="button" :to="{ name: 'ChangePassword' }">
                  Changer le mot de passe
              </router-link>

              <button class="bg-red hover:bg-red-dark text-white font-bold py-2 px-4 rounded block" @click.prevent="disableAccount">
                Supprimer le compte
              </button>

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
    methods: {
        async disableAccount () {
            let message = confirm("Après la suppression, votre compte sera désactivé et aucune opération ne pourra être effectuer. Supprimer le compte ?")

            if (message === true) {
                const result = await this.$fetch('disable-account')
                if (result.status === 'ok') {
                    this.$state.user = null
                    if (this.$route.matched.some(m => m.meta.private)) {
                        this.$router.push({ name: 'List' })
                    }
                }
            }

        }
    }
}
</script>

<style scoped>
</style>
