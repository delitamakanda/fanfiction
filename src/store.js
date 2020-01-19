import Vue from 'vue'
import Vuex from 'vuex'

import * as comment from './state/comment'
import * as fanfic from './state/fanfic'
import * as other from './state/other'
import * as user from './state/user'
import * as help from './state/help'
import * as post from './state/post'
import * as category from './state/category'
import * as chapter from './state/chapter'

Vue.use(Vuex)

const store = new Vuex.Store({
    strict: true,
    modules: {
        comment,
        fanfic,
        other,
        user,
        help,
        post,
        category,
        chapter,
    }
})

export default store
