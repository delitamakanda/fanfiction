import Vue from 'vue'
import Router from 'vue-router'
import List from '@/components/List'
import Detail from '@/components/Detail'
import Category from '@/components/Category'
import Subcategory from '@/components/Subcategory'
import Login from '@/components/Login'
import Signup from '@/components/Signup'
import Loading from '@/components/Loading'

import VueFetch from '../plugins/fetch'

Vue.component('Loading', Loading)

Vue.use(Router)
Vue.use(VueFetch, {
    baseUrl: 'api/'
})

export default new Router({
    routes: [
        {
            path: '/',
            name: 'List',
            component: List,
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
            component: Login
        },
        {
            path: '/signup',
            name: 'Signup',
            component: Signup
        }
    ]
})
