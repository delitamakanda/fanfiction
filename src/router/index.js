import Vue from 'vue'
import Router from 'vue-router'
import state from '../state'
import NotFound from '@/components/NotFound'
import List from '@/components/List'
import Detail from '@/components/Detail'
import Category from '@/components/Category'
import Subcategory from '@/components/Subcategory'
import Login from '@/components/Login'
import Posts from '@/components/Posts'
import PostDetail from '@/components/PostDetail'
import Dashboard from '@/components/Dashboard'
import ListUserFanfic from '@/components/ListUserFanfic'
import NewFanfic from '@/components/NewFanfic'
import NewChapter from '@/components/NewChapter'
import Fanfic from '@/components/Fanfic'
import Loading from '@/components/Loading'
import Form from '@/components/Form'
import Input from '@/components/Input'

import VueFetch from '../plugins/fetch'

Vue.component('Loading', Loading)
Vue.component('Form', Form)
Vue.component('Input', Input)

Vue.use(Router)
Vue.use(VueFetch, {
    baseUrl: 'api/'
})

const router = new Router({
    routes: [
        {
            path: '/',
            name: 'List',
            component: List
        },
        {
            path: '/:id',
            name: 'Detail',
            component: Detail,
            props: true
        },
        {
            path: '/categories',
            name: 'Category',
            component: Category
        },
        {
            path: '/subcategory/:id',
            name: 'Subcategory',
            component: Subcategory,
            props: true
        },
        {
            path: '/login',
            name: 'Login',
            component: Login,
            meta: { guest: true }
        },
        {
            path: '/news',
            name: 'Posts',
            component: Posts
        },
        {
            path: '/news/:id',
            name: 'PostDetail',
            component: PostDetail,
            props: true
        },
        {
            path: '/dashboard',
            name: 'Dashboard',
            component: Dashboard,
            meta: { private: true },
            children: [
                { path: 'fanfics', name: 'ListUserFanfic', component: ListUserFanfic },
                { path: 'create', name: 'NewFanfic', component: NewFanfic },
                { path: 'update/:id', name: 'UpdateFanfic', component: NewFanfic, props: true },
                { path: 'new/chapter', name: 'NewChapter', component: NewChapter, props: true },
                { path: 'update/chapter/:id', name: 'UpdateChapter', component: NewChapter, props: true },
                { path: 'fanfic/:id', name: 'fanfic', component: Fanfic, props: true },
            ]
        },
        {
            path: '*',
            component: NotFound
        },
    ],
    mode: 'hash',
    scrollBehavior (to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        }
        if (to.hash) {
            return { selector: to.hash }
        }
        return { x: 0, y: 0 }
    },
})

router.beforeEach((to, from, next) => {

    if (to.meta.private) {
        // TODO:  redirect to login
    }

    if (to.matched.some(r => r.meta.private) && !state.user && state.user.id == null) {
        next({
            name: 'Login',
            params: {
                wantedRoute: to.fullPath,
            },
        })
        return
    }

    if ( to.matched.some(r => r.meta.guest) && state.user && state.user.id != null) {
        next({name: 'Dashboard'})
        return
    }

    next()
})

export default router
