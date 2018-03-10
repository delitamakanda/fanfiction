// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import state from './state'
import VueState from './plugins/state'
import VueFetch, { $fetch } from './plugins/fetch'
import * as filters from './filters'

Vue.use(VueState, state)

Vue.config.productionTip = false

for (const key in filters) {
  Vue.filter(key, filters[key])
}

async function main () {
    try {
        state.user = await $fetch('user')
        console.log(state.user);
    } catch (e) {
        console.warn(e)
    }

    /* eslint-disable no-new */
    new Vue({
      el: '#app',
      data: state,
      router,
      components: { App },
      template: '<App/>'
    })
}

main ()
