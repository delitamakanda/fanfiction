import Vue from 'vue'
import Vuex from 'vuex'

import * as comment from './state/comment'
import * as fanfic from './state/fanfic'
import * as other from './state/other'
import * as user from './state/user'

Vue.use(Vuex)

const store = new Vuex.Store({
    strict: true,
    modules: {
        comment,
        fanfic,
        other,
        user
    }
})

export default store
