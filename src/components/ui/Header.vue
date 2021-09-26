<template>
    <nav class="flex items-center justify-between flex-wrap bg-white p-6 shadow">
        <div class="flex items-center flex-shrink-0 text-teal mr-6">
            <svg width="23.999999999999996" height="23.999999999999996" xmlns="http://www.w3.org/2000/svg">
             <g>
              <title>background</title>
              <rect fill="none" id="canvas_background" height="402" width="582" y="-1" x="-1"/>
             </g>
             <g>
              <title>Layer 1</title>
              <path id="svg_2" fill="#16a085" d="m3,8l0,2l0,1l0,3l0,1l0,5l0,1c0,1.105 0.8954,2 2,2l14,0c1.105,0 2,-0.895 2,-2l0,-1l0,-5l0,-4l0,-3l-18,0z"/>
              <path id="svg_3" fill="#ecf0f1" d="m3,6.999976l0,2l0,1l0,3l0,1l0,5l0,1c0,1.1 0.8954,2 2,2l14,0c1.105,0 2,-0.9 2,-2l0,-1l0,-5l0,-4l0,-3l-18,0z"/>
              <path id="svg_4" fill="#bdc3c7" d="m3,5.999976l0,2l0,1l0,3l0,1l0,5l0,1c0,1.1 0.8954,2 2,2l14,0c1.105,0 2,-0.9 2,-2l0,-1l0,-5l0,-4l0,-3l-18,0z"/>
              <path id="svg_5" fill="#ecf0f1" d="m3,4.999976l0,2l0,1l0,3l0,1l0,5l0,1c0,1.1 0.8954,2 2,2l14,0c1.105,0 2,-0.9 2,-2l0,-1l0,-5l0,-4l0,-3l-18,0z"/>
              <path id="svg_6" fill="#16a085" d="m5,1c-1.1046,0 -2,0.8954 -2,2l0,1l0,4l0,2l0,1l0,3l0,1l0,5l0,1c0,1.105 0.8954,2 2,2l2,0l0,-1l-1.5,0c-0.8284,0 -1.5,-0.672 -1.5,-1.5s0.6716,-1.5 1.5,-1.5l12.5,0l1,0c1.105,0 2,-0.895 2,-2l0,-1l0,-5l0,-4l0,-3l0,-1c0,-1.1046 -0.895,-2 -2,-2l-4,0l-10,0z"/>
              <path id="svg_7" fill="#1abc9c" d="m8,1l0,18l1,0l9,0l1,0c1.105,0 2,-0.895 2,-2l0,-1l0,-5l0,-4l0,-3l0,-1c0,-1.1046 -0.895,-2 -2,-2l-4,0l-6,0l-1,0z"/>
             </g>
            </svg>
            <span class="font-semibold text-xl tracking-tight">{{ title }}</span>
        </div>
        <div class="block lg:hidden">
            <button @click="toggle" class="flex items-center px-3 py-2 border rounded text-teal-lighter border-teal-light hover:text-teal hover:border-white">
              <svg class="fill-current h-3 w-3" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><title>Menu</title><path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"/></svg>
            </button>
        </div>
        <div :class="open ? 'block': 'hidden'" class="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
            <div class="text-sm lg:flex-grow">
                <router-link :to="{ name: 'List' }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4">{{ $t('message.lireFanfictionsLabel') }}</router-link>
                <template v-if="user && user.id != null">
                    <router-link :to="{ name: 'Dashboard' }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ $t('message.greetLabel')}}, {{ user.username }} !</router-link>
                    <a href="javascript:void(0)" @click="disconnect()" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4 cursor-pointer">{{ $t('message.logoutLabel')}} </a>
                </template>
                <router-link v-else :to="{ name: 'Login' }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4">{{ $t('message.loginLabel')}}</router-link>
                <ul v-if="user && user.id != null" class="menu list-reset block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4">
                    <li @mouseover="survol2 = true" @mouseleave="survol2 = false" class="inline-flex"><svgicon icon="notifications-outline" width="22" height="18" color="#4dc0b5"></svgicon> {{ $t('message.NotificationsLabel') }}
                        <transition name="fade" mode="out-in">
                            <ul class="bg-white p-4 shadow z-10" v-if="survol2" @click="survol2 = false">
                                <li v-for="notification in notifications" :key="notification.id">
                                    {{ notification.user.username }} {{ notification.verb }} {{ notification.target }} - {{ notification.created | date }}
                                </li>
                            </ul>
                        </transition>
                    </li>
                </ul>
                <ul class="menu list-reset block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4">
                    <li @mouseover="survol = true" @mouseleave="survol = false" class="inline-flex "><svgicon icon="question" width="22" height="18" color="#4dc0b5"></svgicon> {{ $t('message.aideLabel') }}
                        <transition name="fade" mode="out-in">
                            <ul class="bg-white p-4 z-10 shadow " v-if="survol" @click="survol = false">
                                <li><a class="text-teal hover:text-teal-darker" href="/help/forum">{{ $t('message.forumLabel') }}</a></li>
                                <li><a href="#" class="text-teal hover:text-teal-darker" @click="openContactForm">{{ $t('message.contactLabel') }}</a></li>
                            </ul>
                        </transition>
                    </li>
                </ul>
            </div>
        </div>
        <popin ref="contact"></popin>
    </nav>
</template>

<script>
import '@/compiled-icons/question'
import '@/compiled-icons/notifications-outline'
import popin from '@/components/popins/PopinContactForm.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default {
    created () {
        if (this.user && this.user.id != null) {
            this.getNotifications();
        }
    },
    mounted () {
      this.$root.$contact = this.$refs.contact.openModal
    },
    props: {
        title: {
            type: String,
            required: true
        }
    },
    components: { popin },
    data(){
        return{
            open: false,
            survol: false,
            survol2: false
        }
    },
    computed: {
        ...mapGetters('user', ['user']),
        ...mapState('other', ['notifications'])
    },
    methods: {
        ...mapActions('user', ['logout']),
        ...mapActions('other', ['getNotifications', 'clearNotifications', 'sendFormContactEmail']),
        openContactForm () {
          this.$root
            .$contact()
            .then(res => {
                if (res.status) {
                    let data = res.r
                    this.sendFormContactEmail(data)
                }
            }).catch(err => console.log(err))
        },
        toggle (){
            this.open = !this.open
        },
        disconnect() {
            this.logout()
        }
    },
    watch: {
        user(val,old) {
            if (this.user && this.user.id != null) {
                this.getNotifications();
            } else {
                this.clearNotifications();
            }
        }
    }
}
</script>

<style scoped>
nav {
    margin-bottom: 14px;
}
.menu li {
    position: relative;
    min-width: 180px;
}
.menu li ul {
    position: absolute;
    left: 0;
    top: 1.5rem;
    list-style-type: disc;
    list-style-position: inside;
}
</style>
