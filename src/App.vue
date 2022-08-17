<template>
    <div id="app" class="container mx-auto px-4">
        <app-header v-bind:title="title"></app-header>
        <transition name="fade" mode="out-in">
            <router-view :key="$route.fullPath" />
        </transition>
        <toggle-provider :on="true">
        <template #default="{ isOn, turnOff, turnOn, toggle }">
            <div>
                <div>
                    <button @click.prevent="turnOn">ON</button>
                    <button @click.prevent="turnOff">OFF</button>
                    <button @click.prevent="toggle">TOGGLE</button>
                </div>
                <div v-if="isOn">
                    ToggleProvider is working
                </div>
            </div>
        </template>
        </toggle-provider>
        <app-footer v-bind:title="title"></app-footer>
        <transition appear name="slideFromBottom">
            <div class="cookie bottom" v-if="isOpen">
                <div class="cookie__content">
                    {{ $t('message.cookieMessage') }}
                </div>
                <div class="cookie__buttons">
                    <div class="cookie__button" @click="accept">{{ $t('message.agreedLabel') }}</div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
import * as Cookie from 'tiny-cookie'

import '@/assets/styles/main.css'

import Header from './components/ui/Header.vue';
import Footer from './components/ui/Footer.vue';
import ToggleProvider from './components/ToggleProvider';

import { mapGetters } from 'vuex'

export default {
    name: 'App',
    components: {
        'app-header': Header,
        'app-footer': Footer,
        'toggle-provider': ToggleProvider
    },
    data () {
        return {
            title: 'Fanfiction',
            isOpen: false,
            supportsLocalStorage: true
        };
    },
    computed: {
        ...mapGetters('user', ['user'])
    },
    created () {
        // Check for availability of localStorage
        try {
            const test = '__vue-cookielaw-check-localStorage'
            window.localStorage.setItem(test, test)
            window.localStorage.removeItem(test)
        } catch (e) {
            console.error('Local storage is not supported, falling back to cookie use')
            this.supportsLocalStorage = false
        }
        if (!this.getVisited() === true) {
            this.isOpen = true
        }
    },
    methods: {
        setVisited () {
            if (this.supportsLocalStorage) {
                localStorage.setItem('cookie:accepted', true)
            } else {
                Cookie.set('cookie:accepted', true)
            }
        },
        getVisited () {
            if (this.supportsLocalStorage) {
                return localStorage.getItem('cookie:accepted')
            } else {
                return Cookie.get('cookie:accepted')
            }
        },
        accept () {
            this.setVisited()
            this.isOpen = false
            this.$emit('accept')
        }
    }
}
</script>

<style>
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
    margin-top: 15px;
}

.cookie {
    position: fixed;
    overflow: hidden;
    box-sizing: border-box;
    z-index: 9999;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-direction: row;
    background: #fff;
    color: #4dc0b5;
    padding: 1.250em;
    border-top: 1px solid #4dc0b5;
}

.cookie > * {
    align-self: center;
}

.cookie.bottom {
    bottom: 0;
    left: 0;
    right: 0;
}

.cookie__buttons {
    margin-top: 5px;
    display: flex;
    flex-direction: column;
}

.cookie__button {
    background: #4dc0b5;
    padding: 0.625em 3.125em;
    color: #fff;
    border-radius: 20px;
    cursor: pointer;
}
.cookie__button:hover {
    background: #38a89d;
    color: #fff;
}
.slideFromBottom-enter, .slideFromBottom-leave-to {
    transform: translate(0px, 12.500em);
}
.slideFromBottom-enter-to, .slideFromBottom-leave {
    transform: translate(0px, 0px);
}
.slideFromBottom-enter-active,
.slideFromBottom-leave-active {
    transition: transform .4s ease-in;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity .1s;
}

.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
}

</style>
