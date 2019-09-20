<template>
    <div>
        <nav class="flex items-center justify-between flex-wrap p-6">
            <div class="flex items-center flex-shrink-0 text-white mr-6">
                <avatar ref="avatar" :email="user.email" />
            </div>
            <div class="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
                <div class="text-sm lg:flex-grow">
                    <div class="block mt-4 lg:block lg:mt-0" v-html="$t('message.connexionUser', [user.username])"></div>
                    <div class="block mt-4 lg:block lg:mt-0">({{ $t('message.dateJoined') }} {{ user.date_joined | date }}).</div>
                </div>
            </div>
            <div class="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
                <div class="text-sm lg:flex-grow">
                 <router-link class="block mt-4 lg:inline-block lg:mt-0 text-teal-500 hover:text-teal-800" v-if="$route.name !== 'ListUserFanfic'" tag="button" :to="{name: 'ListUserFanfic'}">
                      {{ $t('message.myStoriesLabel') }}
                  </router-link>
                  <router-link class="block mt-4 lg:inline-block lg:mt-0 text-teal-500 hover:text-teal-800" v-if="$route.name !== 'NewFanfic'" tag="button" :to="{name: 'NewFanfic'}">
                      {{ $t('message.ecrireFanfictions') }}
                  </router-link>
                  <router-link class="block mt-4 lg:inline-block lg:mt-0 text-teal-500 hover:text-teal-800" tag="button" :to="{name: 'Reviews'}">
                       {{ $t('message.commentairesLabel') }}
                  </router-link>
                  <router-link class="block mt-4 lg:inline-block lg:mt-0 text-teal-500 hover:text-teal-800" v-if="$route.name !== 'EditAccount'" tag="button" :to="{ name: 'EditAccount' }">
                      {{ $t('message.changeProfileEdit') }}
                  </router-link>
                  <button class="block mt-4 lg:inline-block lg:mt-0 text-red-500 hover:text-red-800" @click.prevent="disableAccount">
                    {{ $t('message.removeAccountLabel') }}
                </button>
                  </div>
              </div>
          </nav>
        <router-view />
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
    computed: {
        ...mapGetters('user', ['user'])
    },
    methods: {
        ...mapActions('user', ['removeAccount']),
        async disableAccount () {
            let message = confirm(this.$t('message.removeAccountText'))

            if (message === true) {
                this.removeAccount()
            }

        }
    }
}
</script>

<style scoped>
</style>
