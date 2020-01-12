import Vue from 'vue'
import Vuex from 'vuex'

import * as comment from './state/comment'
import * as fanfic from './state/fanfic'
import * as other from './state/other'
import * as user from './state/user'
import * as help from './state/help'

Vue.use(Vuex)

const store = new Vuex.Store({
    strict: true,
    modules: {
        comment,
        fanfic,
        other,
        user,
        help
    }
})

export default store
