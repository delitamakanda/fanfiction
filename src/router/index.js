import Vue from 'vue'
import Router from 'vue-router'
import state from '../state'
import List from '@/components/List'
import Detail from '@/components/Detail'
import Login from '@/components/Login'
import Posts from '@/components/Posts'
import PostDetail from '@/components/PostDetail'
import Dashboard from '@/components/Dashboard'
import ListUserFanfic from '@/components/ListUserFanfic'
import UpdateFanfic from '@/components/UpdateFanfic'
import UpdateChapter from '@/components/UpdateChapter'
import NewFanfic from '@/components/NewFanfic'
import NewChapter from '@/components/NewChapter'
import Fanfic from '@/components/Fanfic'
import ChangePassword from '@/components/ChangePassword'
import ShowUserFanfic from '@/components/ShowUserFanfic'
import Loading from '@/components/Loading'
import Form from '@/components/Form'
import Input from '@/components/Input'

import VueFetch from '../plugins/fetch'
import VueAffix from 'vue-affix'
import VeeValidate from 'vee-validate'
import VueSVGIcon from 'vue-svgicon'
import VueTrumbowyg from 'vue-trumbowyg';

Vue.component('Loading', Loading)
Vue.component('Form', Form)
Vue.component('Input', Input)

Vue.use(Router)
Vue.use(VueFetch, {
    baseUrl: 'api/'
})
Vue.use(VueAffix)
Vue.use(VeeValidate)
Vue.use(VueSVGIcon)
Vue.use(VueTrumbowyg)

import 'trumbowyg/dist/ui/trumbowyg.css'

const router = new Router({
    routes: [
        { path: '/', name: 'List', component: List },
        { path: '/fanfic/:slug/detail', name: 'Detail', component: Detail, props: true },
        { path: '/login', name: 'Login', component: Login, meta: { guest: true } },
        { path: '/news', name: 'Posts', component: Posts },
        { path: '/news/:slug', name: 'PostDetail', component: PostDetail, props: true },
        { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { private: true },
            children: [
                { path: '/fanfics', name: 'ListUserFanfic', component: ListUserFanfic },
                { path: '/create', name: 'NewFanfic', component: NewFanfic },
                { path: '/update/:id/edit', name: 'UpdateFanfic', component: UpdateFanfic, props: true },
                { path: '/new/:id/chapter', name: 'NewChapter', component: NewChapter, props: true },
                { path: '/update/:id/chapter/:chapter_id/edit', name: 'UpdateChapter', component: UpdateChapter, props: true },
                { path: '/fanfic/:id', name: 'Fanfic', component: Fanfic, props: true },
                { path: '/change-password', name: 'ChangePassword', component: ChangePassword },
            ]
        },
        { path: '*', component: List },
        { path: '/fanfics/:username/show', name: 'ShowUserFanfic', component: ShowUserFanfic, props: true },
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

// const prod = process.env.NODE_ENV === 'production'
// const shouldSW = 'serviceWorker' in navigator && prod
//
// if (shouldSW) {
//   navigator.serviceWorker.register('/sw.js').then(() => {
//     console.log('Sw registered')
//   })
// }



export default router
