<template>
    <div class="flex flex-wrap">
        <div class="w-full sm:w-1/2 md:w-1/4 mb-4">

              <p>{{ $t('message.connexionUser', [user.username])}}.</p>
              <ul class="list-reset">
                 <li> <router-link v-if="$route.name !== 'ListUserFanfic'" tag="button" :to="{name: 'ListUserFanfic'}">
                      {{ $t('message.myStoriesLabel') }}
                  </router-link></li>
                  <li><router-link v-if="$route.name !== 'NewFanfic'" tag="button" :to="{name: 'NewFanfic'}">
                      {{ $t('message.ecrireFanfictions') }}
                  </router-link></li>

                  <li><router-link v-if="$route.name !== 'EditAccount'" tag="button" :to="{ name: 'EditAccount' }">
                      {{ $t('message.changeProfileEdit') }}
                  </router-link></li>

                  <li><button class="text-red hover:text-red-darker" @click.prevent="disableAccount">
                    {{ $t('message.removeAccountLabel') }}
                </button></li>
              </ul>
          </div>
          <div class="w-full sm:w-1/2 md:w-3/4 mb-4">

              <router-view />

          </div>
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
