import Vue from 'vue'
import Router from 'vue-router'
import List from '@/components/List'
import Detail from '@/components/Detail'
import Category from '@/components/Category'
import Login from '@/components/Login'
import Signup from '@/components/Signup'

Vue.use(Router)

export default new Router({
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
