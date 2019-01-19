// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'babel-polyfill'

import Vue from 'vue'
import { sync } from 'vuex-router-sync'
import App from './App'
import router from './router'
import state from './state'
import VueState from './plugins/state'
import VueFetch, { $fetch } from './plugins/fetch'
import * as filters from './filters'
import { i18n } from './plugins/i18n';
import store from './store';

Vue.use(VueState, state)

Vue.config.productionTip = false

for (const key in filters) {
  Vue.filter(key, filters[key])
}

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
