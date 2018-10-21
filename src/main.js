// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueI18n from 'vue-i18n'
import App from './App'
import router from './router'
import state from './state'
import VueState from './plugins/state'
import VueFetch, { $fetch } from './plugins/fetch'
import * as filters from './filters'
import { messages } from './messages';

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

async function main () {
    try {
        state.user = await $fetch('user')
    } catch (e) {
        console.warn(e)
    }

    /* eslint-disable no-new */
    new Vue({
      el: '#app',
      data: state,
      router,
      components: { App },
      template: '<App/>',
      i18n
    })
}

main ()
