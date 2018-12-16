// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import { sync } from 'vuex-router-sync'
import VueI18n from 'vue-i18n'
import App from './App'
import router from './router'
import state from './state'
import VueState from './plugins/state'
import VueFetch, { $fetch } from './plugins/fetch'
import * as filters from './filters'
import { messages } from './messages';
import store from './store';

Vue.use(VueI18n)
Vue.use(VueState, state)

Vue.config.productionTip = false

for (const key in filters) {
  Vue.filter(key, filters[key])
}

const i18n = new VueI18n({
    locale: 'fr',
    messages
})

sync(store, router)

async function main () {
    try {
        //state.user = await $fetch('user')
        await store.dispatch('user/init')
    } catch (e) {
        console.warn(e)
    }

    /* eslint-disable no-new */
    new Vue({
        ...App,
      el: '#app',
      //data: state,
      router,
      store,
      i18n
    })
}

main ()
