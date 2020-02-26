import Vue from 'vue'
import Router from 'vue-router'
import state from '../state'
import store from '../store'

import List from '@/views/fanfics/List'
import Detail from '@/views/fanfics/Detail'
import Login from '@/views/Login'

import Dashboard from '@/views/admin/Dashboard'
import ListUserFanfic from '@/views/fanfics/ListUserFanfic'
import NewFanfic from '@/views/fanfics/NewFanfic'
import EditFanfic from '@/views/fanfics/EditFanfic'
import Reviews from '@/views/comments/Reviews'
import Social from '@/views/account/Social'
import MonProfil from '@/views/account/MonProfil'
import EditAccount from '@/views/account/EditAccount'

import News from '@/views/posts/News'
import EditNews from '@/views/posts/EditNews'

import Loading from '@/components/ui/Loading'
import Form from '@/components/ui/Form'
import Input from '@/components/ui/Input'
import Avatar from '@/components/ui/Avatar'

import VueFetch from '../plugins/fetch'
import VeeValidate from 'vee-validate'
import VueSVGIcon from 'vue-svgicon'
import VueTrumbowyg from 'vue-trumbowyg';

Vue.component('Loading', Loading)
Vue.component('Form', Form)
Vue.component('Input', Input)
Vue.component('Avatar', Avatar)

Vue.use(Router)
Vue.use(VueFetch, {
    baseUrl: 'api/'
})
Vue.use(VeeValidate)
Vue.use(VueSVGIcon)
Vue.use(VueTrumbowyg)

import 'trumbowyg/dist/ui/trumbowyg.css'

const router = new Router({
    routes: [
        {
            path: '/', name: 'List', component: List, meta: {
                title: 'Toutes les fanfictions',
                metaTags: [
                    {
                        name: 'description',
                        content: 'Fanfictions basées sur des Animés, mangas, films, romans, faits historiques, etc.'
                    },
                    {
                        property: 'og:description',
                        content: 'Fanfictions basées sur des Animés, mangas, films, romans, faits historiques, etc.'
                    }
                ]
            }
        },
        { path: '/fanfic/detail/:slug', name: 'Detail', component: Detail, props: true },
        { path: '/reviews', name: 'Reviews', component: Reviews, meta: { title: 'Mes reviews' }, props: true },
        { path: '/login', name: 'Login', component: Login, meta: { guest: true, title: 'Créer un compte ou se connecter à l\'espace membre' } },
        {
            path: '/news', name: 'News', component: News, meta: {
                title: 'News du site Fanfiction',
                metaTags: [
                    {
                        name: 'description',
                        content: 'Toutes les nouveautés et annonces du site.'
                    },
                    {
                        property: 'og:description',
                        content: 'Toutes les nouveautés et annonces du site.'
                    }
                ]
            }
        },
        {
            path: '/dashboard', name: 'Dashboard', redirect: '/dashboard/create', component: Dashboard, meta: { private: true, title: 'Tableau de bord' },
            children: [
                { path: 'fanfics/:username/list', name: 'ListUserFanfic', component: ListUserFanfic, props: true, meta: { title: 'Mes fanfictions', private: true } },
                { path: 'create', name: 'NewFanfic', component: NewFanfic, meta: { title: 'Ecrire une fanfiction', private: true } },
                { path: 'fanfic/:id', name: 'EditFanfic', component: EditFanfic, props: true, meta: { title: 'Voir la fanfiction', private: true } },
                {
                    path: 'edit-account', name: 'EditAccount', component: EditAccount, meta: { title: 'Edition du compte personnel', private: true }, redirect: '/dashboard/edit-account/my-profil', children: [
                        { path: 'my-profil', name: 'MonProfil', component: MonProfil, meta: { private: true, title: 'Mon profil' }, props: true },
                        { path: 'social', name: 'Social', component: Social, meta: { private: true, title: 'Social' }, props: true },
                        { path: 'my-reviews', name: 'MyReviews', component: Reviews, props: true, meta: { private: true, title: 'Commentaires' } },
                    ]
                },
                {
                    path: 'edit-news/:newsSlug', name: 'EditNews', component: EditNews, meta: { title: 'Ajout/Edition de news', private: true }, props: true, beforeEnter: (to, from, next) => {
                        const user = store.getters['user/user']
                        if (user.is_staff) {
                            next(true)
                        } else {
                            next({ name: 'Dashboard' })
                        }
                    }
                },
            ]
        },
        { path: '*', component: List, redirect: '/' },
        { path: '/fanfics/:username/show', name: 'ShowUserFanfic', component: ListUserFanfic, props: true, meta: { title: 'Voir les fanfictions d\'un utilisateur' } },
    ],
    mode: 'hash',
    scrollBehavior(to, from, savedPosition) {
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
    //const user = state.user
    const user = store.getters['user/user']

    if (to.matched.some(r => r.meta.private) && user && user.id == null) {

        next({
            name: 'Login',
            params: {
                wantedRoute: to.fullPath,
            },
        })
        return
    }

    if ( to.matched.some(r => r.meta.guest) && user && user.id != null) {
        next({name: 'Dashboard'})
        return
    }

    const nearestWithTitle = to.matched.slice().reverse().find(r => r.meta && r.meta.title);
    const nearestWithMeta = to.matched.slice().reverse().find(r => r.meta && r.meta.metaTags);
    const previousNearestWithMeta = from.matched.slice().reverse().find(r => r.meta && r.meta.metaTags);

    if(nearestWithTitle) document.title = nearestWithTitle.meta.title;

    Array.from(document.querySelectorAll('[data-vue-router-controlled]')).map(el => el.parentNode.removeChild(el));

    if(!nearestWithMeta) return next();

    nearestWithMeta.meta.metaTags.map(tagDef => {
        const tag = document.createElement('meta');
        Object.keys(tagDef).forEach(key => {
          tag.setAttribute(key, tagDef[key]);
        });

        tag.setAttribute('data-vue-router-controlled', '');

        return tag;
      })
      .forEach(tag => document.head.appendChild(tag));

    next()
})

export default router
