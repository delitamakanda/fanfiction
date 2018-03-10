import Vue from 'vue'
import Router from 'vue-router'
import state from '../state'
import NotFound from '@/components/NotFound'
import List from '@/components/List'
import Detail from '@/components/Detail'
import Category from '@/components/Category'
import Subcategory from '@/components/Subcategory'
import Login from '@/components/Login'
import Blog from '@/components/Blog'
import Dashboard from '@/components/Dashboard'
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
            path: '/categories/:id',
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
            path: '/blog',
            name: 'Blog',
            component: Blog
        },
        {
            path: '/dashboard',
            name: 'Dashboard',
            component: Dashboard,
            meta: { private: true }
        },
        {
            path: '*',
            name: 'NotFound',
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

    if (to.meta.private && !state.user) {
        next({
            name: 'Login',
            params: {
                wantedRoute: to.fullPath,
            },
        })
        return
    }

    if ( to.meta.guest && state.user) {
        next({name: 'Dashboard'})
        return
    }

    next()
})

export default router
