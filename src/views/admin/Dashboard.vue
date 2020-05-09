<template>
    <div class="w-full flex flex-row flex-wrap">
        <div class="w-full bg-indigo-100 h-screen flex flex-row flex-wrap justify-center">
            <div class="bg-white shadow-lg border-t-4 border-indigo-500 absolute bottom-0 w-full md:w-0 md:hidden flex flex-row flex-wrap">
                <div class="w-full text-right"><button class="p-2 fa fa-bars text-4xl text-gray-600"></button></div>
            </div>
            
            <div class="w-0 md:w-1/4 lg:w-1/5 h-0 md:h-screen overflow-y-hidden bg-white shadow-lg">
                <div class="p-5 bg-white sticky top-0">
                <avatar ref="avatar" :email="user.email" class="max-width-100  border border-indigo-100 shadow-lg rounded-full mx-auto" />
                <div class="pt-2 border-t mt-5 w-full text-center text-xl text-gray-600" v-html="$t('message.connexionUser', [user.username])">
                </div>
                <div class="pt-2 border-t mt-5 w-full text-center text-xl text-gray-600">
                    {{ $t('message.dateJoined') }} {{ user.date_joined | date }}
                </div>
                </div>
                <div class="w-full h-screen antialiased flex flex-col hover:cursor-pointer">
                <router-link class="hover:bg-gray-300 bg-gray-200 border-t-2 p-3 w-full text-xl text-left text-gray-600 font-semibold" v-if="$route.name !== 'ListUserFanfic'" tag="button" :to="{name: 'ListUserFanfic', params: { username: user.username, isPrivate: true }}">
                    <svgicon class="pr-1 pt-1 float-right" icon="book-reference" width="22" height="auto" color="#718096"></svgicon>
                    {{ $t('message.myStoriesLabel') }}
                </router-link>

                <router-link class="hover:bg-gray-300 bg-gray-200 border-t-2 p-3 w-full text-xl text-left text-gray-600 font-semibold" v-if="$route.name !== 'NewFanfic'" tag="button" :to="{name: 'NewFanfic'}">
                    <svgicon class="pr-1 pt-1 float-right" icon="edit-pencil" width="22" height="auto" color="#718096"></svgicon>
                    {{ $t('message.ecrireFanfictions') }}
                </router-link>
                
                <router-link v-if="user && user.is_staff" class="hover:bg-gray-300 bg-gray-200 border-t-2 p-3 w-full text-xl text-left text-gray-600 font-semibold" tag="button" :to="{name: 'AddNews'}">
                    <svgicon class="pr-1 pt-1 float-right" icon="list" width="22" height="auto" color="#718096"></svgicon>
                    {{ $t('message.newsEditingLabel') }}
                </router-link>
                
                <router-link class="hover:bg-gray-300 bg-gray-200 border-t-2 p-3 w-full text-xl text-left text-gray-600 font-semibold" v-if="$route.name !== 'EditAccount'" tag="button" :to="{ name: 'EditAccount' }">
                    {{ $t('message.changeProfileEdit') }}
                </router-link>
                
                <button class="hover:bg-gray-300 bg-gray-200 border-t-2 p-3 w-full text-xl text-left text-gray-600 font-semibold" @click.prevent="disableAccount">
                    {{ $t('message.removeAccountLabel') }}
                </button>

                <button class="hover:bg-gray-300 bg-gray-200 border-t-2 p-3 w-full text-xl text-left text-gray-600 font-semibold" @click.prevent="disconnect">{{ $t('message.logoutLabel')}} </button>
                </div>
            </div>
            
            <!-- End Navbar -->
            
            <div class="w-full md:w-3/4 lg:w-4/5 p-5 md:px-12 lg:24 h-full overflow-x-scroll antialiased">
                <div class="bg-white w-full shadow rounded-lg p-5">
                    <router-view />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import '@/compiled-icons/book-reference'
import '@/compiled-icons/edit-pencil'
import '@/compiled-icons/list'
import '@/compiled-icons/inbox'

import { mapGetters, mapActions } from 'vuex'

export default {
    computed: {
        ...mapGetters('user', ['user'])
    },
    methods: {
        ...mapActions('user', ['removeAccount', 'logout']),
        async disableAccount () {
            let message = confirm(this.$t('message.removeAccountText'))

            if (message === true) {
                this.removeAccount()
            }

        },
        disconnect() {
            this.logout()
        }
    }
}
</script>

<style scoped>
.max-width-100 {
    width: 100%;
}
</style>
