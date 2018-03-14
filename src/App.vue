<template>
  <div id="app" class="container mx-auto">
      <app-header v-bind:title="title"></app-header>
      <transition name="fade" mode="out-in">
        <router-view />
    </transition>
      <app-footer v-bind:title="title"></app-footer>
  </div>
</template>

<script>
import '@/assets/styles/main.css'

import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

export default {
  name: 'App',
  components: {
      'app-header': Header,
      'app-footer': Footer,
  },
  data () {
      return {
          title: 'Fanfiction',
      };
  },
  methods: {}
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

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}

.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
