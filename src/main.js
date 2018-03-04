// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import state from './state'
import VueState from './plugins/state'
import VueFetch, { $fetch } from './plugins/fetch'

Vue.use(VueState, state)

Vue.config.productionTip = false

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
      template: '<App/>'
    })
}

main ()
