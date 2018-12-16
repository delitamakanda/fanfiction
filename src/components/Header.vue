<template>
    <nav class="flex items-center justify-between flex-wrap bg-white p-6 shadow">
        <div class="flex items-center flex-no-shrink text-teal mr-6">
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
                <router-link :to="{ name: 'List' }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4">Lire des histoires</router-link>
                <template v-if="user && user.id != null">
                    <router-link :to="{ name: 'Dashboard' }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">Bonjour, {{ user.username }} !</router-link>
                    <a href="javascript:void(0)" @click="disconnect" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4 cursor-pointer">Déconnexion </a>
                </template>
                <router-link v-else :to="{ name: 'Login' }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4">Se connecter</router-link>
                <router-link :to="{ name: 'News' }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4">News</router-link>
                <ul class="menu list-reset block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker mr-4">
                    <li @mouseover="survol = true" @mouseleave="survol = false"><svgicon icon="question" width="22" height="18" color="#4dc0b5"></svgicon> Aide
                        <transition name="fade" mode="out-in">
                            <ul class="bg-white p-4 shadow " v-if="survol" @click="survol = false">
                                <li><a class="text-teal hover:text-teal-darker" href="/help/browse/title">Lexique</a></li>
                                <li><a class="text-teal hover:text-teal-darker" href="/help/faq">Foire aux questions</a></li>
                                <li><a class="text-teal hover:text-teal-darker" href="/help/forum">Forum</a></li>
                                <li><a href="#" class="text-teal hover:text-teal-darker" @click="openModalContact">Contacter le webmestre</a></li>
                            </ul>
                        </transition>
                    </li>
                </ul>
                <modal
                  v-show="isModalContactVisible"
                      @close="closeModalContact"
                    >

                    <h3 slot="header">Formulaire de contact</h3>
                    <div slot="body">
                        <Form
                            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
                            title=""
                            :operation="operation"
                            :valid="valid">
                                <div v-if="user && user.id != null">
                                    &nbsp;
                                </div>
                                <div class="mb-4" v-else>
                                    <label class="block text-grey-darker text-sm font-bold mb-2" for="from_email">
                                        E-mail
                                    </label>
                                    <Input
                                        name="from_email"
                                        type="email"
                                        v-model="from_email"
                                        placeholder="E-mail"
                                        required />
                                </div>
                                <div class="mb-6">
                                    <label class="block text-grey-darker text-sm font-bold mb-2" for="subject">
                                        Sujet du message
                                    </label>
                                    <Input
                                        name="subject"
                                        type="text"
                                        v-model="subject"
                                        placeholder="Sujet du message" />
                                </div>
                                <div class="mb-6">
                                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="message">
                                      Message
                                    </label>
                                    <Input
                                        type="textarea"
                                        name="message"
                                        v-model="message"
                                        placeholder="Message"
                                        maxlength="1000"
                                        rows="4" />
                                </div>
                                <template slot="actions">
                                    <div class="flex items-center justify-between">
                                        <button
                                        class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                                        type="submit"
                                        :disabled="!valid">
                                            Envoyer le message
                                        </button>
                                    </div>
                                </template>

                        </Form>
                    </div>
                </modal>
            </div>
        </div>
    </nav>
</template>

<script>
import '../compiled-icons/question'
import modal from './Modal.vue'
import { mapActions, mapGetters } from 'vuex'

export default {
    props: {
        title: {
            type: String,
            required: true
        }
    },
    components: {
        modal
    },
    data(){
        return{
            isModalContactVisible: false,
            open: false,
            survol: false,
            from_email: '',
            subject: '',
            message: ''
        }
    },
    computed: {
        ...mapGetters('user', ['user']),
        valid () {
            return !!this.subject && !!this.message
        },
    },
    methods: {
        ...mapActions('user', ['logout']),
        toggle (){
            this.open = !this.open
        },
        /*async logout () {
            const result = await this.$fetch('logout')
            if (result.status === 'ok') {
            this.$state.user.id = null
            if (this.$route.matched.some(m => m.meta.private)) {
            this.$router.push({ name: 'Login', params: {wantedRoute: this.$router.currentRoute.fullPath } })
        }
        }
        },*/
        disconnect() {
            this.logout()
        },
        openModalContact () {
            this.isModalContactVisible = true;
        },
        closeModalContact() {
            this.isModalContactVisible = false;
        },
        async operation () {
            const result = await this.$fetch('contact-mail', {
                method: 'POST',
                body: JSON.stringify({
                    from_email: (this.user && this.user.id != null ? this.user.email : this.from_email),
                    subject: this.subject,
                    message: this.message
                }),
            })
            this.from_email = this.subject = this.message = ''
            this.isModalContactVisible = false
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
