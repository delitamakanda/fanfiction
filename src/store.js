import Vue from 'vue'
import Vuex from 'vuex'

import * as fanfic from './state/fanfic'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        fanfic
    }
})
