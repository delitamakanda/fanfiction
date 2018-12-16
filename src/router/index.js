import Vue from 'vue'
import Router from 'vue-router'
import state from '../state'
import store from '../store'
import List from '@/components/List'
import Detail from '@/components/Detail'
import Login from '@/views/Login'
import Dashboard from '@/views/Dashboard'
import ListUserFanfic from '@/components/ListUserFanfic'
import NewFanfic from '@/views/NewFanfic'
import NewChapter from '@/components/NewChapter'
import Fanfic from '@/components/Fanfic'
import EditAccount from '@/components/EditAccount'
import News from '@/views/News'

import Loading from '@/components/Loading'
import Form from '@/components/Form'
import Input from '@/components/Input'
import Pagination from '@/components/Pagination'
import Avatar from '@/components/Avatar'
import Grid from '@/components/Grid'

import VueFetch from '../plugins/fetch'
import VeeValidate from 'vee-validate'
import VueSVGIcon from 'vue-svgicon'
import VueTrumbowyg from 'vue-trumbowyg';

Vue.component('Loading', Loading)
Vue.component('Form', Form)
Vue.component('Input', Input)
Vue.component('Pagination', Pagination)
Vue.component('Avatar', Avatar)
Vue.component('Grid', Grid)

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
        { path: '/', name: 'List', component: List, meta: {
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
        } },
        { path: '/fanfic/detail/:slug', name: 'Detail', component: Detail, props: true},
        { path: '/login', name: 'Login', component: Login, meta: { guest: true, title: 'Créer un compte ou se connecter à l\'espace membre' } },
        { path: '/news', name: 'News', component: News, meta: {
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
        } },
        { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { private: true, title: 'Tableau de bord' },
            children: [
                { path: 'fanfics', name: 'ListUserFanfic', component: ListUserFanfic, meta: { title: 'Vos fanfictions', private: true } },
                { path: 'create', name: 'NewFanfic', component: NewFanfic, meta: { title: 'Ecrire une fanfiction', private: true } },
                { path: 'update/:id/edit', name: 'UpdateFanfic', component: NewFanfic, props: true, meta: { title: 'Editer une fanfiction', private: true } },
                { path: 'new/:id/chapter', name: 'NewChapter', component: NewChapter, props: true, meta: { title: 'Ecrire un chapitre', private: true } },
                { path: 'update/:id/chapter/:chapter_id/edit', name: 'UpdateChapter', component: NewChapter, props: true, meta: { title: 'Editer un chapitre', private: true } },
                { path: 'fanfic/:id', name: 'Fanfic', component: Fanfic, props: true, meta: { title: 'Voir la fanfiction', private: true } },
                { path: 'edit-account', name: 'EditAccount', component: EditAccount, meta: { title: 'Edition du compte personnel', private: true } },
                // TODO: ajout d'une news
                //{ path: 'edit-news', name: 'EditAccount', component: EditAccount, meta: { title: 'Ajout/Edition de news', private: true, is_admin: true } },
            ]
        },
        { path: '*', component: List, redirect: '/' },
        { path: '/fanfics/:username/show', name: 'ShowUserFanfic', component: ListUserFanfic, props: true, title: 'Voir les fanfictions d\'un utilisateur' },
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
    //const user = state.user
    const user = store.getters['user/user']

    if (to.matched.some(r => r.meta.private) && !user && user.id == null) {

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
